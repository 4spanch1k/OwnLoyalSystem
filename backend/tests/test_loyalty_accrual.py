from datetime import datetime, timezone
from decimal import Decimal
import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db.base import Base
from backend.app.db.models.audit import AuditLog
from backend.app.db.models.loyalty import LoyaltyLedgerEntry, LoyaltyPolicyServiceRule, LoyaltyPolicyVersion, LoyaltyProgram, PatientWallet
from backend.app.db.models.patient import Patient
from backend.app.db.models.payment import Payment, PaymentLine
from backend.app.db.models.tenancy import Branch, Tenant
from backend.app.db.models.visit import Visit
from backend.app.db.session import get_db
from backend.app.main import app

TENANT_ID = "tenant-1"
BRANCH_ID = "branch-1"
PATIENT_ID = "patient-1"
VISIT_ID = "visit-1"
POLICY_ID = "policy-1"
PROGRAM_ID = "program-1"
PAYMENT_ID = "payment-1"
PAYMENT_NUMBER = "pay-001"


class LoyaltyAccrualFlowTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine(
            "sqlite+pysqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.session_factory = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=Session)
        Base.metadata.create_all(self.engine)

        def override_get_db():
            db = self.session_factory()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    def test_confirm_payment_happy_path_creates_accrual_and_updates_wallet(self) -> None:
        self._seed_slice_one_fixture(service_category="therapy")

        response = self.client.post(f"/api/v1/payments/{PAYMENT_ID}/confirm", headers={"X-Tenant-Id": TENANT_ID})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["payment_id"], PAYMENT_ID)
        self.assertEqual(Decimal(str(payload["accrual_amount"])), Decimal("5.00"))
        self.assertFalse(payload["already_processed"])
        self.assertIsNotNone(payload["ledger_entry_id"])

        with self.session_factory() as db:
            wallet = db.execute(
                select(PatientWallet).where(PatientWallet.tenant_id == TENANT_ID, PatientWallet.patient_id == PATIENT_ID)
            ).scalar_one()
            ledger_entries = db.execute(
                select(LoyaltyLedgerEntry).where(LoyaltyLedgerEntry.tenant_id == TENANT_ID, LoyaltyLedgerEntry.payment_id == PAYMENT_ID)
            ).scalars().all()

        self.assertEqual(wallet.available_balance, Decimal("5.00"))
        self.assertEqual(wallet.lifetime_accrued, Decimal("5.00"))
        self.assertEqual(len(ledger_entries), 1)
        self.assertEqual(ledger_entries[0].entry_type, "accrual")

    def test_confirm_payment_is_idempotent(self) -> None:
        self._seed_slice_one_fixture(service_category="therapy")

        first_response = self.client.post(f"/api/v1/payments/{PAYMENT_ID}/confirm", headers={"X-Tenant-Id": TENANT_ID})
        second_response = self.client.post(f"/api/v1/payments/{PAYMENT_ID}/confirm", headers={"X-Tenant-Id": TENANT_ID})

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertTrue(second_response.json()["already_processed"])

        with self.session_factory() as db:
            wallet = db.execute(
                select(PatientWallet).where(PatientWallet.tenant_id == TENANT_ID, PatientWallet.patient_id == PATIENT_ID)
            ).scalar_one()
            ledger_count = db.execute(
                select(LoyaltyLedgerEntry).where(
                    LoyaltyLedgerEntry.tenant_id == TENANT_ID,
                    LoyaltyLedgerEntry.idempotency_key == "payment_confirmed:payment-1:accrual:v1",
                )
            ).scalars().all()

        self.assertEqual(wallet.available_balance, Decimal("5.00"))
        self.assertEqual(len(ledger_count), 1)

    def test_excluded_service_category_skips_accrual(self) -> None:
        self._seed_slice_one_fixture(service_category="implants")

        response = self.client.post(f"/api/v1/payments/{PAYMENT_ID}/confirm", headers={"X-Tenant-Id": TENANT_ID})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(Decimal(str(payload["accrual_amount"])), Decimal("0.00"))
        self.assertIsNone(payload["ledger_entry_id"])

        with self.session_factory() as db:
            wallet = db.execute(
                select(PatientWallet).where(PatientWallet.tenant_id == TENANT_ID, PatientWallet.patient_id == PATIENT_ID)
            ).scalar_one_or_none()
            ledger_entries = db.execute(
                select(LoyaltyLedgerEntry).where(LoyaltyLedgerEntry.tenant_id == TENANT_ID, LoyaltyLedgerEntry.payment_id == PAYMENT_ID)
            ).scalars().all()
            audit_logs = db.execute(
                select(AuditLog).where(AuditLog.tenant_id == TENANT_ID, AuditLog.entity_id == PAYMENT_ID)
            ).scalars().all()

        self.assertIsNone(wallet)
        self.assertEqual(ledger_entries, [])
        self.assertEqual(len(audit_logs), 1)
        self.assertEqual(audit_logs[0].action, "loyalty_accrual_skipped")

    def test_refunded_payment_reprocess_does_not_create_second_accrual(self) -> None:
        self._seed_slice_one_fixture(service_category="therapy")

        initial_response = self.client.post(f"/api/v1/payments/{PAYMENT_ID}/confirm", headers={"X-Tenant-Id": TENANT_ID})
        self.assertEqual(initial_response.status_code, 200)

        with self.session_factory() as db:
            payment = db.execute(select(Payment).where(Payment.tenant_id == TENANT_ID, Payment.id == PAYMENT_ID)).scalar_one()
            payment.status = "refunded"
            payment.refunded_at = datetime.now(timezone.utc)
            db.commit()

        repeated_response = self.client.post(f"/api/v1/payments/{PAYMENT_ID}/confirm", headers={"X-Tenant-Id": TENANT_ID})

        self.assertEqual(repeated_response.status_code, 200)
        self.assertTrue(repeated_response.json()["already_processed"])

        with self.session_factory() as db:
            ledger_entries = db.execute(
                select(LoyaltyLedgerEntry).where(LoyaltyLedgerEntry.tenant_id == TENANT_ID, LoyaltyLedgerEntry.payment_id == PAYMENT_ID)
            ).scalars().all()

        self.assertEqual(len(ledger_entries), 1)

    def test_wallet_and_ledger_reads_are_consistent_after_accrual(self) -> None:
        self._seed_slice_one_fixture(service_category="therapy")
        confirm_response = self.client.post(f"/api/v1/payments/{PAYMENT_ID}/confirm", headers={"X-Tenant-Id": TENANT_ID})
        self.assertEqual(confirm_response.status_code, 200)

        wallet_response = self.client.get(f"/api/v1/patients/{PATIENT_ID}/wallet", headers={"X-Tenant-Id": TENANT_ID})
        ledger_response = self.client.get(f"/api/v1/patients/{PATIENT_ID}/ledger", headers={"X-Tenant-Id": TENANT_ID})

        self.assertEqual(wallet_response.status_code, 200)
        self.assertEqual(ledger_response.status_code, 200)

        wallet_payload = wallet_response.json()
        ledger_payload = ledger_response.json()

        self.assertEqual(Decimal(str(wallet_payload["available_balance"])), Decimal("5.00"))
        self.assertEqual(len(ledger_payload["items"]), 1)
        self.assertEqual(ledger_payload["items"][0]["entry_type"], "accrual")
        self.assertEqual(ledger_payload["items"][0]["payment_id"], PAYMENT_ID)
        self.assertEqual(
            Decimal(str(wallet_payload["available_balance"])),
            Decimal(str(ledger_payload["items"][0]["balance_after"])),
        )

    def _seed_slice_one_fixture(self, service_category: str) -> None:
        now = datetime.now(timezone.utc)
        with self.session_factory() as db:
            tenant = Tenant(
                id=TENANT_ID,
                name="Aster Dental",
                slug="aster-dental",
                status="active",
                default_currency_code="KZT",
                timezone="Asia/Almaty",
                created_at=now,
                updated_at=now,
            )
            branch = Branch(
                id=BRANCH_ID,
                tenant_id=TENANT_ID,
                name="Main Branch",
                code="main",
                is_active=True,
                created_at=now,
                updated_at=now,
            )
            patient = Patient(
                id=PATIENT_ID,
                tenant_id=TENANT_ID,
                branch_id=BRANCH_ID,
                first_name="Aruzhan",
                last_name="Test",
                phone="+77000000000",
                status="active",
                created_at=now,
                updated_at=now,
            )
            visit = Visit(
                id=VISIT_ID,
                tenant_id=TENANT_ID,
                branch_id=BRANCH_ID,
                patient_id=PATIENT_ID,
                status="scheduled",
                created_at=now,
                updated_at=now,
            )
            payment = Payment(
                id=PAYMENT_ID,
                tenant_id=TENANT_ID,
                branch_id=BRANCH_ID,
                patient_id=PATIENT_ID,
                visit_id=VISIT_ID,
                payment_number=PAYMENT_NUMBER,
                status="pending",
                currency="KZT",
                total_amount=Decimal("100.00"),
                created_at=now,
                updated_at=now,
            )
            payment_line = PaymentLine(
                id="payment-line-1",
                tenant_id=TENANT_ID,
                payment_id=PAYMENT_ID,
                service_code="svc-1",
                service_category=service_category,
                quantity=1,
                unit_price=Decimal("100.00"),
                line_total=Decimal("100.00"),
                created_at=now,
                updated_at=now,
            )
            program = LoyaltyProgram(
                id=PROGRAM_ID,
                tenant_id=TENANT_ID,
                branch_id=None,
                status="active",
                active_policy_version_id=POLICY_ID,
                created_at=now,
                updated_at=now,
            )
            policy = LoyaltyPolicyVersion(
                id=POLICY_ID,
                tenant_id=TENANT_ID,
                program_id=PROGRAM_ID,
                version=1,
                accrual_rate_bps=500,
                redemption_cap_bps=2000,
                bonus_ttl_days=180,
                is_active=True,
                effective_from=now,
                created_at=now,
            )
            excluded_rule = LoyaltyPolicyServiceRule(
                id="rule-implants",
                tenant_id=TENANT_ID,
                policy_version_id=POLICY_ID,
                service_category="implants",
                accrual_allowed=False,
                redemption_allowed=False,
                created_at=now,
            )

            db.add_all([tenant, branch, patient, visit, payment, payment_line, program, policy, excluded_rule])
            db.commit()


if __name__ == "__main__":
    unittest.main()
