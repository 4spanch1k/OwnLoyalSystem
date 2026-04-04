"""add loyalty manual adjustments for slice 4

Revision ID: 0004_loyalty_manual_adjustments
Revises: 0003_payment_refund_state
Create Date: 2026-04-04 02:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0004_loyalty_manual_adjustments"
down_revision = "0003_payment_refund_state"
branch_labels = None
depends_on = None


MONEY = sa.Numeric(18, 2)


def upgrade() -> None:
    op.create_table(
        "loyalty_manual_adjustments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("patient_id", sa.String(length=36), nullable=False),
        sa.Column("wallet_id", sa.String(length=36), nullable=False),
        sa.Column("ledger_entry_id", sa.String(length=36), nullable=False),
        sa.Column("actor_user_id", sa.String(length=36), nullable=False),
        sa.Column("direction", sa.String(length=16), nullable=False),
        sa.Column("amount", MONEY, nullable=False),
        sa.Column("balance_before", MONEY, nullable=False),
        sa.Column("balance_after", MONEY, nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("reason_code", sa.String(length=64), nullable=False),
        sa.Column("comment", sa.String(length=500), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("applied_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("amount >= 0", name="ck_loyalty_manual_adjustments_amount_non_negative"),
        sa.CheckConstraint("balance_before >= 0", name="ck_loyalty_manual_adjustments_balance_before_non_negative"),
        sa.CheckConstraint("balance_after >= 0", name="ck_loyalty_manual_adjustments_balance_after_non_negative"),
        sa.CheckConstraint(
            "direction IN ('credit', 'debit')",
            name="ck_loyalty_manual_adjustments_direction_valid",
        ),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_loyalty_manual_adjustments_tenant_id_tenants"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "patient_id"],
            ["patients.tenant_id", "patients.id"],
            name="fk_loyalty_manual_adjustments_tenant_patient_patients",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "wallet_id"],
            ["patient_wallets.tenant_id", "patient_wallets.id"],
            name="fk_loyalty_manual_adjustments_tenant_wallet_patient_wallets",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "ledger_entry_id"],
            ["loyalty_ledger_entries.tenant_id", "loyalty_ledger_entries.id"],
            name="fk_loyalty_manual_adjustments_tenant_ledger_loyalty_ledger_entries",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "actor_user_id"],
            ["users.tenant_id", "users.id"],
            name="fk_loyalty_manual_adjustments_tenant_actor_users",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_loyalty_manual_adjustments"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_loyalty_manual_adjustments_tenant_id_id"),
        sa.UniqueConstraint("tenant_id", "ledger_entry_id", name="uq_loyalty_manual_adjustments_tenant_ledger_entry"),
    )
    op.create_index(
        "ix_loyalty_manual_adjustments_tenant_patient_created_at",
        "loyalty_manual_adjustments",
        ["tenant_id", "patient_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_loyalty_manual_adjustments_tenant_patient_created_at", table_name="loyalty_manual_adjustments")
    op.drop_table("loyalty_manual_adjustments")
