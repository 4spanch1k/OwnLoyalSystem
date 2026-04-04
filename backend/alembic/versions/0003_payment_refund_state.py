"""add payment refund state for rollback flow

Revision ID: 0003_payment_refund_state
Revises: 0002_loyalty_redemptions
Create Date: 2026-04-04 01:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0003_payment_refund_state"
down_revision = "0002_loyalty_redemptions"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "payments",
        sa.Column(
            "refunded_amount",
            sa.Numeric(18, 2),
            nullable=False,
            server_default="0.00",
        ),
    )
    op.create_check_constraint(
        "ck_payments_refunded_amount_non_negative",
        "payments",
        "refunded_amount >= 0",
    )


def downgrade() -> None:
    op.drop_constraint("ck_payments_refunded_amount_non_negative", "payments", type_="check")
    op.drop_column("payments", "refunded_amount")
