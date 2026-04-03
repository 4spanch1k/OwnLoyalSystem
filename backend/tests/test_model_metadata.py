import unittest

from backend.app.modules.audit import models as audit_models
from backend.app.modules.loyalty_ledger import models as loyalty_ledger_models
from backend.app.modules.loyalty_programs import models as loyalty_program_models
from backend.app.modules.loyalty_wallet import models as loyalty_wallet_models
from backend.app.modules.patients import models as patient_models
from backend.app.modules.payments import models as payment_models
from backend.app.modules.rbac import models as rbac_models
from backend.app.modules.tenancy import models as tenancy_models
from backend.app.modules.visits import models as visit_models
from backend.app.shared.db.base import Base


class ModelMetadataTestCase(unittest.TestCase):
    def test_expected_tables_are_registered(self) -> None:
        _ = (
            audit_models,
            loyalty_ledger_models,
            loyalty_program_models,
            loyalty_wallet_models,
            patient_models,
            payment_models,
            rbac_models,
            tenancy_models,
            visit_models,
        )
        expected_tables = {
            "tenants",
            "branches",
            "users",
            "user_memberships",
            "patients",
            "patient_consents",
            "visits",
            "payments",
            "payment_lines",
            "loyalty_programs",
            "loyalty_policy_versions",
            "loyalty_policy_service_rules",
            "patient_wallets",
            "loyalty_ledger_entries",
            "loyalty_redemptions",
            "loyalty_manual_adjustments",
            "audit_logs",
        }

        self.assertTrue(expected_tables.issubset(set(Base.metadata.tables.keys())))


if __name__ == "__main__":
    unittest.main()
