"""add user settings fields

Revision ID: 0f8b7f8b7d2a
Revises: db2a4ea6bd55
Create Date: 2026-08-12 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0f8b7f8b7d2a"
down_revision: Union[str, Sequence[str], None] = "db2a4ea6bd55"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "meliponary_name",
            sa.String(),
            server_default="Meu Meliponário",
            nullable=True,
        ),
    )
    op.add_column("users", sa.Column("meliponary_location", sa.String(), nullable=True))
    op.add_column(
        "users",
        sa.Column(
            "inspection_frequency_days",
            sa.Integer(),
            server_default="14",
            nullable=True,
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "notify_health_alerts",
            sa.Boolean(),
            server_default=sa.true(),
            nullable=True,
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "notify_email",
            sa.Boolean(),
            server_default=sa.true(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "notify_email")
    op.drop_column("users", "notify_health_alerts")
    op.drop_column("users", "inspection_frequency_days")
    op.drop_column("users", "meliponary_location")
    op.drop_column("users", "meliponary_name")
