from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.db.base import ZERO_MONEY, utc_now
from backend.app.db.models.audit import AuditLog
from backend.app.db.models.loyalty import LoyaltyLedgerEntry, PatientWallet
from backend.app.db.models.patient import Patient
from backend.app.db.models.payment import Payment, PaymentLine
from backend.app.services.loyalty.eligibility import calculate_eligible_accrual_base, get_active_policy_for_payment
from backend.app.services.loyalty.errors import PaymentNotFoundError, PaymentStateError, PatientNotFoundError

PAYMENT_STATUS_PENDING = "pending"
PAYMENT_STATUS_CONFIRMED = "confirmed"
REFUNDED_PAYMENT_STATUSES = {"refunded", "partially_refunded"}
LEDGER_ENTRY_ACCRUAL = "accrual"
LEDGER_ENTRY_STATUS_POSTED = "posted"
IDEMPOTENCY_VERSION = "v1"
BONUS_ROUNDING_STEP = Decimal("0.01")


@dataclass(frozen=True)
class AccrualProcessingResult:
    payment_id: str
    payment_status: str
    confirmed_at: datetime | None
    accrual_amount: Decimal
    wallet_balance: Decimal
    currency_code: str
    ledger_entry_id: str | None
    idempotency_key: str
    already_processed: bool


def build_payment_confirmed_idempotency_key(payment_id: str) -> str:
    return f"payment_confirmed:{payment_id}:accrual:{IDEMPOTENCY_VERSION}"


def quantize_money(amount: Decimal) -> Decimal:
    return amount.quantize(BONUS_ROUNDING_STEP, rounding=ROUND_HALF_UP)


def confirm_payment(db: Session, tenant_id: str, payment_id: str, actor_user_id: str | None = None) -> AccrualProcessingResult:
    with db.begin():
        payment = db.execute(
            select(Payment)
            .where(Payment.tenant_id == tenant_id, Payment.id == payment_id)
            .with_for_update()
        ).scalar_one_or_none()
        if payment is None:
            raise PaymentNotFoundError(f"Payment {payment_id} was not found in tenant {tenant_id}.")
        allowed_payment_statuses = {PAYMENT_STATUS_PENDING, PAYMENT_STATUS_CONFIRMED} | REFUNDED_PAYMENT_STATUSES
        if payment.status not in allowed_payment_statuses:
            raise PaymentStateError(f"Payment status '{payment.status}' cannot be confirmed.")

        if payment.status != PAYMENT_STATUS_CONFIRMED:
            if payment.status in REFUNDED_PAYMENT_STATUSES:
                return process_payment_confirmed(db=db, tenant_id=tenant_id, payment_id=payment_id, actor_user_id=actor_user_id)
            payment.status = PAYMENT_STATUS_CONFIRMED
            payment.confirmed_at = payment.confirmed_at or utc_now()
            db.flush()

        return process_payment_confirmed(db=db, tenant_id=tenant_id, payment_id=payment_id, actor_user_id=actor_user_id)


def process_payment_confirmed(
    db: Session,
    tenant_id: str,
    payment_id: str,
    actor_user_id: str | None = None,
) -> AccrualProcessingResult:
    payment = db.execute(select(Payment).where(Payment.tenant_id == tenant_id, Payment.id == payment_id)).scalar_one_or_none()
    if payment is None:
        raise PaymentNotFoundError(f"Payment {payment_id} was not found in tenant {tenant_id}.")

    idempotency_key = build_payment_confirmed_idempotency_key(payment_id)
    existing_entry = _get_existing_ledger_entry(db=db, tenant_id=tenant_id, idempotency_key=idempotency_key)
    if existing_entry is not None:
        return _build_existing_result(db=db, payment=payment, existing_entry=existing_entry, idempotency_key=idempotency_key)

    if payment.status != PAYMENT_STATUS_CONFIRMED:
        raise PaymentStateError("Payment must be confirmed before loyalty accrual is processed.")
    if payment.refunded_at is not None or payment.status in REFUNDED_PAYMENT_STATUSES:
        raise PaymentStateError("Refunded payments cannot accrue loyalty bonuses.")

    payment_lines = db.execute(
        select(PaymentLine).where(PaymentLine.tenant_id == tenant_id, PaymentLine.payment_id == payment_id)
    ).scalars().all()
    policy_context = get_active_policy_for_payment(db=db, tenant_id=tenant_id, branch_id=payment.branch_id)
    eligible_amount = calculate_eligible_accrual_base(payment_lines=payment_lines, policy_rules=policy_context.rules_by_category)
    accrual_amount = quantize_money(eligible_amount * Decimal(policy_context.policy.accrual_rate_bps) / Decimal("10000"))

    if eligible_amount <= ZERO_MONEY or accrual_amount <= ZERO_MONEY:
        _append_audit_log(
            db=db,
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            entity_type="payment",
            entity_id=payment.id,
            action="loyalty_accrual_skipped",
            payload_json={
                "idempotency_key": idempotency_key,
                "eligible_amount": str(eligible_amount),
                "accrual_rate_bps": policy_context.policy.accrual_rate_bps,
            },
        )
        wallet = db.execute(
            select(PatientWallet).where(PatientWallet.tenant_id == tenant_id, PatientWallet.patient_id == payment.patient_id)
        ).scalar_one_or_none()
        wallet_balance = wallet.available_balance if wallet is not None else ZERO_MONEY
        db.flush()
        return AccrualProcessingResult(
            payment_id=payment.id,
            payment_status=payment.status,
            confirmed_at=payment.confirmed_at,
            accrual_amount=ZERO_MONEY,
            wallet_balance=wallet_balance,
            currency_code=payment.currency,
            ledger_entry_id=None,
            idempotency_key=idempotency_key,
            already_processed=False,
        )

    try:
        with db.begin_nested():
            patient = db.execute(
                select(Patient)
                .where(Patient.tenant_id == tenant_id, Patient.id == payment.patient_id)
                .with_for_update()
            ).scalar_one_or_none()
            if patient is None:
                raise PatientNotFoundError(f"Patient {payment.patient_id} was not found in tenant {tenant_id}.")

            wallet = db.execute(
                select(PatientWallet)
                .where(PatientWallet.tenant_id == tenant_id, PatientWallet.patient_id == payment.patient_id)
                .with_for_update()
            ).scalar_one_or_none()
            if wallet is None:
                wallet = PatientWallet(
                    tenant_id=tenant_id,
                    patient_id=payment.patient_id,
                    available_balance=ZERO_MONEY,
                    lifetime_accrued=ZERO_MONEY,
                    lifetime_redeemed=ZERO_MONEY,
                    lifetime_expired=ZERO_MONEY,
                    updated_at=utc_now(),
                )
                db.add(wallet)
                db.flush()

            wallet.available_balance = quantize_money(wallet.available_balance + accrual_amount)
            wallet.lifetime_accrued = quantize_money(wallet.lifetime_accrued + accrual_amount)
            wallet.updated_at = utc_now()

            ledger_entry = LoyaltyLedgerEntry(
                tenant_id=tenant_id,
                patient_id=payment.patient_id,
                wallet_id=wallet.id,
                payment_id=payment.id,
                payment_line_id=None,
                entry_type=LEDGER_ENTRY_ACCRUAL,
                amount=accrual_amount,
                balance_after=wallet.available_balance,
                currency=payment.currency,
                status=LEDGER_ENTRY_STATUS_POSTED,
                policy_version_id=policy_context.policy.id,
                idempotency_key=idempotency_key,
                reason_code="payment_confirmed",
                metadata_json={
                    "eligible_amount": str(eligible_amount),
                    "accrual_rate_bps": policy_context.policy.accrual_rate_bps,
                },
                created_at=utc_now(),
            )
            db.add(ledger_entry)
            _append_audit_log(
                db=db,
                tenant_id=tenant_id,
                actor_user_id=actor_user_id,
                entity_type="payment",
                entity_id=payment.id,
                action="loyalty_accrual_created",
                payload_json={
                    "ledger_entry_id": ledger_entry.id,
                    "idempotency_key": idempotency_key,
                    "accrual_amount": str(accrual_amount),
                },
            )
            db.flush()
    except IntegrityError:
        existing_entry = _get_existing_ledger_entry(db=db, tenant_id=tenant_id, idempotency_key=idempotency_key)
        if existing_entry is None:
            raise
        return _build_existing_result(db=db, payment=payment, existing_entry=existing_entry, idempotency_key=idempotency_key)

    return AccrualProcessingResult(
        payment_id=payment.id,
        payment_status=payment.status,
        confirmed_at=payment.confirmed_at,
        accrual_amount=accrual_amount,
        wallet_balance=ledger_entry.balance_after,
        currency_code=payment.currency,
        ledger_entry_id=ledger_entry.id,
        idempotency_key=idempotency_key,
        already_processed=False,
    )


def _append_audit_log(
    db: Session,
    tenant_id: str,
    actor_user_id: str | None,
    entity_type: str,
    entity_id: str,
    action: str,
    payload_json: dict[str, object],
) -> None:
    audit_log = AuditLog(
        tenant_id=tenant_id,
        actor_user_id=actor_user_id,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        payload_json=payload_json,
        created_at=utc_now(),
    )
    db.add(audit_log)


def _build_existing_result(
    db: Session,
    payment: Payment,
    existing_entry: LoyaltyLedgerEntry,
    idempotency_key: str,
) -> AccrualProcessingResult:
    wallet = db.execute(
        select(PatientWallet).where(PatientWallet.tenant_id == payment.tenant_id, PatientWallet.id == existing_entry.wallet_id)
    ).scalar_one()
    return AccrualProcessingResult(
        payment_id=payment.id,
        payment_status=payment.status,
        confirmed_at=payment.confirmed_at,
        accrual_amount=existing_entry.amount,
        wallet_balance=wallet.available_balance,
        currency_code=existing_entry.currency,
        ledger_entry_id=existing_entry.id,
        idempotency_key=idempotency_key,
        already_processed=True,
    )


def _get_existing_ledger_entry(db: Session, tenant_id: str, idempotency_key: str) -> LoyaltyLedgerEntry | None:
    return db.execute(
        select(LoyaltyLedgerEntry).where(
            LoyaltyLedgerEntry.tenant_id == tenant_id,
            LoyaltyLedgerEntry.idempotency_key == idempotency_key,
        )
    ).scalar_one_or_none()
