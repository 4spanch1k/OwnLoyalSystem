from datetime import datetime, timezone
from decimal import Decimal
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db.base import Base
from backend.app.db.models.audit import AuditLog
from backend.app.db.models.loyalty import LoyaltyLedgerEntry, PatientWallet
from backend.app.db.models.loyalty_manual_adjustment import LoyaltyManualAdjustment
from backend.app.db.models.patient import Patient
from backend.app.db.models.rbac import User, UserMembership
from backend.app.db.models.tenancy import Branch, Tenant
from backend.app.db.session import get_db
from backend.app.main import app
from backend.app.services.loyalty.manual_adjustment import create_manual_adjustment

TENANT_ID = "tenant-manual-adjustment"
BRANCH_ID = "branch-manual-adjustment"
PATIENT_ID = "patient-manual-adjustment"
MANAGER_USER_ID = "user-clinic-manager"
OWNER_USER_ID = "user-owner"
FRONT_DESK_USER_ID = "user-front-desk"


class LoyaltyManualAdjustmentFlowTestCase(unittest.TestCase):
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

    def test_clinic_manager_can_create_manual_credit_and_wallet_if_missing(self) -> None:
        self._seed_fixture(wallet_balance=None)

        response = self.client.post(
            f"/api/v1/patients/{PATIENT_ID}/wallet/adjustments",
            headers={"X-Tenant-Id": TENANT_ID, "X-Actor-User-Id": MANAGER_USER_ID},
            json={
                "amount": "5.00",
                "direction": "credit",
                "reason_code": "goodwill_credit",
                "comment": "Compensation for delayed appointment",
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(Decimal(str(payload["wallet_balance_after"])), Decimal("5.00"))
        self.assertEqual(payload["direction"], "credit")

        with self.session_factory() as db:
            wallet = db.execute(
                select(PatientWallet).where(PatientWallet.tenant_id == TENANT_ID, PatientWallet.patient_id == PATIENT_ID)
            ).scalar_one()
            ledger_entry = db.execute(
                select(LoyaltyLedgerEntry).where(LoyaltyLedgerEntry.tenant_id == TENANT_ID, LoyaltyLedgerEntry.id == payload["ledger_entry_id"])
            ).scalar_one()
            adjustment = db.execute(
                select(LoyaltyManualAdjustment).where(
                    LoyaltyManualAdjustment.tenant_id == TENANT_ID,
                    LoyaltyManualAdjustment.id == payload["adjustment_id"],
                )
            ).scalar_one()
            audit_log = db.execute(
                select(AuditLog).where(AuditLog.tenant_id == TENANT_ID, AuditLog.id == payload["audit_log_id"])
            ).scalar_one()

        self.assertEqual(wallet.available_balance, Decimal("5.00"))
        self.assertEqual(ledger_entry.entry_type, "manual_adjustment")
        self.assertEqual(ledger_entry.metadata_json["direction"], "credit")
        self.assertEqual(adjustment.reason_code, "goodwill_credit")
        self.assertEqual(audit_log.action, "loyalty_manual_adjustment_created")

    def test_owner_can_create_manual_debit_within_balance(self) -> None:
        self._seed_fixture(wallet_balance=Decimal("20.00"))

        response = self.client.post(
            f"/api/v1/patients/{PATIENT_ID}/wallet/adjustments",
            headers={"X-Tenant-Id": TENANT_ID, "X-Actor-User-Id": OWNER_USER_ID},
            json={
                "amount": "7.50",
                "direction": "debit",
                "reason_code": "billing_fix",
                "comment": "Correct previous over-credit",
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(Decimal(str(payload["balance_before"])), Decimal("20.00"))
        self.assertEqual(Decimal(str(payload["wallet_balance_after"])), Decimal("12.50"))

    def test_forbidden_role_is_rejected(self) -> None:
        self._seed_fixture(wallet_balance=Decimal("20.00"))

        response = self.client.post(
            f"/api/v1/patients/{PATIENT_ID}/wallet/adjustments",
            headers={"X-Tenant-Id": TENANT_ID, "X-Actor-User-Id": FRONT_DESK_USER_ID},
            json={
                "amount": "5.00",
                "direction": "credit",
                "reason_code": "goodwill_credit",
                "comment": "Compensation",
            },
        )

        self.assertEqual(response.status_code, 403)
        with self.session_factory() as db:
            self.assertEqual(db.execute(select(LoyaltyManualAdjustment)).scalars().all(), [])
            self.assertEqual(db.execute(select(LoyaltyLedgerEntry)).scalars().all(), [])

    def test_missing_reason_and_blank_comment_are_rejected(self) -> None:
        self._seed_fixture(wallet_balance=Decimal("20.00"))

        missing_reason_response = self.client.post(
            f"/api/v1/patients/{PATIENT_ID}/wallet/adjustments",
            headers={"X-Tenant-Id": TENANT_ID, "X-Actor-User-Id": MANAGER_USER_ID},
            json={"amount": "5.00", "direction": "credit", "comment": "Compensation"},
        )
        blank_comment_response = self.client.post(
            f"/api/v1/patients/{PATIENT_ID}/wallet/adjustments",
            headers={"X-Tenant-Id": TENANT_ID, "X-Actor-User-Id": MANAGER_USER_ID},
            json={
                "amount": "5.00",
                "direction": "credit",
                "reason_code": "goodwill_credit",
                "comment": "   ",
            },
        )

        self.assertEqual(missing_reason_response.status_code, 422)
        self.assertEqual(blank_comment_response.status_code, 422)

    def test_manual_debit_cannot_overspend_wallet(self) -> None:
        self._seed_fixture(wallet_balance=Decimal("20.00"))

        response = self.client.post(
            f"/api/v1/patients/{PATIENT_ID}/wallet/adjustments",
            headers={"X-Tenant-Id": TENANT_ID, "X-Actor-User-Id": MANAGER_USER_ID},
            json={
                "amount": "25.00",
                "direction": "debit",
                "reason_code": "billing_fix",
                "comment": "Attempted correction",
            },
        )

        self.assertEqual(response.status_code, 409)
        with self.session_factory() as db:
            wallet = db.execute(
                select(PatientWallet).where(PatientWallet.tenant_id == TENANT_ID, PatientWallet.patient_id == PATIENT_ID)
            ).scalar_one()
        self.assertEqual(wallet.available_balance, Decimal("20.00"))

    def test_wallet_and_last_ledger_balance_stay_consistent_after_adjustment(self) -> None:
        self._seed_fixture(wallet_balance=Decimal("20.00"))

        response = self.client.post(
            f"/api/v1/patients/{PATIENT_ID}/wallet/adjustments",
            headers={"X-Tenant-Id": TENANT_ID, "X-Actor-User-Id": MANAGER_USER_ID},
            json={
                "amount": "4.00",
                "direction": "debit",
                "reason_code": "admin_error_fix",
                "comment": "Correction after duplicated bonus",
            },
        )
        self.assertEqual(response.status_code, 200)

        wallet_response = self.client.get(f"/api/v1/patients/{PATIENT_ID}/wallet", headers={"X-Tenant-Id": TENANT_ID})
        ledger_response = self.client.get(f"/api/v1/patients/{PATIENT_ID}/ledger", headers={"X-Tenant-Id": TENANT_ID})

        self.assertEqual(wallet_response.status_code, 200)
        self.assertEqual(ledger_response.status_code, 200)

        wallet_payload = wallet_response.json()
        last_entry = ledger_response.json()["items"][0]

        self.assertEqual(last_entry["entry_type"], "manual_adjustment")
        self.assertEqual(Decimal(str(wallet_payload["available_balance"])), Decimal(str(last_entry["balance_after"])))
        self.assertEqual(Decimal(str(wallet_payload["available_balance"])), Decimal("16.00"))

    def test_transaction_rolls_back_if_audit_write_fails(self) -> None:
        self._seed_fixture(wallet_balance=Decimal("20.00"))

        with self.assertRaises(RuntimeError):
            with self.session_factory() as db:
                with patch(
                    "backend.app.services.loyalty.manual_adjustment._append_audit_log",
                    side_effect=RuntimeError("audit unavailable"),
                ):
                    create_manual_adjustment(
                        db=db,
                        tenant_id=TENANT_ID,
                        patient_id=PATIENT_ID,
                        amount=Decimal("5.00"),
                        direction="credit",
                        reason_code="goodwill_credit",
                        comment="Compensation after service issue",
                        actor_user_id=MANAGER_USER_ID,
                    )

        with self.session_factory() as db:
            wallet = db.execute(
                select(PatientWallet).where(PatientWallet.tenant_id == TENANT_ID, PatientWallet.patient_id == PATIENT_ID)
            ).scalar_one()
            adjustments = db.execute(select(LoyaltyManualAdjustment).where(LoyaltyManualAdjustment.tenant_id == TENANT_ID)).scalars().all()
            ledger_entries = db.execute(select(LoyaltyLedgerEntry).where(LoyaltyLedgerEntry.tenant_id == TENANT_ID)).scalars().all()
            audit_logs = db.execute(select(AuditLog).where(AuditLog.tenant_id == TENANT_ID)).scalars().all()

        self.assertEqual(wallet.available_balance, Decimal("20.00"))
        self.assertEqual(adjustments, [])
        self.assertEqual(ledger_entries, [])
        self.assertEqual(audit_logs, [])

    def _seed_fixture(self, wallet_balance: Decimal | None) -> None:
        now = datetime.now(timezone.utc)
        with self.session_factory() as db:
            db.add(
                Tenant(
                    id=TENANT_ID,
                    name="Aster Dental",
                    slug="aster-dental-manual-adjustment",
                    status="active",
                    default_currency_code="KZT",
                    timezone="Asia/Almaty",
                    created_at=now,
                    updated_at=now,
                )
            )
            db.add(
                Branch(
                    id=BRANCH_ID,
                    tenant_id=TENANT_ID,
                    name="Main Branch",
                    code="main",
                    is_active=True,
                    created_at=now,
                    updated_at=now,
                )
            )
            db.add(
                Patient(
                    id=PATIENT_ID,
                    tenant_id=TENANT_ID,
                    branch_id=BRANCH_ID,
                    first_name="Aruzhan",
                    last_name="Patient",
                    phone="+77000000011",
                    status="active",
                    created_at=now,
                    updated_at=now,
                )
            )
            for user_id, email, role_code in (
                (MANAGER_USER_ID, "manager@example.com", "clinic_manager"),
                (OWNER_USER_ID, "owner@example.com", "owner"),
                (FRONT_DESK_USER_ID, "frontdesk@example.com", "front_desk"),
            ):
                db.add(
                    User(
                        id=user_id,
                        tenant_id=TENANT_ID,
                        email=email,
                        password_hash="hashed",
                        full_name=role_code.replace("_", " ").title(),
                        status="active",
                        created_at=now,
                        updated_at=now,
                    )
                )
                db.add(
                    UserMembership(
                        id=f"membership-{user_id}",
                        tenant_id=TENANT_ID,
                        user_id=user_id,
                        branch_id=None,
                        role_code=role_code,
                        is_active=True,
                        created_at=now,
                        updated_at=now,
                    )
                )
            if wallet_balance is not None:
                db.add(
                    PatientWallet(
                        id="wallet-manual-adjustment",
                        tenant_id=TENANT_ID,
                        patient_id=PATIENT_ID,
                        available_balance=wallet_balance,
                        lifetime_accrued=Decimal("0.00"),
                        lifetime_redeemed=Decimal("0.00"),
                        lifetime_expired=Decimal("0.00"),
                        updated_at=now,
                    )
                )
            db.commit()
