"""create notes table

Revision ID: 153e5fa1eaa3
Revises:
Create Date: 2026-10-19 18:17:01.250453
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "153e5fa1eaa3"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    notes = op.create_table(
        "notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # Example rows, so "Load notes" shows something on a fresh database.
    op.bulk_insert(
        notes,
        [
            {"body": "Hello from Postgres!"},
            {"body": "This note was inserted by the first Alembic migration."},
            {"body": "Edit the models in backend/src/app/models to change the schema."},
        ],
    )


def downgrade() -> None:
    op.drop_table("notes")
