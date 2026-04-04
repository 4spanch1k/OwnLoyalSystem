from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.db.base import ZERO_MONEY, utc_now
from backend.app.db.models.audit import AuditLog
from backend.app.db.models.loyalty import LoyaltyLedgerEntry, PatientWallet
from backend.app.db.models.loyalty_redemption import LoyaltyRedemption
from backend.app.db.models.payment import Payment, PaymentLine
from backend.app.services.loyalty.accrual import BONUS_ROUNDING_STEP, LEDGER_ENTRY_STATUS_POSTED, quantize_money
from backend.app.services.loyalty.eligibility import (
    RedemptionEligibilityResult,
    calculate_redemption_eligibility,
    get_active_policy_for_payment,
)
from backend.app.services.loyalty.errors import PaymentNotFoundError, PaymentStateError, RedemptionConflictError

PAYMENT_STATUS_PENDING = "pending"
REFUNDED_PAYMENT_STATUSES = {"refunded", "partially_refunded"}
LEDGER_ENTRY_REDEEM = "redeem"
REDEMPTION_STATUS_APPLIED = "applied"
REDEMPTION_IDEMPOTENCY_VERSION = "v1"


@dataclass(frozen=True)
class RedemptionQuoteResult:
    payment_id: str
    eligible_subtotal: Decimal
    wallet_available: Decimal
    cap_amount: Decimal
    max_redeemable: Decimal
    currency_code: str
    denied_categories: tuple[str, ...]
    policy_version_id: str


@dataclass(frozen=True)
class RedemptionApplyResult:
    redemption_id: str
    approved_amount: Decimal
    wallet_balance_after: Decimal
    ledger_entry_id: str
    status: str
    idempotency_key: str
    already_processed: bool


def build_redemption_apply_idempotency_key(payment_id: str, patient_id: str, client_request_id: str) -> str:
    return f"redemption_apply:{payment_id}:{patient_id}:{client_request_id}:{REDEMPTION_IDEMPOTENCY_VERSION}"


def quote_redemption(db: Session, tenant_id: str, payment_id: str) -> RedemptionQuoteResult:
    payment = _get_payment(db=db, tenant_id=tenant_id, payment_id=payment_id)
    _ensure_payment_allows_redemption(payment)

    payment_lines = _get_payment_lines(db=db, tenant_id=tenant_id, payment_id=payment_id)
    policy_context = get_active_policy_for_payment(db=db, tenant_id=tenant_id, branch_id=payment.branch_id)
    eligibility = calculate_redemption_eligibility(payment_lines=payment_lines, policy_rules=policy_context.rules_by_category)
    wallet = _get_wallet(db=db, tenant_id=tenant_id, patient_id=payment.patient_id)

    cap_amount = quantize_money(
        eligibility.eligible_total * Decimal(policy_context.policy.redemption_cap_bps) / Decimal("10000")
    )
    wallet_available = wallet.available_balance if wallet is not None else ZERO_MONEY
    max_redeemable = min(wallet_available, cap_amount)

    return RedemptionQuoteResult(
        payment_id=payment.id,
        eligible_subtotal=eligibility.eligible_total,
        wallet_available=wallet_available,
        cap_amount=cap_amount,
        max_redeemable=max_redeemable,
        currency_code=payment.currency,
        denied_categories=eligibility.denied_categories,
        policy_version_id=policy_context.policy.id,
    )


def apply_redemption(
    db: Session,
    tenant_id: str,
    payment_id: str,
    requested_amount: Decimal,
    client_request_id: str,
    actor_user_id: str | None = None,
) -> RedemptionApplyResult:
    with db.begin():
        payment = db.execute(
            select(Payment)
            .where(Payment.tenant_id == tenant_id, Payment.id == payment_id)
            .with_for_update()
        ).scalar_one_or_none()
        if payment is None:
            raise PaymentNotFoundError(f"Payment {payment_id} was not found in tenant {tenant_id}.")

        idempotency_key = build_redemption_apply_idempotency_key(payment_id, payment.patient_id, client_request_id)
        existing_redemption = _get_existing_redemption(db=db, tenant_id=tenant_id, idempotency_key=idempotency_key)
        if existing_redemption is not None:
            return _build_existing_redemption_result(
                db=db,
                tenant_id=tenant_id,
                redemption=existing_redemption,
                idempotency_key=idempotency_key,
            )

        _ensure_payment_allows_redemption(payment)
        normalized_requested_amount = quantize_money(requested_amount)
        if normalized_requested_amount < BONUS_ROUNDING_STEP:
            raise RedemptionConflictError("Requested redemption amount must be at least 0.01.")

        payment_lines = _get_payment_lines(db=db, tenant_id=tenant_id, payment_id=payment_id)
        policy_context = get_active_policy_for_payment(db=db, tenant_id=tenant_id, branch_id=payment.branch_id)
        eligibility = calculate_redemption_eligibility(payment_lines=payment_lines, policy_rules=policy_context.rules_by_category)
        wallet = db.execute(
            select(PatientWallet)
            .where(PatientWallet.tenant_id == tenant_id, PatientWallet.patient_id == payment.patient_id)
            .with_for_update()
        ).scalar_one_or_none()
        if wallet is None:
            raise RedemptionConflictError("Wallet is empty. Redemption cannot be applied.")

        quote_result = _build_locked_quote(
            payment=payment,
            wallet=wallet,
            redemption_cap_bps=policy_context.policy.redemption_cap_bps,
            eligibility=eligibility,
            policy_version_id=policy_context.policy.id,
        )
        if quote_result.max_redeemable <= ZERO_MONEY:
            raise RedemptionConflictError("Payment is not eligible for redemption.")
        if normalized_requested_amount > quote_result.max_redeemable:
            raise RedemptionConflictError("Requested redemption amount exceeds the allowed maximum.")

        try:
            with db.begin_nested():
                redemption = LoyaltyRedemption(
                    tenant_id=tenant_id,
                    patient_id=payment.patient_id,
                    payment_id=payment.id,
                    wallet_id=wallet.id,
                    policy_version_id=policy_context.policy.id,
                    requested_amount=normalized_requested_amount,
                    approved_amount=normalized_requested_amount,
                    currency=payment.currency,
                    status=REDEMPTION_STATUS_APPLIED,
                    idempotency_key=idempotency_key,
                    created_at=utc_now(),
                )
                db.add(redemption)
                db.flush()

                wallet_update_result = db.execute(
                    update(PatientWallet)
                    .where(
                        PatientWallet.tenant_id == tenant_id,
                        PatientWallet.id == wallet.id,
                        PatientWallet.available_balance >= normalized_requested_amount,
                    )
                    .values(
                        available_balance=PatientWallet.available_balance - normalized_requested_amount,
                        lifetime_redeemed=PatientWallet.lifetime_redeemed + normalized_requested_amount,
                        updated_at=utc_now(),
                    )
                )
                if wallet_update_result.rowcount != 1:
                    raise RedemptionConflictError("Wallet balance changed during redemption apply. Please refresh and retry.")

                refreshed_wallet = db.execute(
                    select(PatientWallet).where(PatientWallet.tenant_id == tenant_id, PatientWallet.id == wallet.id)
                ).scalar_one()
                ledger_entry = LoyaltyLedgerEntry(
                    tenant_id=tenant_id,
                    patient_id=payment.patient_id,
                    wallet_id=wallet.id,
                    payment_id=payment.id,
                    payment_line_id=None,
                    entry_type=LEDGER_ENTRY_REDEEM,
                    amount=normalized_requested_amount,
                    balance_after=quantize_money(refreshed_wallet.available_balance),
                    currency=payment.currency,
                    status=LEDGER_ENTRY_STATUS_POSTED,
                    policy_version_id=policy_context.policy.id,
                    idempotency_key=idempotency_key,
                    reason_code="redemption_apply",
                    metadata_json={
                        "eligible_subtotal": str(quote_result.eligible_subtotal),
                        "cap_amount": str(quote_result.cap_amount),
                    },
                    created_at=utc_now(),
                )
                db.add(ledger_entry)
                _append_redemption_audit_log(
                    db=db,
                    tenant_id=tenant_id,
                    actor_user_id=actor_user_id,
                    payment_id=payment.id,
                    idempotency_key=idempotency_key,
                    approved_amount=normalized_requested_amount,
                )
                db.flush()
        except IntegrityError:
            existing_redemption = _get_existing_redemption(db=db, tenant_id=tenant_id, idempotency_key=idempotency_key)
            if existing_redemption is None:
                raise
            return _build_existing_redemption_result(
                db=db,
                tenant_id=tenant_id,
                redemption=existing_redemption,
                idempotency_key=idempotency_key,
            )

        return RedemptionApplyResult(
            redemption_id=redemption.id,
            approved_amount=redemption.approved_amount,
            wallet_balance_after=ledger_entry.balance_after,
            ledger_entry_id=ledger_entry.id,
            status=redemption.status,
            idempotency_key=idempotency_key,
            already_processed=False,
        )


def _build_locked_quote(
    payment: Payment,
    wallet: PatientWallet,
    redemption_cap_bps: int,
    eligibility: RedemptionEligibilityResult,
    policy_version_id: str,
) -> RedemptionQuoteResult:
    cap_amount = quantize_money(eligibility.eligible_total * Decimal(redemption_cap_bps) / Decimal("10000"))
    wallet_available = quantize_money(wallet.available_balance)
    max_redeemable = min(wallet_available, cap_amount)
    return RedemptionQuoteResult(
        payment_id=payment.id,
        eligible_subtotal=eligibility.eligible_total,
        wallet_available=wallet_available,
        cap_amount=cap_amount,
        max_redeemable=max_redeemable,
        currency_code=payment.currency,
        denied_categories=eligibility.denied_categories,
        policy_version_id=policy_version_id,
    )


def _get_existing_redemption(db: Session, tenant_id: str, idempotency_key: str) -> LoyaltyRedemption | None:
    return db.execute(
        select(LoyaltyRedemption).where(
            LoyaltyRedemption.tenant_id == tenant_id,
            LoyaltyRedemption.idempotency_key == idempotency_key,
        )
    ).scalar_one_or_none()


def _build_existing_redemption_result(
    db: Session,
    tenant_id: str,
    redemption: LoyaltyRedemption,
    idempotency_key: str,
) -> RedemptionApplyResult:
    ledger_entry = db.execute(
        select(LoyaltyLedgerEntry).where(
            LoyaltyLedgerEntry.tenant_id == tenant_id,
            LoyaltyLedgerEntry.idempotency_key == idempotency_key,
        )
    ).scalar_one()
    wallet = db.execute(
        select(PatientWallet).where(PatientWallet.tenant_id == tenant_id, PatientWallet.id == redemption.wallet_id)
    ).scalar_one()
    return RedemptionApplyResult(
        redemption_id=redemption.id,
        approved_amount=redemption.approved_amount,
        wallet_balance_after=wallet.available_balance,
        ledger_entry_id=ledger_entry.id,
        status=redemption.status,
        idempotency_key=idempotency_key,
        already_processed=True,
    )


def _get_payment(db: Session, tenant_id: str, payment_id: str) -> Payment:
    payment = db.execute(select(Payment).where(Payment.tenant_id == tenant_id, Payment.id == payment_id)).scalar_one_or_none()
    if payment is None:
        raise PaymentNotFoundError(f"Payment {payment_id} was not found in tenant {tenant_id}.")
    return payment


def _ensure_payment_allows_redemption(payment: Payment) -> None:
    if payment.status != PAYMENT_STATUS_PENDING:
        raise PaymentStateError("Only pending payments can accept redemption apply.")
    if payment.refunded_at is not None or payment.status in REFUNDED_PAYMENT_STATUSES:
        raise PaymentStateError("Refunded payments cannot accept redemption apply.")


def _get_payment_lines(db: Session, tenant_id: str, payment_id: str) -> list[PaymentLine]:
    return db.execute(
        select(PaymentLine).where(PaymentLine.tenant_id == tenant_id, PaymentLine.payment_id == payment_id)
    ).scalars().all()


def _get_wallet(db: Session, tenant_id: str, patient_id: str) -> PatientWallet | None:
    return db.execute(
        select(PatientWallet).where(PatientWallet.tenant_id == tenant_id, PatientWallet.patient_id == patient_id)
    ).scalar_one_or_none()


def _append_redemption_audit_log(
    db: Session,
    tenant_id: str,
    actor_user_id: str | None,
    payment_id: str,
    idempotency_key: str,
    approved_amount: Decimal,
) -> None:
    db.add(
        AuditLog(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            entity_type="payment",
            entity_id=payment_id,
            action="loyalty_redemption_applied",
            payload_json={
                "idempotency_key": idempotency_key,
                "approved_amount": str(approved_amount),
            },
            created_at=utc_now(),
        )
    )
