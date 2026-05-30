"""set hospital active default true

Revision ID: 20250530_02
Revises: 20250530_01
Create Date: 2026-05-30 09:55:00
"""

from __future__ import annotations

import alembic.op as op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20250530_02"
down_revision = "20250530_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("hospitals") as batch_op:
        batch_op.alter_column("active", existing_type=sa.Boolean(), server_default=sa.true())


def downgrade() -> None:
    with op.batch_alter_table("hospitals") as batch_op:
        batch_op.alter_column("active", existing_type=sa.Boolean(), server_default=sa.false())
