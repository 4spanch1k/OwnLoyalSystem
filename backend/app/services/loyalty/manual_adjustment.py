from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.base import ZERO_MONEY, utc_now
from backend.app.db.models.audit import AuditLog
from backend.app.db.models.loyalty import LoyaltyLedgerEntry, PatientWallet
from backend.app.db.models.loyalty_manual_adjustment import LoyaltyManualAdjustment
from backend.app.db.models.patient import Patient
from backend.app.db.models.rbac import UserMembership
from backend.app.db.models.tenancy import Tenant
from backend.app.services.loyalty.accrual import LEDGER_ENTRY_STATUS_POSTED, quantize_money
from backend.app.services.loyalty.errors import (
    ManualAdjustmentConflictError,
    ManualAdjustmentPermissionError,
    ManualAdjustmentValidationError,
    PatientNotFoundError,
)

ALLOWED_MANUAL_ADJUSTMENT_ROLES = {"clinic_manager", "owner"}
MANUAL_ADJUSTMENT_REASON_CODES = {
    "customer_support_correction",
    "billing_fix",
    "migration_fix",
    "goodwill_credit",
    "fraud_reversal",
    "admin_error_fix",
}
MANUAL_ADJUSTMENT_DIRECTION_CREDIT = "credit"
MANUAL_ADJUSTMENT_DIRECTION_DEBIT = "debit"
MANUAL_ADJUSTMENT_MIN_AMOUNT = Decimal("0.01")
LEDGER_ENTRY_MANUAL_ADJUSTMENT = "manual_adjustment"
AUDIT_ACTION_MANUAL_ADJUSTMENT_CREATED = "loyalty_manual_adjustment_created"
AUDIT_ENTITY_TYPE_PATIENT_WALLET = "patient_wallet"
MANUAL_ADJUSTMENT_IDEMPOTENCY_PREFIX = "manual_adjustment"
DEFAULT_CURRENCY_CODE = "KZT"


@dataclass(frozen=True)
class ManualAdjustmentResult:
    adjustment_id: str
    patient_id: str
    wallet_id: str
    ledger_entry_id: str
    audit_log_id: str
    direction: str
    amount: Decimal
    balance_before: Decimal
    wallet_balance_after: Decimal
    reason_code: str
    comment: str
    applied_at: datetime


def create_manual_adjustment(
    db: Session,
    tenant_id: str,
    patient_id: str,
    amount: Decimal,
    direction: str,
    reason_code: str,
    comment: str,
    actor_user_id: str | None,
) -> ManualAdjustmentResult:
    normalized_direction = _normalize_direction(direction)
    normalized_reason_code = _normalize_reason_code(reason_code)
    normalized_comment = _normalize_comment(comment)
    normalized_amount = _normalize_amount(amount)

    with db.begin():
        patient = db.execute(
            select(Patient)
            .where(Patient.tenant_id == tenant_id, Patient.id == patient_id)
            .with_for_update()
        ).scalar_one_or_none()
        if patient is None:
            raise PatientNotFoundError(f"Patient {patient_id} was not found in tenant {tenant_id}.")

        _ensure_actor_is_allowed(
            db=db,
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            patient_branch_id=patient.branch_id,
        )

        wallet = db.execute(
            select(PatientWallet)
            .where(PatientWallet.tenant_id == tenant_id, PatientWallet.patient_id == patient_id)
            .with_for_update()
        ).scalar_one_or_none()
        if wallet is None:
            if normalized_direction == MANUAL_ADJUSTMENT_DIRECTION_DEBIT:
                raise ManualAdjustmentConflictError("Manual debit cannot be applied because the wallet balance is empty.")
            wallet = PatientWallet(
                tenant_id=tenant_id,
                patient_id=patient_id,
                available_balance=ZERO_MONEY,
                lifetime_accrued=ZERO_MONEY,
                lifetime_redeemed=ZERO_MONEY,
                lifetime_expired=ZERO_MONEY,
                updated_at=utc_now(),
            )
            db.add(wallet)
            db.flush()

        balance_before = quantize_money(wallet.available_balance)
        balance_after = _calculate_balance_after(
            balance_before=balance_before,
            amount=normalized_amount,
            direction=normalized_direction,
        )
        applied_at = utc_now()
        currency_code = _get_currency_code(db=db, tenant_id=tenant_id)

        wallet.available_balance = balance_after
        wallet.updated_at = applied_at

        ledger_entry = LoyaltyLedgerEntry(
            tenant_id=tenant_id,
            patient_id=patient_id,
            wallet_id=wallet.id,
            payment_id=None,
            payment_line_id=None,
            entry_type=LEDGER_ENTRY_MANUAL_ADJUSTMENT,
            amount=normalized_amount,
            balance_after=balance_after,
            currency=currency_code,
            status=LEDGER_ENTRY_STATUS_POSTED,
            policy_version_id=None,
            idempotency_key=_build_manual_adjustment_idempotency_key(),
            reason_code=normalized_reason_code,
            metadata_json={
                "direction": normalized_direction,
                "comment": normalized_comment,
                "actor_user_id": actor_user_id,
                "balance_before": str(balance_before),
                "balance_after": str(balance_after),
            },
            created_at=applied_at,
        )
        db.add(ledger_entry)
        db.flush()

        adjustment = LoyaltyManualAdjustment(
            tenant_id=tenant_id,
            patient_id=patient_id,
            wallet_id=wallet.id,
            ledger_entry_id=ledger_entry.id,
            actor_user_id=actor_user_id,
            direction=normalized_direction,
            amount=normalized_amount,
            balance_before=balance_before,
            balance_after=balance_after,
            currency=currency_code,
            reason_code=normalized_reason_code,
            comment=normalized_comment,
            created_at=applied_at,
            applied_at=applied_at,
        )
        db.add(adjustment)
        db.flush()

        audit_log = _append_audit_log(
            db=db,
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            wallet_id=wallet.id,
            patient_id=patient_id,
            adjustment=adjustment,
            ledger_entry=ledger_entry,
        )
        db.flush()

        return ManualAdjustmentResult(
            adjustment_id=adjustment.id,
            patient_id=patient_id,
            wallet_id=wallet.id,
            ledger_entry_id=ledger_entry.id,
            audit_log_id=audit_log.id,
            direction=normalized_direction,
            amount=normalized_amount,
            balance_before=balance_before,
            wallet_balance_after=balance_after,
            reason_code=normalized_reason_code,
            comment=normalized_comment,
            applied_at=applied_at,
        )


def _normalize_direction(direction: str) -> str:
    normalized_direction = direction.strip().lower()
    if normalized_direction not in {MANUAL_ADJUSTMENT_DIRECTION_CREDIT, MANUAL_ADJUSTMENT_DIRECTION_DEBIT}:
        raise ManualAdjustmentValidationError("Direction must be either 'credit' or 'debit'.")
    return normalized_direction


def _normalize_reason_code(reason_code: str) -> str:
    normalized_reason_code = reason_code.strip()
    if normalized_reason_code not in MANUAL_ADJUSTMENT_REASON_CODES:
        raise ManualAdjustmentValidationError("Reason code is not allowed for manual adjustment.")
    return normalized_reason_code


def _normalize_comment(comment: str) -> str:
    normalized_comment = comment.strip()
    if not normalized_comment:
        raise ManualAdjustmentValidationError("Comment is required for manual adjustment.")
    return normalized_comment


def _normalize_amount(amount: Decimal) -> Decimal:
    normalized_amount = quantize_money(amount)
    if normalized_amount < MANUAL_ADJUSTMENT_MIN_AMOUNT:
        raise ManualAdjustmentValidationError("Manual adjustment amount must be at least 0.01.")
    return normalized_amount


def _calculate_balance_after(balance_before: Decimal, amount: Decimal, direction: str) -> Decimal:
    if direction == MANUAL_ADJUSTMENT_DIRECTION_CREDIT:
        return quantize_money(balance_before + amount)
    if balance_before < amount:
        raise ManualAdjustmentConflictError("Manual debit exceeds the available wallet balance.")
    return quantize_money(balance_before - amount)


def _ensure_actor_is_allowed(
    db: Session,
    tenant_id: str,
    actor_user_id: str | None,
    patient_branch_id: str,
) -> None:
    if actor_user_id is None or not actor_user_id.strip():
        raise ManualAdjustmentPermissionError("Actor user is required for manual adjustment.")

    memberships = db.execute(
        select(UserMembership).where(
            UserMembership.tenant_id == tenant_id,
            UserMembership.user_id == actor_user_id,
            UserMembership.is_active.is_(True),
        )
    ).scalars().all()
    for membership in memberships:
        if membership.role_code not in ALLOWED_MANUAL_ADJUSTMENT_ROLES:
            continue
        if membership.branch_id is None or membership.branch_id == patient_branch_id:
            return
    raise ManualAdjustmentPermissionError("Actor role is not allowed to perform manual adjustments for this patient.")


def _get_currency_code(db: Session, tenant_id: str) -> str:
    return (
        db.execute(select(Tenant.default_currency_code).where(Tenant.id == tenant_id)).scalar_one_or_none()
        or DEFAULT_CURRENCY_CODE
    )


def _build_manual_adjustment_idempotency_key() -> str:
    return f"{MANUAL_ADJUSTMENT_IDEMPOTENCY_PREFIX}:{uuid4()}"


def _append_audit_log(
    db: Session,
    tenant_id: str,
    actor_user_id: str | None,
    wallet_id: str,
    patient_id: str,
    adjustment: LoyaltyManualAdjustment,
    ledger_entry: LoyaltyLedgerEntry,
) -> AuditLog:
    audit_log = AuditLog(
        tenant_id=tenant_id,
        actor_user_id=actor_user_id,
        entity_type=AUDIT_ENTITY_TYPE_PATIENT_WALLET,
        entity_id=wallet_id,
        action=AUDIT_ACTION_MANUAL_ADJUSTMENT_CREATED,
        payload_json={
            "patient_id": patient_id,
            "wallet_id": wallet_id,
            "adjustment_id": adjustment.id,
            "ledger_entry_id": ledger_entry.id,
            "direction": adjustment.direction,
            "amount": str(adjustment.amount),
            "balance_before": str(adjustment.balance_before),
            "balance_after": str(adjustment.balance_after),
            "reason_code": adjustment.reason_code,
            "comment": adjustment.comment,
        },
        created_at=adjustment.applied_at,
    )
    db.add(audit_log)
    return audit_log
