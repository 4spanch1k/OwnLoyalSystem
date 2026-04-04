import unittest

from sqlalchemy import create_engine, inspect

from backend.app.db.base import Base
import backend.app.db.models  # noqa: F401


class ModelMetadataTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.inspector = inspect(cls.engine)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.inspector = None
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

    def test_expected_tables_are_registered(self) -> None:
        expected_tables = {
            "tenants",
            "branches",
            "users",
            "user_memberships",
            "patients",
            "visits",
            "payments",
            "payment_lines",
            "loyalty_programs",
            "loyalty_policy_versions",
            "loyalty_policy_service_rules",
            "patient_wallets",
            "loyalty_ledger_entries",
            "loyalty_manual_adjustments",
            "loyalty_redemptions",
            "audit_logs",
        }

        self.assertEqual(expected_tables, set(Base.metadata.tables.keys()))

    def test_wallet_and_ledger_uniques_are_registered(self) -> None:
        wallet_uniques = {tuple(constraint["column_names"]) for constraint in self.inspector.get_unique_constraints("patient_wallets")}
        ledger_uniques = {
            tuple(constraint["column_names"]) for constraint in self.inspector.get_unique_constraints("loyalty_ledger_entries")
        }
        redemption_uniques = {
            tuple(constraint["column_names"]) for constraint in self.inspector.get_unique_constraints("loyalty_redemptions")
        }
        manual_adjustment_uniques = {
            tuple(constraint["column_names"])
            for constraint in self.inspector.get_unique_constraints("loyalty_manual_adjustments")
        }

        self.assertIn(("tenant_id", "patient_id"), wallet_uniques)
        self.assertIn(("tenant_id", "idempotency_key"), ledger_uniques)
        self.assertIn(("tenant_id", "idempotency_key"), redemption_uniques)
        self.assertIn(("tenant_id", "ledger_entry_id"), manual_adjustment_uniques)

    def test_slice_one_indexes_exist(self) -> None:
        payments_indexes = {tuple(index["column_names"]) for index in self.inspector.get_indexes("payments")}
        payment_line_indexes = {tuple(index["column_names"]) for index in self.inspector.get_indexes("payment_lines")}
        wallet_indexes = {tuple(index["column_names"]) for index in self.inspector.get_indexes("patient_wallets")}
        ledger_indexes = {tuple(index["column_names"]) for index in self.inspector.get_indexes("loyalty_ledger_entries")}
        manual_adjustment_indexes = {
            tuple(index["column_names"]) for index in self.inspector.get_indexes("loyalty_manual_adjustments")
        }
        redemption_indexes = {tuple(index["column_names"]) for index in self.inspector.get_indexes("loyalty_redemptions")}
        audit_indexes = {tuple(index["column_names"]) for index in self.inspector.get_indexes("audit_logs")}

        self.assertIn(("tenant_id", "patient_id"), payments_indexes)
        self.assertIn(("tenant_id", "status"), payments_indexes)
        self.assertIn(("payment_id",), payment_line_indexes)
        self.assertIn(("tenant_id", "patient_id"), wallet_indexes)
        self.assertIn(("tenant_id", "patient_id", "created_at"), ledger_indexes)
        self.assertIn(("tenant_id", "patient_id", "created_at"), manual_adjustment_indexes)
        self.assertIn(("payment_id",), ledger_indexes)
        self.assertIn(("tenant_id", "patient_id", "created_at"), redemption_indexes)
        self.assertIn(("payment_id",), redemption_indexes)
        self.assertIn(("tenant_id", "entity_type", "entity_id"), audit_indexes)


if __name__ == "__main__":
    unittest.main()
