from datetime import datetime, timezone
from decimal import Decimal
import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db.base import Base
from backend.app.db.models.loyalty import LoyaltyLedgerEntry, LoyaltyPolicyServiceRule, LoyaltyPolicyVersion, LoyaltyProgram, PatientWallet
from backend.app.db.models.patient import Patient
from backend.app.db.models.payment import Payment, PaymentLine
from backend.app.db.models.tenancy import Branch, Tenant
from backend.app.db.models.visit import Visit
from backend.app.db.session import get_db
from backend.app.main import app

TENANT_ID = "tenant-rollback"
BRANCH_ID = "branch-rollback"
PATIENT_ID = "patient-rollback"
VISIT_ID = "visit-rollback"
POLICY_ID = "policy-rollback"
PROGRAM_ID = "program-rollback"
PAYMENT_ID = "payment-rollback"


class LoyaltyRollbackFlowTestCase(unittest.TestCase):
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

    def test_full_refund_creates_full_rollback(self) -> None:
        self._seed_fixture()
        self._confirm_payment()

        response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/refund",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"refunded_amount": "100.00", "refund_marker": "full-1", "reason": "full refund"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(Decimal(str(payload["rollback_amount"])), Decimal("5.00"))
        self.assertEqual(Decimal(str(payload["wallet_balance_after"])), Decimal("0.00"))
        self.assertEqual(payload["status"], "refunded")

        with self.session_factory() as db:
            rollback_entries = db.execute(
                select(LoyaltyLedgerEntry).where(
                    LoyaltyLedgerEntry.tenant_id == TENANT_ID,
                    LoyaltyLedgerEntry.payment_id == PAYMENT_ID,
                    LoyaltyLedgerEntry.entry_type == "rollback",
                )
            ).scalars().all()
            wallet = db.execute(
                select(PatientWallet).where(PatientWallet.tenant_id == TENANT_ID, PatientWallet.patient_id == PATIENT_ID)
            ).scalar_one()

        self.assertEqual(len(rollback_entries), 1)
        self.assertEqual(wallet.available_balance, Decimal("0.00"))

    def test_partial_refund_creates_proportional_rollback(self) -> None:
        self._seed_fixture()
        self._confirm_payment()

        response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/refund",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"refunded_amount": "50.00", "refund_marker": "partial-1", "reason": "partial refund"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(Decimal(str(payload["rollback_amount"])), Decimal("2.50"))
        self.assertEqual(payload["status"], "partially_refunded")

    def test_refund_handling_is_idempotent_per_refund_marker(self) -> None:
        self._seed_fixture()
        self._confirm_payment()

        first_response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/refund",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"refunded_amount": "100.00", "refund_marker": "same-marker", "reason": "duplicate"},
        )
        second_response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/refund",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"refunded_amount": "100.00", "refund_marker": "same-marker", "reason": "duplicate"},
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertTrue(second_response.json()["already_processed"])

        with self.session_factory() as db:
            rollback_entries = db.execute(
                select(LoyaltyLedgerEntry).where(
                    LoyaltyLedgerEntry.tenant_id == TENANT_ID,
                    LoyaltyLedgerEntry.payment_id == PAYMENT_ID,
                    LoyaltyLedgerEntry.entry_type == "rollback",
                )
            ).scalars().all()

        self.assertEqual(len(rollback_entries), 1)

    def test_cumulative_partial_refunds_only_apply_delta(self) -> None:
        self._seed_fixture()
        self._confirm_payment()

        first_response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/refund",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"refunded_amount": "30.00", "refund_marker": "partial-30", "reason": "30 percent"},
        )
        second_response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/refund",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"refunded_amount": "60.00", "refund_marker": "partial-60", "reason": "60 percent total"},
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(Decimal(str(first_response.json()["rollback_amount"])), Decimal("1.50"))
        self.assertEqual(Decimal(str(second_response.json()["rollback_amount"])), Decimal("1.50"))

        with self.session_factory() as db:
            rollback_total = sum(
                (
                    entry.amount
                    for entry in db.execute(
                        select(LoyaltyLedgerEntry).where(
                            LoyaltyLedgerEntry.tenant_id == TENANT_ID,
                            LoyaltyLedgerEntry.payment_id == PAYMENT_ID,
                            LoyaltyLedgerEntry.entry_type == "rollback",
                        )
                    ).scalars()
                ),
                Decimal("0.00"),
            )

        self.assertEqual(rollback_total, Decimal("3.00"))

    def test_wallet_and_ledger_stay_consistent_after_rollback(self) -> None:
        self._seed_fixture()
        self._confirm_payment()

        refund_response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/refund",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"refunded_amount": "50.00", "refund_marker": "consistency", "reason": "consistency"},
        )
        self.assertEqual(refund_response.status_code, 200)

        wallet_response = self.client.get(f"/api/v1/patients/{PATIENT_ID}/wallet", headers={"X-Tenant-Id": TENANT_ID})
        ledger_response = self.client.get(f"/api/v1/patients/{PATIENT_ID}/ledger", headers={"X-Tenant-Id": TENANT_ID})

        self.assertEqual(wallet_response.status_code, 200)
        self.assertEqual(ledger_response.status_code, 200)

        wallet_payload = wallet_response.json()
        ledger_payload = ledger_response.json()
        last_entry = ledger_payload["items"][0]

        self.assertEqual(last_entry["entry_type"], "rollback")
        self.assertEqual(Decimal(str(wallet_payload["available_balance"])), Decimal(str(last_entry["balance_after"])))
        self.assertEqual(Decimal(str(wallet_payload["available_balance"])), Decimal("2.50"))

    def test_refund_without_accrual_creates_no_rollback(self) -> None:
        self._seed_fixture()

        response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/refund",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"refunded_amount": "100.00", "refund_marker": "no-accrual", "reason": "no accrual"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(Decimal(str(payload["rollback_amount"])), Decimal("0.00"))
        self.assertIsNone(payload["ledger_entry_id"])

        with self.session_factory() as db:
            rollback_entries = db.execute(
                select(LoyaltyLedgerEntry).where(
                    LoyaltyLedgerEntry.tenant_id == TENANT_ID,
                    LoyaltyLedgerEntry.payment_id == PAYMENT_ID,
                    LoyaltyLedgerEntry.entry_type == "rollback",
                )
            ).scalars().all()

        self.assertEqual(rollback_entries, [])

    def test_refund_rejects_when_refunded_amount_exceeds_payment_total(self) -> None:
        self._seed_fixture()
        self._confirm_payment()

        response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/refund",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"refunded_amount": "150.00", "refund_marker": "over", "reason": "too much"},
        )

        self.assertEqual(response.status_code, 409)

    def test_refund_rejects_when_accrual_effect_is_already_spent(self) -> None:
        self._seed_fixture()
        self._confirm_payment()

        with self.session_factory() as db:
            wallet = db.execute(
                select(PatientWallet).where(PatientWallet.tenant_id == TENANT_ID, PatientWallet.patient_id == PATIENT_ID)
            ).scalar_one()
            wallet.available_balance = Decimal("0.00")
            db.commit()

        response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/refund",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"refunded_amount": "100.00", "refund_marker": "spent", "reason": "spent elsewhere"},
        )

        self.assertEqual(response.status_code, 409)

    def _confirm_payment(self) -> None:
        response = self.client.post(f"/api/v1/payments/{PAYMENT_ID}/confirm", headers={"X-Tenant-Id": TENANT_ID})
        self.assertEqual(response.status_code, 200)

    def _seed_fixture(self) -> None:
        now = datetime.now(timezone.utc)
        with self.session_factory() as db:
            tenant = Tenant(
                id=TENANT_ID,
                name="Aster Dental",
                slug="aster-dental-rollback",
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
                first_name="Aliya",
                last_name="Rollback",
                phone="+77000000002",
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
                payment_number="payment-rollback-001",
                status="pending",
                currency="KZT",
                total_amount=Decimal("100.00"),
                created_at=now,
                updated_at=now,
            )
            payment_line = PaymentLine(
                id="payment-rollback-line-1",
                tenant_id=TENANT_ID,
                payment_id=PAYMENT_ID,
                service_code="svc-rollback-1",
                service_category="therapy",
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
                id="rule-rollback-implants",
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
