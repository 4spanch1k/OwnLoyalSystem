from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal
import os
from tempfile import NamedTemporaryFile
import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db.base import Base
from backend.app.db.models.loyalty import LoyaltyLedgerEntry, LoyaltyPolicyServiceRule, LoyaltyPolicyVersion, LoyaltyProgram, PatientWallet
from backend.app.db.models.loyalty_redemption import LoyaltyRedemption
from backend.app.db.models.patient import Patient
from backend.app.db.models.payment import Payment, PaymentLine
from backend.app.db.models.tenancy import Branch, Tenant
from backend.app.db.models.visit import Visit
from backend.app.db.session import get_db
from backend.app.main import app
from backend.app.services.loyalty.errors import RedemptionConflictError
from backend.app.services.loyalty.redemption import apply_redemption

TENANT_ID = "tenant-redemption"
BRANCH_ID = "branch-redemption"
PATIENT_ID = "patient-redemption"
VISIT_ID = "visit-redemption"
POLICY_ID = "policy-redemption"
PROGRAM_ID = "program-redemption"
PAYMENT_ID = "payment-redemption"


class LoyaltyRedemptionFlowTestCase(unittest.TestCase):
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

    def test_redemption_quote_and_apply_respect_cap(self) -> None:
        self._seed_redemption_fixture(wallet_balance=Decimal("100.00"), eligible_total=Decimal("100.00"))

        quote_response = self.client.post(f"/api/v1/payments/{PAYMENT_ID}/redemption/quote", headers={"X-Tenant-Id": TENANT_ID})
        self.assertEqual(quote_response.status_code, 200)
        self.assertEqual(Decimal(str(quote_response.json()["cap_amount"])), Decimal("20.00"))
        self.assertEqual(Decimal(str(quote_response.json()["max_redeemable"])), Decimal("20.00"))

        apply_response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/redemptions",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"requested_amount": "25.00", "client_request_id": "cap-over"},
        )
        self.assertEqual(apply_response.status_code, 409)

        success_response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/redemptions",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"requested_amount": "20.00", "client_request_id": "cap-ok"},
        )
        self.assertEqual(success_response.status_code, 200)
        self.assertEqual(Decimal(str(success_response.json()["approved_amount"])), Decimal("20.00"))

    def test_redemption_quote_is_limited_by_wallet_balance(self) -> None:
        self._seed_redemption_fixture(wallet_balance=Decimal("10.00"), eligible_total=Decimal("100.00"))

        quote_response = self.client.post(f"/api/v1/payments/{PAYMENT_ID}/redemption/quote", headers={"X-Tenant-Id": TENANT_ID})

        self.assertEqual(quote_response.status_code, 200)
        payload = quote_response.json()
        self.assertEqual(Decimal(str(payload["cap_amount"])), Decimal("20.00"))
        self.assertEqual(Decimal(str(payload["wallet_available"])), Decimal("10.00"))
        self.assertEqual(Decimal(str(payload["max_redeemable"])), Decimal("10.00"))

    def test_denied_categories_block_quote_and_apply(self) -> None:
        self._seed_redemption_fixture(wallet_balance=Decimal("50.00"), eligible_total=Decimal("100.00"), service_category="implants")

        quote_response = self.client.post(f"/api/v1/payments/{PAYMENT_ID}/redemption/quote", headers={"X-Tenant-Id": TENANT_ID})
        self.assertEqual(quote_response.status_code, 200)
        payload = quote_response.json()
        self.assertEqual(Decimal(str(payload["eligible_subtotal"])), Decimal("0.00"))
        self.assertEqual(Decimal(str(payload["max_redeemable"])), Decimal("0.00"))
        self.assertEqual(payload["denied_categories"], ["implants"])

        apply_response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/redemptions",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"requested_amount": "5.00", "client_request_id": "denied-1"},
        )
        self.assertEqual(apply_response.status_code, 409)

    def test_apply_redemption_is_idempotent(self) -> None:
        self._seed_redemption_fixture(wallet_balance=Decimal("50.00"), eligible_total=Decimal("100.00"))

        first_response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/redemptions",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"requested_amount": "10.00", "client_request_id": "same-request"},
        )
        second_response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/redemptions",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"requested_amount": "10.00", "client_request_id": "same-request"},
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertTrue(second_response.json()["already_processed"])

        with self.session_factory() as db:
            redemptions = db.execute(select(LoyaltyRedemption).where(LoyaltyRedemption.tenant_id == TENANT_ID)).scalars().all()
            ledger_entries = db.execute(
                select(LoyaltyLedgerEntry).where(
                    LoyaltyLedgerEntry.tenant_id == TENANT_ID,
                    LoyaltyLedgerEntry.idempotency_key == first_response.json()["idempotency_key"],
                )
            ).scalars().all()
            wallet = db.execute(
                select(PatientWallet).where(PatientWallet.tenant_id == TENANT_ID, PatientWallet.patient_id == PATIENT_ID)
            ).scalar_one()

        self.assertEqual(len(redemptions), 1)
        self.assertEqual(len(ledger_entries), 1)
        self.assertEqual(wallet.available_balance, Decimal("40.00"))

    def test_wallet_and_ledger_stay_consistent_after_redemption_apply(self) -> None:
        self._seed_redemption_fixture(wallet_balance=Decimal("50.00"), eligible_total=Decimal("100.00"))

        apply_response = self.client.post(
            f"/api/v1/payments/{PAYMENT_ID}/redemptions",
            headers={"X-Tenant-Id": TENANT_ID},
            json={"requested_amount": "12.50", "client_request_id": "consistency"},
        )
        self.assertEqual(apply_response.status_code, 200)

        wallet_response = self.client.get(f"/api/v1/patients/{PATIENT_ID}/wallet", headers={"X-Tenant-Id": TENANT_ID})
        ledger_response = self.client.get(f"/api/v1/patients/{PATIENT_ID}/ledger", headers={"X-Tenant-Id": TENANT_ID})

        self.assertEqual(wallet_response.status_code, 200)
        self.assertEqual(ledger_response.status_code, 200)

        wallet_payload = wallet_response.json()
        ledger_payload = ledger_response.json()
        last_entry = ledger_payload["items"][0]

        self.assertEqual(Decimal(str(wallet_payload["available_balance"])), Decimal("37.50"))
        self.assertEqual(Decimal(str(wallet_payload["lifetime_redeemed"])), Decimal("12.50"))
        self.assertEqual(last_entry["entry_type"], "redeem")
        self.assertEqual(Decimal(str(last_entry["balance_after"])), Decimal("37.50"))

    def test_concurrency_smoke_allows_only_one_competing_full_redemption(self) -> None:
        temp_db = NamedTemporaryFile(prefix="loyalty-redemption-", suffix=".sqlite", delete=False)
        temp_db.close()
        database_url = f"sqlite+pysqlite:///{temp_db.name}"
        engine = create_engine(database_url, connect_args={"check_same_thread": False, "timeout": 5})
        session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=Session)
        Base.metadata.create_all(engine)

        try:
            self._seed_redemption_fixture(
                wallet_balance=Decimal("10.00"),
                eligible_total=Decimal("100.00"),
                session_factory=session_factory,
            )

            def worker(client_request_id: str) -> str:
                with session_factory() as db:
                    try:
                        apply_redemption(
                            db=db,
                            tenant_id=TENANT_ID,
                            payment_id=PAYMENT_ID,
                            requested_amount=Decimal("10.00"),
                            client_request_id=client_request_id,
                        )
                        return "success"
                    except RedemptionConflictError:
                        return "conflict"

            with ThreadPoolExecutor(max_workers=2) as executor:
                outcomes = list(executor.map(worker, ("race-a", "race-b")))

            with session_factory() as db:
                redemptions = db.execute(select(LoyaltyRedemption).where(LoyaltyRedemption.tenant_id == TENANT_ID)).scalars().all()
                wallet = db.execute(
                    select(PatientWallet).where(PatientWallet.tenant_id == TENANT_ID, PatientWallet.patient_id == PATIENT_ID)
                ).scalar_one()

            self.assertEqual(sorted(outcomes), ["conflict", "success"])
            self.assertEqual(len(redemptions), 1)
            self.assertEqual(wallet.available_balance, Decimal("0.00"))
        finally:
            Base.metadata.drop_all(engine)
            engine.dispose()
            if os.path.exists(temp_db.name):
                os.unlink(temp_db.name)

    def _seed_redemption_fixture(
        self,
        wallet_balance: Decimal,
        eligible_total: Decimal,
        service_category: str = "therapy",
        session_factory: sessionmaker[Session] | None = None,
    ) -> None:
        session_factory = session_factory or self.session_factory
        now = datetime.now(timezone.utc)
        with session_factory() as db:
            tenant = Tenant(
                id=TENANT_ID,
                name="Aster Dental",
                slug="aster-dental-redemption",
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
                first_name="Dana",
                last_name="Redeem",
                phone="+77000000001",
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
                payment_number="payment-redemption-001",
                status="pending",
                currency="KZT",
                total_amount=eligible_total,
                created_at=now,
                updated_at=now,
            )
            payment_line = PaymentLine(
                id="payment-redemption-line-1",
                tenant_id=TENANT_ID,
                payment_id=PAYMENT_ID,
                service_code="svc-redemption-1",
                service_category=service_category,
                quantity=1,
                unit_price=eligible_total,
                line_total=eligible_total,
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
            denied_rule = LoyaltyPolicyServiceRule(
                id="rule-redemption-implants",
                tenant_id=TENANT_ID,
                policy_version_id=POLICY_ID,
                service_category="implants",
                accrual_allowed=False,
                redemption_allowed=False,
                created_at=now,
            )
            wallet = PatientWallet(
                id="wallet-redemption",
                tenant_id=TENANT_ID,
                patient_id=PATIENT_ID,
                available_balance=wallet_balance,
                lifetime_accrued=wallet_balance,
                lifetime_redeemed=Decimal("0.00"),
                lifetime_expired=Decimal("0.00"),
                updated_at=now,
            )
            db.add_all([tenant, branch, patient, visit, payment, payment_line, program, policy, denied_rule, wallet])
            db.commit()


if __name__ == "__main__":
    unittest.main()
