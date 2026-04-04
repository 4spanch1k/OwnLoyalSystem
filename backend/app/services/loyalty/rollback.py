from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.db.base import ZERO_MONEY, utc_now
from backend.app.db.models.audit import AuditLog
from backend.app.db.models.loyalty import LoyaltyLedgerEntry, PatientWallet
from backend.app.db.models.payment import Payment
from backend.app.services.loyalty.accrual import BONUS_ROUNDING_STEP, LEDGER_ENTRY_STATUS_POSTED, quantize_money
from backend.app.services.loyalty.errors import PaymentNotFoundError, PaymentStateError, RollbackConflictError

PAYMENT_STATUS_PENDING = "pending"
PAYMENT_STATUS_CONFIRMED = "confirmed"
PAYMENT_STATUS_PARTIALLY_REFUNDED = "partially_refunded"
PAYMENT_STATUS_REFUNDED = "refunded"
LEDGER_ENTRY_ACCRUAL = "accrual"
LEDGER_ENTRY_ROLLBACK = "rollback"
ROLLBACK_IDEMPOTENCY_VERSION = "v1"
PAYMENT_REFUND_REASON_FULL = "payment_refund_full"
PAYMENT_REFUND_REASON_PARTIAL = "payment_refund_partial"
ROLLBACK_REASON_CODES = {PAYMENT_REFUND_REASON_FULL, PAYMENT_REFUND_REASON_PARTIAL}


@dataclass(frozen=True)
class PaymentRefundResult:
    payment_id: str
    refund_status: str
    refunded_amount: Decimal
    rollback_amount: Decimal
    wallet_balance_after: Decimal
    ledger_entry_id: str | None
    idempotency_key: str
    already_processed: bool


def build_payment_refunded_idempotency_key(payment_id: str, refund_marker: str) -> str:
    return f"payment_refunded:{payment_id}:rollback:{refund_marker}:{ROLLBACK_IDEMPOTENCY_VERSION}"


def process_payment_refunded(
    db: Session,
    tenant_id: str,
    payment_id: str,
    refunded_amount: Decimal,
    actor_user_id: str | None = None,
    refund_marker: str | None = None,
    reason: str | None = None,
) -> PaymentRefundResult:
    if refund_marker is None:
        raise RollbackConflictError("Refund marker is required for idempotent rollback processing.")

    normalized_refunded_amount = quantize_money(refunded_amount)
    idempotency_key = build_payment_refunded_idempotency_key(payment_id, refund_marker)

    with db.begin():
        payment = db.execute(
            select(Payment)
            .where(Payment.tenant_id == tenant_id, Payment.id == payment_id)
            .with_for_update()
        ).scalar_one_or_none()
        if payment is None:
            raise PaymentNotFoundError(f"Payment {payment_id} was not found in tenant {tenant_id}.")

        existing_entry = _get_existing_rollback_entry(db=db, tenant_id=tenant_id, idempotency_key=idempotency_key)
        if existing_entry is not None:
            return _build_existing_result(db=db, payment=payment, existing_entry=existing_entry, idempotency_key=idempotency_key)

        if normalized_refunded_amount < BONUS_ROUNDING_STEP:
            raise RollbackConflictError("Refunded amount must be at least 0.01.")
        if normalized_refunded_amount > payment.total_amount:
            raise RollbackConflictError("Refunded amount cannot exceed the original payment total.")
        if payment.refunded_amount and normalized_refunded_amount < payment.refunded_amount:
            raise RollbackConflictError("Refunded amount cannot go backwards for cumulative refund handling.")

        payment.refunded_amount = normalized_refunded_amount
        payment.refunded_at = utc_now()
        payment.status = _resolve_refund_status(payment=payment, refunded_amount=normalized_refunded_amount)

        accrual_entries, accrual_total = get_payment_accrual_totals(db=db, tenant_id=tenant_id, payment_id=payment_id)
        wallet = db.execute(
            select(PatientWallet)
            .where(PatientWallet.tenant_id == tenant_id, PatientWallet.patient_id == payment.patient_id)
            .with_for_update()
        ).scalar_one_or_none()
        wallet_balance = wallet.available_balance if wallet is not None else ZERO_MONEY

        if accrual_total <= ZERO_MONEY:
            _append_audit_log(
                db=db,
                tenant_id=tenant_id,
                actor_user_id=actor_user_id,
                payment_id=payment.id,
                action="loyalty_rollback_skipped_no_accrual",
                payload_json={
                    "idempotency_key": idempotency_key,
                    "refunded_amount": str(normalized_refunded_amount),
                    "reason": reason,
                },
            )
            db.flush()
            return PaymentRefundResult(
                payment_id=payment.id,
                refund_status=payment.status,
                refunded_amount=payment.refunded_amount,
                rollback_amount=ZERO_MONEY,
                wallet_balance_after=wallet_balance,
                ledger_entry_id=None,
                idempotency_key=idempotency_key,
                already_processed=False,
            )

        rollback_total = get_payment_rollback_totals(db=db, tenant_id=tenant_id, payment_id=payment_id)
        target_rollback = calculate_target_rollback(
            payment_total=payment.total_amount,
            accrual_total=accrual_total,
            refunded_amount=normalized_refunded_amount,
        )
        delta_to_rollback = quantize_money(target_rollback - rollback_total)

        if delta_to_rollback <= ZERO_MONEY:
            db.flush()
            return PaymentRefundResult(
                payment_id=payment.id,
                refund_status=payment.status,
                refunded_amount=payment.refunded_amount,
                rollback_amount=ZERO_MONEY,
                wallet_balance_after=wallet_balance,
                ledger_entry_id=None,
                idempotency_key=idempotency_key,
                already_processed=False,
            )

        if wallet is None:
            raise RollbackConflictError("Wallet is missing for payment with accrued bonuses.")
        if wallet.available_balance < delta_to_rollback:
            raise RollbackConflictError("Rollback exceeds available wallet balance. Cross-flow reconciliation is not enabled.")

        rollback_reason = PAYMENT_REFUND_REASON_FULL if normalized_refunded_amount == payment.total_amount else PAYMENT_REFUND_REASON_PARTIAL
        source_policy_version_id = accrual_entries[-1].policy_version_id if accrual_entries else None

        try:
            with db.begin_nested():
                wallet.available_balance = quantize_money(wallet.available_balance - delta_to_rollback)
                wallet.updated_at = utc_now()

                rollback_entry = LoyaltyLedgerEntry(
                    tenant_id=tenant_id,
                    patient_id=payment.patient_id,
                    wallet_id=wallet.id,
                    payment_id=payment.id,
                    payment_line_id=None,
                    entry_type=LEDGER_ENTRY_ROLLBACK,
                    amount=delta_to_rollback,
                    balance_after=wallet.available_balance,
                    currency=payment.currency,
                    status=LEDGER_ENTRY_STATUS_POSTED,
                    policy_version_id=source_policy_version_id,
                    idempotency_key=idempotency_key,
                    reason_code=rollback_reason,
                    metadata_json={
                        "source_accrual_amount": str(accrual_total),
                        "refund_ratio": str(quantize_money(normalized_refunded_amount / payment.total_amount)),
                        "refunded_amount": str(normalized_refunded_amount),
                        "reason": reason,
                    },
                    created_at=utc_now(),
                )
                db.add(rollback_entry)
                _append_audit_log(
                    db=db,
                    tenant_id=tenant_id,
                    actor_user_id=actor_user_id,
                    payment_id=payment.id,
                    action="loyalty_rollback_created",
                    payload_json={
                        "idempotency_key": idempotency_key,
                        "rollback_amount": str(delta_to_rollback),
                        "refunded_amount": str(normalized_refunded_amount),
                        "reason": reason,
                    },
                )
                db.flush()
        except IntegrityError:
            existing_entry = _get_existing_rollback_entry(db=db, tenant_id=tenant_id, idempotency_key=idempotency_key)
            if existing_entry is None:
                raise
            return _build_existing_result(db=db, payment=payment, existing_entry=existing_entry, idempotency_key=idempotency_key)

        return PaymentRefundResult(
            payment_id=payment.id,
            refund_status=payment.status,
            refunded_amount=payment.refunded_amount,
            rollback_amount=delta_to_rollback,
            wallet_balance_after=rollback_entry.balance_after,
            ledger_entry_id=rollback_entry.id,
            idempotency_key=idempotency_key,
            already_processed=False,
        )


def get_payment_accrual_totals(
    db: Session,
    tenant_id: str,
    payment_id: str,
) -> tuple[list[LoyaltyLedgerEntry], Decimal]:
    accrual_entries = db.execute(
        select(LoyaltyLedgerEntry)
        .where(
            LoyaltyLedgerEntry.tenant_id == tenant_id,
            LoyaltyLedgerEntry.payment_id == payment_id,
            LoyaltyLedgerEntry.entry_type == LEDGER_ENTRY_ACCRUAL,
        )
        .order_by(LoyaltyLedgerEntry.created_at.asc())
    ).scalars().all()
    total = sum((entry.amount for entry in accrual_entries), ZERO_MONEY)
    return accrual_entries, quantize_money(total)


def get_payment_rollback_totals(db: Session, tenant_id: str, payment_id: str) -> Decimal:
    rollback_entries = db.execute(
        select(LoyaltyLedgerEntry)
        .where(
            LoyaltyLedgerEntry.tenant_id == tenant_id,
            LoyaltyLedgerEntry.payment_id == payment_id,
            LoyaltyLedgerEntry.entry_type == LEDGER_ENTRY_ROLLBACK,
        )
        .order_by(LoyaltyLedgerEntry.created_at.asc())
    ).scalars().all()
    total = sum((entry.amount for entry in rollback_entries if entry.reason_code in ROLLBACK_REASON_CODES), ZERO_MONEY)
    return quantize_money(total)


def calculate_target_rollback(
    payment_total: Decimal,
    accrual_total: Decimal,
    refunded_amount: Decimal,
) -> Decimal:
    if payment_total <= ZERO_MONEY:
        raise RollbackConflictError("Payment total must be positive for refund rollback processing.")
    if refunded_amount >= payment_total:
        return quantize_money(accrual_total)
    refund_ratio = refunded_amount / payment_total
    return quantize_money(accrual_total * refund_ratio)


def _resolve_refund_status(payment: Payment, refunded_amount: Decimal) -> str:
    if refunded_amount >= payment.total_amount:
        return PAYMENT_STATUS_REFUNDED
    if refunded_amount > ZERO_MONEY:
        return PAYMENT_STATUS_PARTIALLY_REFUNDED
    return PAYMENT_STATUS_CONFIRMED


def _get_existing_rollback_entry(db: Session, tenant_id: str, idempotency_key: str) -> LoyaltyLedgerEntry | None:
    return db.execute(
        select(LoyaltyLedgerEntry).where(
            LoyaltyLedgerEntry.tenant_id == tenant_id,
            LoyaltyLedgerEntry.idempotency_key == idempotency_key,
        )
    ).scalar_one_or_none()


def _build_existing_result(
    db: Session,
    payment: Payment,
    existing_entry: LoyaltyLedgerEntry,
    idempotency_key: str,
) -> PaymentRefundResult:
    wallet = db.execute(
        select(PatientWallet).where(PatientWallet.tenant_id == payment.tenant_id, PatientWallet.id == existing_entry.wallet_id)
    ).scalar_one()
    return PaymentRefundResult(
        payment_id=payment.id,
        refund_status=payment.status,
        refunded_amount=payment.refunded_amount,
        rollback_amount=existing_entry.amount,
        wallet_balance_after=wallet.available_balance,
        ledger_entry_id=existing_entry.id,
        idempotency_key=idempotency_key,
        already_processed=True,
    )


def _append_audit_log(
    db: Session,
    tenant_id: str,
    actor_user_id: str | None,
    payment_id: str,
    action: str,
    payload_json: dict[str, object | None],
) -> None:
    db.add(
        AuditLog(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            entity_type="payment",
            entity_id=payment_id,
            action=action,
            payload_json=payload_json,
            created_at=utc_now(),
        )
    )
