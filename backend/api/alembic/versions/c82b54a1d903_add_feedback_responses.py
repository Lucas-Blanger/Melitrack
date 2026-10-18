"""Add feedback responses.

Revision ID: c82b54a1d903
Revises: 4b8d2f6c9a10
Create Date: 2026-10-18 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "c82b54a1d903"
down_revision: Union[str, Sequence[str], None] = "4b8d2f6c9a10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "feedback_responses",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("enjoyment", sa.String(length=20), nullable=False),
        sa.Column("comments", sa.Text(), nullable=False),
        sa.Column("suggestions", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "enjoyment IN ('gostando', 'neutro', 'nao_gostando')",
            name="ck_feedback_responses_enjoyment",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_feedback_responses_user_id",
        "feedback_responses",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_feedback_responses_user_id", table_name="feedback_responses")
    op.drop_table("feedback_responses")
