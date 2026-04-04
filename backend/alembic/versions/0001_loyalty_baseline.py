"""loyalty baseline schema for slice 1

Revision ID: 0001_loyalty_baseline
Revises: None
Create Date: 2026-04-04 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001_loyalty_baseline"
down_revision = None
branch_labels = None
depends_on = None


MONEY = sa.Numeric(18, 2)


def upgrade() -> None:
    op.create_table(
        "tenants",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("default_currency_code", sa.String(length=3), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_tenants"),
        sa.UniqueConstraint("slug", name="uq_tenants_slug"),
    )

    op.create_table(
        "branches",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("address_line", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_branches_tenant_id_tenants"),
        sa.PrimaryKeyConstraint("id", name="pk_branches"),
        sa.UniqueConstraint("tenant_id", "code", name="uq_branches_tenant_code"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_branches_tenant_id_id"),
    )
    op.create_index("ix_branches_tenant_id", "branches", ["tenant_id"], unique=False)
    op.create_index("ix_branches_tenant_id_is_active", "branches", ["tenant_id", "is_active"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_users_tenant_id_tenants"),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("tenant_id", "email", name="uq_users_tenant_email"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_users_tenant_id_id"),
    )
    op.create_index("ix_users_tenant_id", "users", ["tenant_id"], unique=False)

    op.create_table(
        "user_memberships",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("branch_id", sa.String(length=36), nullable=True),
        sa.Column("role_code", sa.String(length=64), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_user_memberships_tenant_id_tenants"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "branch_id"],
            ["branches.tenant_id", "branches.id"],
            name="fk_user_memberships_tenant_branch_branches",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "user_id"],
            ["users.tenant_id", "users.id"],
            name="fk_user_memberships_tenant_user_users",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_user_memberships"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_user_memberships_tenant_id_id"),
    )
    op.create_index("ix_user_memberships_tenant_id", "user_memberships", ["tenant_id"], unique=False)
    op.create_index("ix_user_memberships_tenant_id_user_id", "user_memberships", ["tenant_id", "user_id"], unique=False)

    op.create_table(
        "patients",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("branch_id", sa.String(length=36), nullable=False),
        sa.Column("external_patient_code", sa.String(length=64), nullable=True),
        sa.Column("first_name", sa.String(length=120), nullable=False),
        sa.Column("last_name", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_patients_tenant_id_tenants"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "branch_id"],
            ["branches.tenant_id", "branches.id"],
            name="fk_patients_tenant_branch_branches",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_patients"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_patients_tenant_id_id"),
    )
    op.create_index("ix_patients_tenant_id", "patients", ["tenant_id"], unique=False)
    op.create_index("ix_patients_tenant_id_phone", "patients", ["tenant_id", "phone"], unique=False)

    op.create_table(
        "visits",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("branch_id", sa.String(length=36), nullable=False),
        sa.Column("patient_id", sa.String(length=36), nullable=False),
        sa.Column("doctor_user_id", sa.String(length=36), nullable=True),
        sa.Column("appointment_id", sa.String(length=36), nullable=True),
        sa.Column("visit_number", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_visits_tenant_id_tenants"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "branch_id"],
            ["branches.tenant_id", "branches.id"],
            name="fk_visits_tenant_branch_branches",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "doctor_user_id"],
            ["users.tenant_id", "users.id"],
            name="fk_visits_tenant_doctor_users",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "patient_id"],
            ["patients.tenant_id", "patients.id"],
            name="fk_visits_tenant_patient_patients",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_visits"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_visits_tenant_id_id"),
    )
    op.create_index("ix_visits_tenant_id", "visits", ["tenant_id"], unique=False)
    op.create_index("ix_visits_tenant_id_patient_id", "visits", ["tenant_id", "patient_id"], unique=False)

    op.create_table(
        "payments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("branch_id", sa.String(length=36), nullable=False),
        sa.Column("patient_id", sa.String(length=36), nullable=False),
        sa.Column("visit_id", sa.String(length=36), nullable=False),
        sa.Column("payment_number", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("total_amount", MONEY, nullable=False),
        sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("refunded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("total_amount >= 0", name="ck_payments_total_amount_non_negative"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_payments_tenant_id_tenants"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "branch_id"],
            ["branches.tenant_id", "branches.id"],
            name="fk_payments_tenant_branch_branches",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "patient_id"],
            ["patients.tenant_id", "patients.id"],
            name="fk_payments_tenant_patient_patients",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "visit_id"],
            ["visits.tenant_id", "visits.id"],
            name="fk_payments_tenant_visit_visits",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_payments"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_payments_tenant_id_id"),
        sa.UniqueConstraint("tenant_id", "payment_number", name="uq_payments_tenant_payment_number"),
    )
    op.create_index("ix_payments_tenant_id", "payments", ["tenant_id"], unique=False)
    op.create_index("ix_payments_tenant_id_patient_id", "payments", ["tenant_id", "patient_id"], unique=False)
    op.create_index("ix_payments_tenant_id_status", "payments", ["tenant_id", "status"], unique=False)

    op.create_table(
        "payment_lines",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("payment_id", sa.String(length=36), nullable=False),
        sa.Column("service_code", sa.String(length=64), nullable=False),
        sa.Column("service_category", sa.String(length=64), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", MONEY, nullable=False),
        sa.Column("line_total", MONEY, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("line_total >= 0", name="ck_payment_lines_line_total_non_negative"),
        sa.CheckConstraint("quantity > 0", name="ck_payment_lines_quantity_positive"),
        sa.CheckConstraint("unit_price >= 0", name="ck_payment_lines_unit_price_non_negative"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_payment_lines_tenant_id_tenants"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "payment_id"],
            ["payments.tenant_id", "payments.id"],
            name="fk_payment_lines_tenant_payment_payments",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_payment_lines"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_payment_lines_tenant_id_id"),
    )
    op.create_index("ix_payment_lines_tenant_id", "payment_lines", ["tenant_id"], unique=False)
    op.create_index("ix_payment_lines_payment_id", "payment_lines", ["payment_id"], unique=False)

    op.create_table(
        "loyalty_programs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("branch_id", sa.String(length=36), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("active_policy_version_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_loyalty_programs_tenant_id_tenants"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "branch_id"],
            ["branches.tenant_id", "branches.id"],
            name="fk_loyalty_programs_tenant_branch_branches",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_loyalty_programs"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_loyalty_programs_tenant_id_id"),
    )
    op.create_index("ix_loyalty_programs_tenant_id", "loyalty_programs", ["tenant_id"], unique=False)
    op.create_index("ix_loyalty_programs_tenant_id_status", "loyalty_programs", ["tenant_id", "status"], unique=False)

    op.create_table(
        "loyalty_policy_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("program_id", sa.String(length=36), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("accrual_rate_bps", sa.Integer(), nullable=False),
        sa.Column("redemption_cap_bps", sa.Integer(), nullable=False),
        sa.Column("bonus_ttl_days", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("effective_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("accrual_rate_bps >= 0", name="ck_loyalty_policy_versions_accrual_rate_non_negative"),
        sa.CheckConstraint("bonus_ttl_days > 0", name="ck_loyalty_policy_versions_bonus_ttl_positive"),
        sa.CheckConstraint("redemption_cap_bps >= 0", name="ck_loyalty_policy_versions_redemption_cap_non_negative"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_loyalty_policy_versions_tenant_id_tenants"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "program_id"],
            ["loyalty_programs.tenant_id", "loyalty_programs.id"],
            name="fk_loyalty_policy_versions_tenant_program_loyalty_programs",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_loyalty_policy_versions"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_loyalty_policy_versions_tenant_id_id"),
        sa.UniqueConstraint("tenant_id", "program_id", "version", name="uq_loyalty_policy_versions_program_version"),
    )
    op.create_index("ix_loyalty_policy_versions_tenant_id", "loyalty_policy_versions", ["tenant_id"], unique=False)

    op.create_foreign_key(
        "fk_loyalty_programs_active_policy_version_id",
        "loyalty_programs",
        "loyalty_policy_versions",
        ["active_policy_version_id"],
        ["id"],
    )

    op.create_table(
        "loyalty_policy_service_rules",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("policy_version_id", sa.String(length=36), nullable=False),
        sa.Column("service_category", sa.String(length=64), nullable=False),
        sa.Column("accrual_allowed", sa.Boolean(), nullable=False),
        sa.Column("redemption_allowed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_loyalty_policy_service_rules_tenant_id_tenants"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "policy_version_id"],
            ["loyalty_policy_versions.tenant_id", "loyalty_policy_versions.id"],
            name="fk_lpsr_tenant_policy_versions",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_loyalty_policy_service_rules"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_loyalty_policy_service_rules_tenant_id_id"),
        sa.UniqueConstraint(
            "tenant_id",
            "policy_version_id",
            "service_category",
            name="uq_loyalty_policy_service_rules_policy_category",
        ),
    )
    op.create_index("ix_loyalty_policy_service_rules_tenant_id", "loyalty_policy_service_rules", ["tenant_id"], unique=False)

    op.create_table(
        "patient_wallets",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("patient_id", sa.String(length=36), nullable=False),
        sa.Column("available_balance", MONEY, nullable=False),
        sa.Column("lifetime_accrued", MONEY, nullable=False),
        sa.Column("lifetime_redeemed", MONEY, nullable=False),
        sa.Column("lifetime_expired", MONEY, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("available_balance >= 0", name="ck_patient_wallets_available_balance_non_negative"),
        sa.CheckConstraint("lifetime_accrued >= 0", name="ck_patient_wallets_lifetime_accrued_non_negative"),
        sa.CheckConstraint("lifetime_expired >= 0", name="ck_patient_wallets_lifetime_expired_non_negative"),
        sa.CheckConstraint("lifetime_redeemed >= 0", name="ck_patient_wallets_lifetime_redeemed_non_negative"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_patient_wallets_tenant_id_tenants"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "patient_id"],
            ["patients.tenant_id", "patients.id"],
            name="fk_patient_wallets_tenant_patient_patients",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_patient_wallets"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_patient_wallets_tenant_id_id"),
        sa.UniqueConstraint("tenant_id", "patient_id", name="uq_patient_wallets_tenant_patient"),
    )
    op.create_index("ix_patient_wallets_tenant_id", "patient_wallets", ["tenant_id"], unique=False)
    op.create_index("ix_patient_wallets_tenant_id_patient_id", "patient_wallets", ["tenant_id", "patient_id"], unique=False)

    op.create_table(
        "loyalty_ledger_entries",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("patient_id", sa.String(length=36), nullable=False),
        sa.Column("wallet_id", sa.String(length=36), nullable=False),
        sa.Column("payment_id", sa.String(length=36), nullable=True),
        sa.Column("payment_line_id", sa.String(length=36), nullable=True),
        sa.Column("entry_type", sa.String(length=32), nullable=False),
        sa.Column("amount", MONEY, nullable=False),
        sa.Column("balance_after", MONEY, nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("policy_version_id", sa.String(length=36), nullable=True),
        sa.Column("idempotency_key", sa.String(length=255), nullable=False),
        sa.Column("reason_code", sa.String(length=64), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("amount >= 0", name="ck_loyalty_ledger_entries_amount_non_negative"),
        sa.CheckConstraint("balance_after >= 0", name="ck_loyalty_ledger_entries_balance_after_non_negative"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_loyalty_ledger_entries_tenant_id_tenants"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "patient_id"],
            ["patients.tenant_id", "patients.id"],
            name="fk_loyalty_ledger_entries_tenant_patient_patients",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "wallet_id"],
            ["patient_wallets.tenant_id", "patient_wallets.id"],
            name="fk_loyalty_ledger_entries_tenant_wallet_patient_wallets",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "payment_id"],
            ["payments.tenant_id", "payments.id"],
            name="fk_loyalty_ledger_entries_tenant_payment_payments",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "payment_line_id"],
            ["payment_lines.tenant_id", "payment_lines.id"],
            name="fk_loyalty_ledger_entries_tenant_payment_line_payment_lines",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "policy_version_id"],
            ["loyalty_policy_versions.tenant_id", "loyalty_policy_versions.id"],
            name="fk_loyalty_ledger_entries_tenant_policy_loyalty_policy_versions",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_loyalty_ledger_entries"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_loyalty_ledger_entries_tenant_id_id"),
        sa.UniqueConstraint("tenant_id", "idempotency_key", name="uq_loyalty_ledger_entries_tenant_idempotency_key"),
    )
    op.create_index("ix_loyalty_ledger_entries_tenant_id", "loyalty_ledger_entries", ["tenant_id"], unique=False)
    op.create_index("ix_loyalty_ledger_entries_payment_id", "loyalty_ledger_entries", ["payment_id"], unique=False)
    op.create_index(
        "ix_loyalty_ledger_entries_tenant_patient_created_at",
        "loyalty_ledger_entries",
        ["tenant_id", "patient_id", "created_at"],
        unique=False,
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("actor_user_id", sa.String(length=36), nullable=True),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.String(length=36), nullable=False),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_audit_logs_tenant_id_tenants"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "actor_user_id"],
            ["users.tenant_id", "users.id"],
            name="fk_audit_logs_tenant_actor_users",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_audit_logs"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_audit_logs_tenant_id_id"),
    )
    op.create_index("ix_audit_logs_tenant_id", "audit_logs", ["tenant_id"], unique=False)
    op.create_index("ix_audit_logs_tenant_entity", "audit_logs", ["tenant_id", "entity_type", "entity_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_audit_logs_tenant_entity", table_name="audit_logs")
    op.drop_index("ix_audit_logs_tenant_id", table_name="audit_logs")
    op.drop_table("audit_logs")

    op.drop_index("ix_loyalty_ledger_entries_tenant_patient_created_at", table_name="loyalty_ledger_entries")
    op.drop_index("ix_loyalty_ledger_entries_payment_id", table_name="loyalty_ledger_entries")
    op.drop_index("ix_loyalty_ledger_entries_tenant_id", table_name="loyalty_ledger_entries")
    op.drop_table("loyalty_ledger_entries")

    op.drop_index("ix_patient_wallets_tenant_id_patient_id", table_name="patient_wallets")
    op.drop_index("ix_patient_wallets_tenant_id", table_name="patient_wallets")
    op.drop_table("patient_wallets")

    op.drop_index("ix_loyalty_policy_service_rules_tenant_id", table_name="loyalty_policy_service_rules")
    op.drop_table("loyalty_policy_service_rules")

    op.drop_constraint("fk_loyalty_programs_active_policy_version_id", "loyalty_programs", type_="foreignkey")
    op.drop_index("ix_loyalty_policy_versions_tenant_id", table_name="loyalty_policy_versions")
    op.drop_table("loyalty_policy_versions")

    op.drop_index("ix_loyalty_programs_tenant_id_status", table_name="loyalty_programs")
    op.drop_index("ix_loyalty_programs_tenant_id", table_name="loyalty_programs")
    op.drop_table("loyalty_programs")

    op.drop_index("ix_payment_lines_payment_id", table_name="payment_lines")
    op.drop_index("ix_payment_lines_tenant_id", table_name="payment_lines")
    op.drop_table("payment_lines")

    op.drop_index("ix_payments_tenant_id_status", table_name="payments")
    op.drop_index("ix_payments_tenant_id_patient_id", table_name="payments")
    op.drop_index("ix_payments_tenant_id", table_name="payments")
    op.drop_table("payments")

    op.drop_index("ix_visits_tenant_id_patient_id", table_name="visits")
    op.drop_index("ix_visits_tenant_id", table_name="visits")
    op.drop_table("visits")

    op.drop_index("ix_patients_tenant_id_phone", table_name="patients")
    op.drop_index("ix_patients_tenant_id", table_name="patients")
    op.drop_table("patients")

    op.drop_index("ix_user_memberships_tenant_id_user_id", table_name="user_memberships")
    op.drop_index("ix_user_memberships_tenant_id", table_name="user_memberships")
    op.drop_table("user_memberships")

    op.drop_index("ix_users_tenant_id", table_name="users")
    op.drop_table("users")

    op.drop_index("ix_branches_tenant_id_is_active", table_name="branches")
    op.drop_index("ix_branches_tenant_id", table_name="branches")
    op.drop_table("branches")

    op.drop_table("tenants")
