"""add loyalty redemptions for slice 2

Revision ID: 0002_loyalty_redemptions
Revises: 0001_loyalty_baseline
Create Date: 2026-04-04 00:30:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0002_loyalty_redemptions"
down_revision = "0001_loyalty_baseline"
branch_labels = None
depends_on = None


MONEY = sa.Numeric(18, 2)


def upgrade() -> None:
    op.create_table(
        "loyalty_redemptions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("patient_id", sa.String(length=36), nullable=False),
        sa.Column("payment_id", sa.String(length=36), nullable=False),
        sa.Column("wallet_id", sa.String(length=36), nullable=False),
        sa.Column("policy_version_id", sa.String(length=36), nullable=False),
        sa.Column("requested_amount", MONEY, nullable=False),
        sa.Column("approved_amount", MONEY, nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("idempotency_key", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("requested_amount >= 0", name="ck_loyalty_redemptions_requested_amount_non_negative"),
        sa.CheckConstraint("approved_amount >= 0", name="ck_loyalty_redemptions_approved_amount_non_negative"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_loyalty_redemptions_tenant_id_tenants"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "patient_id"],
            ["patients.tenant_id", "patients.id"],
            name="fk_loyalty_redemptions_tenant_patient_patients",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "payment_id"],
            ["payments.tenant_id", "payments.id"],
            name="fk_loyalty_redemptions_tenant_payment_payments",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "wallet_id"],
            ["patient_wallets.tenant_id", "patient_wallets.id"],
            name="fk_loyalty_redemptions_tenant_wallet_patient_wallets",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "policy_version_id"],
            ["loyalty_policy_versions.tenant_id", "loyalty_policy_versions.id"],
            name="fk_loyalty_redemptions_tenant_policy_loyalty_policy_versions",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_loyalty_redemptions"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_loyalty_redemptions_tenant_id_id"),
        sa.UniqueConstraint("tenant_id", "idempotency_key", name="uq_loyalty_redemptions_tenant_idempotency_key"),
    )
    op.create_index(
        "ix_loyalty_redemptions_tenant_patient_created_at",
        "loyalty_redemptions",
        ["tenant_id", "patient_id", "created_at"],
        unique=False,
    )
    op.create_index("ix_loyalty_redemptions_payment_id", "loyalty_redemptions", ["payment_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_loyalty_redemptions_payment_id", table_name="loyalty_redemptions")
    op.drop_index("ix_loyalty_redemptions_tenant_patient_created_at", table_name="loyalty_redemptions")
    op.drop_table("loyalty_redemptions")
