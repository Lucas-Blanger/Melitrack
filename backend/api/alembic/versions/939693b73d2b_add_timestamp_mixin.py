"""add timestamp mixin

Revision ID: 939693b73d2b
Revises: 88afac00a395
Create Date: 2026-07-07 00:38:07.892928

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "939693b73d2b"
down_revision: Union[str, Sequence[str], None] = "88afac00a395"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # No-op: created_at/updated_at columns for these tables were already
    # included when the initial schema (88afac00a395) was generated,
    # making this migration redundant. hive_photos never had an
    # 'uploaded_at' column to drop either. Kept as a no-op to preserve
    # the revision chain (d6aa2dd82355 depends on this revision).
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
