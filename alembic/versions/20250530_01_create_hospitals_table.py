"""create hospitals table

Revision ID: 20250530_01
Revises:
Create Date: 2026-05-30 09:40:00
"""

from __future__ import annotations

import alembic.op as op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20250530_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "hospitals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("address", sa.String(length=500), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=False),
        sa.Column("creation_batch_id", sa.String(length=36), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_hospitals_creation_batch_id"), "hospitals", ["creation_batch_id"], unique=False
    )
    op.create_index(op.f("ix_hospitals_id"), "hospitals", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_hospitals_id"), table_name="hospitals")
    op.drop_index(op.f("ix_hospitals_creation_batch_id"), table_name="hospitals")
    op.drop_table("hospitals")
