"""add ml prediction corrections

Revision ID: 4b8d2f6c9a10
Revises: 0f8b7f8b7d2a
Create Date: 2026-08-13 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "4b8d2f6c9a10"
down_revision: Union[str, Sequence[str], None] = "0f8b7f8b7d2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "ml_predictions",
        sa.Column(
            "corrected_result",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )
    op.add_column(
        "ml_predictions",
        sa.Column("correction_notes", sa.Text(), nullable=True),
    )
    op.add_column(
        "ml_predictions",
        sa.Column("corrected_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("ml_predictions", "corrected_at")
    op.drop_column("ml_predictions", "correction_notes")
    op.drop_column("ml_predictions", "corrected_result")
