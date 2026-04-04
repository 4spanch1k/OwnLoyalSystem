from datetime import datetime, timezone
from decimal import Decimal
import unittest

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db.base import Base
from backend.app.db.models.loyalty import LoyaltyLedgerEntry, PatientWallet
from backend.app.db.models.patient import Patient
from backend.app.db.models.rbac import UserMembership
from backend.app.db.models.tenancy import Tenant
from backend.scripts.seed_loyalty_demo import (
    ACCRUAL_LEDGER_ENTRY_ID,
    EXPECTED_BALANCE,
    MANAGER_USER_ID,
    PATIENT_ID,
    PAYMENT_ID,
    SeedConflictError,
    TENANT_ID,
    seed_demo_dataset,
)


class LoyaltyDemoSeedScriptTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine(
            "sqlite+pysqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=Session,
        )
        Base.metadata.create_all(self.engine)

    def tearDown(self) -> None:
        Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    def test_seed_demo_dataset_creates_canonical_records(self) -> None:
        with self.session_factory() as db:
            summary = seed_demo_dataset(db)

        self.assertTrue(summary.ready_for_demo)
        self.assertEqual(summary.tenant_id, TENANT_ID)
        self.assertEqual(summary.patient_id, PATIENT_ID)
        self.assertEqual(summary.clinic_manager_user_id, MANAGER_USER_ID)
        self.assertEqual(summary.payment_id, PAYMENT_ID)
        self.assertEqual(summary.wallet_balance, EXPECTED_BALANCE)
        self.assertEqual(summary.ledger_entry_count, 1)

        with self.session_factory() as db:
            tenant = db.get(Tenant, TENANT_ID)
            patient = db.get(Patient, PATIENT_ID)
            wallet = db.get(PatientWallet, "wallet-manual-adjustment")
            membership = db.execute(
                select(UserMembership).where(
                    UserMembership.tenant_id == TENANT_ID,
                    UserMembership.user_id == MANAGER_USER_ID,
                    UserMembership.role_code == "clinic_manager",
                )
            ).scalar_one_or_none()
            ledger_entry = db.get(LoyaltyLedgerEntry, ACCRUAL_LEDGER_ENTRY_ID)

        self.assertIsNotNone(tenant)
        self.assertIsNotNone(patient)
        self.assertIsNotNone(wallet)
        self.assertIsNotNone(membership)
        self.assertIsNotNone(ledger_entry)
        self.assertEqual(wallet.available_balance, Decimal("5.00"))
        self.assertEqual(ledger_entry.balance_after, Decimal("5.00"))

    def test_seed_demo_dataset_is_idempotent_without_duplicates(self) -> None:
        with self.session_factory() as db:
            first_summary = seed_demo_dataset(db)

        with self.session_factory() as db:
            second_summary = seed_demo_dataset(db)

        self.assertTrue(first_summary.ready_for_demo)
        self.assertTrue(second_summary.ready_for_demo)

        with self.session_factory() as db:
            tenant_count = db.execute(select(func.count()).select_from(Tenant)).scalar_one()
            patient_count = db.execute(select(func.count()).select_from(Patient)).scalar_one()
            wallet_count = db.execute(select(func.count()).select_from(PatientWallet)).scalar_one()
            ledger_count = db.execute(select(func.count()).select_from(LoyaltyLedgerEntry)).scalar_one()
            manager_membership_count = db.execute(
                select(func.count()).select_from(UserMembership).where(
                    UserMembership.tenant_id == TENANT_ID,
                    UserMembership.user_id == MANAGER_USER_ID,
                    UserMembership.role_code == "clinic_manager",
                )
            ).scalar_one()

        self.assertEqual(tenant_count, 1)
        self.assertEqual(patient_count, 1)
        self.assertEqual(wallet_count, 1)
        self.assertEqual(ledger_count, 1)
        self.assertEqual(manager_membership_count, 1)

    def test_seed_demo_dataset_fails_fast_on_demo_drift(self) -> None:
        with self.session_factory() as db:
            seed_demo_dataset(db)
            extra_ledger = LoyaltyLedgerEntry(
                id="ledger-extra-demo",
                tenant_id=TENANT_ID,
                patient_id=PATIENT_ID,
                wallet_id="wallet-manual-adjustment",
                payment_id=None,
                payment_line_id=None,
                entry_type="manual_adjustment",
                amount=Decimal("1.00"),
                balance_after=Decimal("6.00"),
                currency="KZT",
                status="posted",
                policy_version_id=None,
                idempotency_key="manual_adjustment:test",
                reason_code="goodwill_credit",
                metadata_json={"direction": "credit"},
                created_at=datetime.now(timezone.utc),
            )
            db.add(extra_ledger)
            db.commit()

            with self.assertRaises(SeedConflictError):
                seed_demo_dataset(db)


if __name__ == "__main__":
    unittest.main()
