from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.db.base import ZERO_MONEY, utc_now
from backend.app.db.models.audit import AuditLog
from backend.app.db.models.loyalty import (
    LoyaltyLedgerEntry,
    LoyaltyPolicyServiceRule,
    LoyaltyPolicyVersion,
    LoyaltyProgram,
    PatientWallet,
)
from backend.app.db.models.patient import Patient
from backend.app.db.models.payment import Payment, PaymentLine
from backend.app.db.models.rbac import User, UserMembership
from backend.app.db.models.tenancy import Branch, Tenant
from backend.app.db.models.visit import Visit
from backend.app.db.session import create_session

TENANT_ID = "tenant-manual-adjustment"
BRANCH_ID = "branch-manual-adjustment"
OWNER_USER_ID = "user-owner"
MANAGER_USER_ID = "user-clinic-manager"
DOCTOR_USER_ID = "user-doctor-demo"
PATIENT_ID = "patient-manual-adjustment"
VISIT_ID = "visit-demo-1"
PROGRAM_ID = "program-demo-1"
POLICY_ID = "policy-demo-1"
RULE_ID = "rule-demo-implants"
WALLET_ID = "wallet-manual-adjustment"
PAYMENT_ID = "payment-demo-1"
PAYMENT_LINE_ID = "payment-line-demo-1"
ACCRUAL_LEDGER_ENTRY_ID = "ledger-accrual-demo-1"

TENANT_SLUG = "aster-dental-manual-adjustment"
BRANCH_CODE = "main-demo"
PAYMENT_NUMBER = "payment-demo-001"
CANONICAL_CURRENCY_CODE = "KZT"
EXPECTED_BALANCE = Decimal("5.00")
EXPECTED_LEDGER_ENTRY_COUNT = 1
EXPECTED_POLICY_VERSION = 1
EXPECTED_ACCRUAL_RATE_BPS = 500
EXPECTED_REDEMPTION_CAP_BPS = 2000
EXPECTED_BONUS_TTL_DAYS = 180
EXPECTED_PAYMENT_TOTAL = Decimal("100.00")
EXPECTED_ACCRUAL_AMOUNT = Decimal("5.00")


class SeedConflictError(RuntimeError):
    """Raised when the current database state conflicts with the canonical demo dataset."""


@dataclass(frozen=True)
class DemoSeedSummary:
    tenant_id: str
    patient_id: str
    clinic_manager_user_id: str
    payment_id: str
    wallet_balance: Decimal
    ledger_entry_count: int
    ready_for_demo: bool


def seed_demo_dataset(db: Session) -> DemoSeedSummary:
    now = utc_now()

    with db.begin():
        _ensure_tenant(db, now)
        _ensure_branch(db, now)
        _ensure_users_and_memberships(db, now)
        _ensure_patient(db, now)
        _ensure_visit(db, now)
        _ensure_program(db, now)
        _ensure_policy(db, now)
        _ensure_policy_rule(db, now)
        _assert_demo_patient_is_not_dirty(db)
        _ensure_wallet(db, now)
        _ensure_payment(db, now)
        _ensure_payment_line(db, now)
        _ensure_seeded_accrual_entry(db, now)

    return validate_demo_dataset(db)


def validate_demo_dataset(db: Session) -> DemoSeedSummary:
    tenant = db.get(Tenant, TENANT_ID)
    patient = db.get(Patient, PATIENT_ID)
    payment = db.get(Payment, PAYMENT_ID)
    wallet = db.get(PatientWallet, WALLET_ID)
    program = db.get(LoyaltyProgram, PROGRAM_ID)
    policy = db.get(LoyaltyPolicyVersion, POLICY_ID)
    accrual_entry = db.get(LoyaltyLedgerEntry, ACCRUAL_LEDGER_ENTRY_ID)

    manager_membership = db.execute(
        select(UserMembership).where(
            UserMembership.tenant_id == TENANT_ID,
            UserMembership.user_id == MANAGER_USER_ID,
            UserMembership.role_code == "clinic_manager",
            UserMembership.is_active.is_(True),
        )
    ).scalar_one_or_none()

    latest_ledger_entry = db.execute(
        select(LoyaltyLedgerEntry)
        .where(
            LoyaltyLedgerEntry.tenant_id == TENANT_ID,
            LoyaltyLedgerEntry.patient_id == PATIENT_ID,
        )
        .order_by(LoyaltyLedgerEntry.created_at.desc(), LoyaltyLedgerEntry.id.desc())
    ).scalars().first()

    ledger_entry_count = db.execute(
        select(func.count()).select_from(LoyaltyLedgerEntry).where(
            LoyaltyLedgerEntry.tenant_id == TENANT_ID,
            LoyaltyLedgerEntry.patient_id == PATIENT_ID,
        )
    ).scalar_one()

    ready_for_demo = all(
        [
            tenant is not None,
            patient is not None,
            payment is not None,
            wallet is not None,
            program is not None,
            policy is not None,
            manager_membership is not None,
            accrual_entry is not None,
            program.active_policy_version_id == POLICY_ID if program else False,
            wallet.available_balance == EXPECTED_BALANCE if wallet else False,
            wallet.lifetime_accrued == EXPECTED_BALANCE if wallet else False,
            ledger_entry_count == EXPECTED_LEDGER_ENTRY_COUNT,
            latest_ledger_entry is not None,
            latest_ledger_entry.balance_after == EXPECTED_BALANCE if latest_ledger_entry else False,
            latest_ledger_entry.id == ACCRUAL_LEDGER_ENTRY_ID if latest_ledger_entry else False,
        ]
    )

    return DemoSeedSummary(
        tenant_id=TENANT_ID,
        patient_id=PATIENT_ID,
        clinic_manager_user_id=MANAGER_USER_ID,
        payment_id=PAYMENT_ID,
        wallet_balance=wallet.available_balance if wallet else ZERO_MONEY,
        ledger_entry_count=int(ledger_entry_count),
        ready_for_demo=ready_for_demo,
    )


def main() -> int:
    db = create_session()
    try:
        summary = seed_demo_dataset(db)
        _print_summary(summary)
        if not summary.ready_for_demo:
            raise SeedConflictError("Canonical loyalty demo dataset was seeded, but final validation did not pass.")
        return 0
    except SeedConflictError as error:
        print(f"[seed_loyalty_demo] conflict: {error}", file=sys.stderr)
        return 1
    except Exception as error:  # noqa: BLE001
        print(f"[seed_loyalty_demo] failed: {error}", file=sys.stderr)
        return 1
    finally:
        db.close()


def _ensure_tenant(db: Session, now: datetime) -> Tenant:
    _assert_unique_conflict(
        db=db,
        existing_id=TENANT_ID,
        description="tenant slug",
        statement=select(Tenant.id).where(Tenant.slug == TENANT_SLUG),
    )
    tenant = db.get(Tenant, TENANT_ID)
    if tenant is None:
        tenant = Tenant(
            id=TENANT_ID,
            name="Aster Dental",
            slug=TENANT_SLUG,
            status="active",
            default_currency_code=CANONICAL_CURRENCY_CODE,
            timezone="Asia/Almaty",
            created_at=now,
            updated_at=now,
        )
        db.add(tenant)
        return tenant

    tenant.name = "Aster Dental"
    tenant.slug = TENANT_SLUG
    tenant.status = "active"
    tenant.default_currency_code = CANONICAL_CURRENCY_CODE
    tenant.timezone = "Asia/Almaty"
    tenant.updated_at = now
    return tenant


def _ensure_branch(db: Session, now: datetime) -> Branch:
    _assert_unique_conflict(
        db=db,
        existing_id=BRANCH_ID,
        description="branch code",
        statement=select(Branch.id).where(
            Branch.tenant_id == TENANT_ID,
            Branch.code == BRANCH_CODE,
        ),
    )
    branch = db.get(Branch, BRANCH_ID)
    if branch is None:
        branch = Branch(
            id=BRANCH_ID,
            tenant_id=TENANT_ID,
            name="Main Demo Branch",
            code=BRANCH_CODE,
            address_line="Abylai Khan Ave 51, Almaty",
            phone="+7 (727) 555-01-01",
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        db.add(branch)
        return branch

    branch.tenant_id = TENANT_ID
    branch.name = "Main Demo Branch"
    branch.code = BRANCH_CODE
    branch.address_line = "Abylai Khan Ave 51, Almaty"
    branch.phone = "+7 (727) 555-01-01"
    branch.is_active = True
    branch.updated_at = now
    return branch


def _ensure_users_and_memberships(db: Session, now: datetime) -> None:
    for user_id, email, full_name, role_code in (
        (OWNER_USER_ID, "owner@example.com", "Aster Demo Owner", "owner"),
        (MANAGER_USER_ID, "manager@example.com", "Aster Demo Manager", "clinic_manager"),
        (DOCTOR_USER_ID, "doctor@example.com", "Aster Demo Doctor", "doctor"),
    ):
        _assert_unique_conflict(
            db=db,
            existing_id=user_id,
            description=f"user email {email}",
            statement=select(User.id).where(
                User.tenant_id == TENANT_ID,
                User.email == email,
            ),
        )
        user = db.get(User, user_id)
        if user is None:
            user = User(
                id=user_id,
                tenant_id=TENANT_ID,
                email=email,
                password_hash="seeded-demo-password-hash",
                full_name=full_name,
                status="active",
                created_at=now,
                updated_at=now,
            )
            db.add(user)
        else:
            user.tenant_id = TENANT_ID
            user.email = email
            user.password_hash = "seeded-demo-password-hash"
            user.full_name = full_name
            user.status = "active"
            user.updated_at = now

        membership_id = f"membership-{user_id}"
        membership = db.get(UserMembership, membership_id)
        if membership is None:
            membership = UserMembership(
                id=membership_id,
                tenant_id=TENANT_ID,
                user_id=user_id,
                branch_id=None,
                role_code=role_code,
                is_active=True,
                created_at=now,
                updated_at=now,
            )
            db.add(membership)
        else:
            membership.tenant_id = TENANT_ID
            membership.user_id = user_id
            membership.branch_id = None
            membership.role_code = role_code
            membership.is_active = True
            membership.updated_at = now


def _ensure_patient(db: Session, now: datetime) -> Patient:
    patient = db.get(Patient, PATIENT_ID)
    if patient is None:
        patient = Patient(
            id=PATIENT_ID,
            tenant_id=TENANT_ID,
            branch_id=BRANCH_ID,
            external_patient_code="DEMO-001",
            first_name="Aruzhan",
            last_name="Patient",
            phone="+77000000011",
            email="aruzhan.demo@asterdental.kz",
            status="active",
            created_at=now,
            updated_at=now,
        )
        db.add(patient)
        return patient

    patient.tenant_id = TENANT_ID
    patient.branch_id = BRANCH_ID
    patient.external_patient_code = "DEMO-001"
    patient.first_name = "Aruzhan"
    patient.last_name = "Patient"
    patient.phone = "+77000000011"
    patient.email = "aruzhan.demo@asterdental.kz"
    patient.status = "active"
    patient.updated_at = now
    return patient


def _ensure_visit(db: Session, now: datetime) -> Visit:
    visit = db.get(Visit, VISIT_ID)
    if visit is None:
        visit = Visit(
            id=VISIT_ID,
            tenant_id=TENANT_ID,
            branch_id=BRANCH_ID,
            patient_id=PATIENT_ID,
            doctor_user_id=DOCTOR_USER_ID,
            appointment_id=None,
            visit_number="VISIT-DEMO-001",
            status="completed",
            scheduled_at=now,
            completed_at=now,
            cancelled_at=None,
            created_at=now,
            updated_at=now,
        )
        db.add(visit)
        return visit

    visit.tenant_id = TENANT_ID
    visit.branch_id = BRANCH_ID
    visit.patient_id = PATIENT_ID
    visit.doctor_user_id = DOCTOR_USER_ID
    visit.appointment_id = None
    visit.visit_number = "VISIT-DEMO-001"
    visit.status = "completed"
    visit.scheduled_at = now
    visit.completed_at = now
    visit.cancelled_at = None
    visit.updated_at = now
    return visit


def _ensure_program(db: Session, now: datetime) -> LoyaltyProgram:
    program = db.get(LoyaltyProgram, PROGRAM_ID)
    if program is None:
        program = LoyaltyProgram(
            id=PROGRAM_ID,
            tenant_id=TENANT_ID,
            branch_id=None,
            status="active",
            active_policy_version_id=POLICY_ID,
            created_at=now,
            updated_at=now,
        )
        db.add(program)
        return program

    program.tenant_id = TENANT_ID
    program.branch_id = None
    program.status = "active"
    program.active_policy_version_id = POLICY_ID
    program.updated_at = now
    return program


def _ensure_policy(db: Session, now: datetime) -> LoyaltyPolicyVersion:
    policy = db.get(LoyaltyPolicyVersion, POLICY_ID)
    if policy is None:
        policy = LoyaltyPolicyVersion(
            id=POLICY_ID,
            tenant_id=TENANT_ID,
            program_id=PROGRAM_ID,
            version=EXPECTED_POLICY_VERSION,
            accrual_rate_bps=EXPECTED_ACCRUAL_RATE_BPS,
            redemption_cap_bps=EXPECTED_REDEMPTION_CAP_BPS,
            bonus_ttl_days=EXPECTED_BONUS_TTL_DAYS,
            is_active=True,
            effective_from=now,
            effective_to=None,
            created_at=now,
        )
        db.add(policy)
        return policy

    policy.tenant_id = TENANT_ID
    policy.program_id = PROGRAM_ID
    policy.version = EXPECTED_POLICY_VERSION
    policy.accrual_rate_bps = EXPECTED_ACCRUAL_RATE_BPS
    policy.redemption_cap_bps = EXPECTED_REDEMPTION_CAP_BPS
    policy.bonus_ttl_days = EXPECTED_BONUS_TTL_DAYS
    policy.is_active = True
    policy.effective_from = now
    policy.effective_to = None
    return policy


def _ensure_policy_rule(db: Session, now: datetime) -> LoyaltyPolicyServiceRule:
    rule = db.get(LoyaltyPolicyServiceRule, RULE_ID)
    if rule is None:
        rule = LoyaltyPolicyServiceRule(
            id=RULE_ID,
            tenant_id=TENANT_ID,
            policy_version_id=POLICY_ID,
            service_category="implants",
            accrual_allowed=False,
            redemption_allowed=False,
            created_at=now,
        )
        db.add(rule)
        return rule

    rule.tenant_id = TENANT_ID
    rule.policy_version_id = POLICY_ID
    rule.service_category = "implants"
    rule.accrual_allowed = False
    rule.redemption_allowed = False
    return rule


def _ensure_wallet(db: Session, now: datetime) -> PatientWallet:
    wallet = db.get(PatientWallet, WALLET_ID)
    if wallet is None:
        wallet = PatientWallet(
            id=WALLET_ID,
            tenant_id=TENANT_ID,
            patient_id=PATIENT_ID,
            available_balance=EXPECTED_BALANCE,
            lifetime_accrued=EXPECTED_BALANCE,
            lifetime_redeemed=ZERO_MONEY,
            lifetime_expired=ZERO_MONEY,
            updated_at=now,
        )
        db.add(wallet)
        return wallet

    wallet.tenant_id = TENANT_ID
    wallet.patient_id = PATIENT_ID
    wallet.available_balance = EXPECTED_BALANCE
    wallet.lifetime_accrued = EXPECTED_BALANCE
    wallet.lifetime_redeemed = ZERO_MONEY
    wallet.lifetime_expired = ZERO_MONEY
    wallet.updated_at = now
    return wallet


def _ensure_payment(db: Session, now: datetime) -> Payment:
    _assert_unique_conflict(
        db=db,
        existing_id=PAYMENT_ID,
        description="payment number",
        statement=select(Payment.id).where(
            Payment.tenant_id == TENANT_ID,
            Payment.payment_number == PAYMENT_NUMBER,
        ),
    )
    payment = db.get(Payment, PAYMENT_ID)
    if payment is None:
        payment = Payment(
            id=PAYMENT_ID,
            tenant_id=TENANT_ID,
            branch_id=BRANCH_ID,
            patient_id=PATIENT_ID,
            visit_id=VISIT_ID,
            payment_number=PAYMENT_NUMBER,
            status="confirmed",
            currency=CANONICAL_CURRENCY_CODE,
            total_amount=EXPECTED_PAYMENT_TOTAL,
            refunded_amount=ZERO_MONEY,
            confirmed_at=now,
            refunded_at=None,
            created_at=now,
            updated_at=now,
        )
        db.add(payment)
        return payment

    payment.tenant_id = TENANT_ID
    payment.branch_id = BRANCH_ID
    payment.patient_id = PATIENT_ID
    payment.visit_id = VISIT_ID
    payment.payment_number = PAYMENT_NUMBER
    payment.status = "confirmed"
    payment.currency = CANONICAL_CURRENCY_CODE
    payment.total_amount = EXPECTED_PAYMENT_TOTAL
    payment.refunded_amount = ZERO_MONEY
    payment.confirmed_at = now
    payment.refunded_at = None
    payment.updated_at = now
    return payment


def _ensure_payment_line(db: Session, now: datetime) -> PaymentLine:
    payment_line = db.get(PaymentLine, PAYMENT_LINE_ID)
    if payment_line is None:
        payment_line = PaymentLine(
            id=PAYMENT_LINE_ID,
            tenant_id=TENANT_ID,
            payment_id=PAYMENT_ID,
            service_code="svc-demo-therapy-1",
            service_category="therapy",
            quantity=1,
            unit_price=EXPECTED_PAYMENT_TOTAL,
            line_total=EXPECTED_PAYMENT_TOTAL,
            created_at=now,
            updated_at=now,
        )
        db.add(payment_line)
        return payment_line

    payment_line.tenant_id = TENANT_ID
    payment_line.payment_id = PAYMENT_ID
    payment_line.service_code = "svc-demo-therapy-1"
    payment_line.service_category = "therapy"
    payment_line.quantity = 1
    payment_line.unit_price = EXPECTED_PAYMENT_TOTAL
    payment_line.line_total = EXPECTED_PAYMENT_TOTAL
    payment_line.updated_at = now
    return payment_line


def _ensure_seeded_accrual_entry(db: Session, now: datetime) -> LoyaltyLedgerEntry:
    ledger_entry = db.get(LoyaltyLedgerEntry, ACCRUAL_LEDGER_ENTRY_ID)
    if ledger_entry is None:
        ledger_entry = LoyaltyLedgerEntry(
            id=ACCRUAL_LEDGER_ENTRY_ID,
            tenant_id=TENANT_ID,
            patient_id=PATIENT_ID,
            wallet_id=WALLET_ID,
            payment_id=PAYMENT_ID,
            payment_line_id=PAYMENT_LINE_ID,
            entry_type="accrual",
            amount=EXPECTED_ACCRUAL_AMOUNT,
            balance_after=EXPECTED_BALANCE,
            currency=CANONICAL_CURRENCY_CODE,
            status="posted",
            policy_version_id=POLICY_ID,
            idempotency_key="payment_confirmed:payment-demo-1:accrual:v1",
            reason_code="payment_confirmed",
            metadata_json={"seeded_by": "seed_loyalty_demo"},
            created_at=now,
        )
        db.add(ledger_entry)
        return ledger_entry

    ledger_entry.tenant_id = TENANT_ID
    ledger_entry.patient_id = PATIENT_ID
    ledger_entry.wallet_id = WALLET_ID
    ledger_entry.payment_id = PAYMENT_ID
    ledger_entry.payment_line_id = PAYMENT_LINE_ID
    ledger_entry.entry_type = "accrual"
    ledger_entry.amount = EXPECTED_ACCRUAL_AMOUNT
    ledger_entry.balance_after = EXPECTED_BALANCE
    ledger_entry.currency = CANONICAL_CURRENCY_CODE
    ledger_entry.status = "posted"
    ledger_entry.policy_version_id = POLICY_ID
    ledger_entry.idempotency_key = "payment_confirmed:payment-demo-1:accrual:v1"
    ledger_entry.reason_code = "payment_confirmed"
    ledger_entry.metadata_json = {"seeded_by": "seed_loyalty_demo"}
    ledger_entry.created_at = now
    return ledger_entry


def _assert_demo_patient_is_not_dirty(db: Session) -> None:
    existing_patient = db.get(Patient, PATIENT_ID)
    if existing_patient is None:
        return

    extra_ledger_ids = db.execute(
        select(LoyaltyLedgerEntry.id).where(
            LoyaltyLedgerEntry.tenant_id == TENANT_ID,
            LoyaltyLedgerEntry.patient_id == PATIENT_ID,
            LoyaltyLedgerEntry.id != ACCRUAL_LEDGER_ENTRY_ID,
        )
    ).scalars().all()
    if extra_ledger_ids:
        raise SeedConflictError(
            "Demo patient already has non-canonical loyalty history. "
            "Reset is not supported yet; use a clean database or remove demo drift first."
        )

    extra_audit_ids = db.execute(
        select(AuditLog.id).where(
            AuditLog.tenant_id == TENANT_ID,
            AuditLog.entity_id == PATIENT_ID,
            AuditLog.entity_type == "patient_wallet",
        )
    ).scalars().all()
    if extra_audit_ids:
        raise SeedConflictError(
            "Demo patient already has audit activity in the canonical dataset. "
            "Reset is not supported yet; use a clean database or remove demo drift first."
        )


def _assert_unique_conflict(db: Session, statement, existing_id: str, description: str) -> None:
    conflict_id = db.execute(statement).scalar_one_or_none()
    if conflict_id is not None and conflict_id != existing_id:
        raise SeedConflictError(
            f"Found conflicting {description}: expected id {existing_id}, but database already contains id {conflict_id}."
        )


def _print_summary(summary: DemoSeedSummary) -> None:
    print("[seed_loyalty_demo] summary")
    print(f"tenant id: {summary.tenant_id}")
    print(f"patient id: {summary.patient_id}")
    print(f"clinic_manager id: {summary.clinic_manager_user_id}")
    print(f"payment id: {summary.payment_id}")
    print(f"wallet balance: {summary.wallet_balance}")
    print(f"ledger entry count: {summary.ledger_entry_count}")
    print(f"ready for demo: {'yes' if summary.ready_for_demo else 'no'}")


if __name__ == "__main__":
    raise SystemExit(main())
