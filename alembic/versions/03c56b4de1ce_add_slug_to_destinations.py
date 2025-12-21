"""add slug to destinations

Revision ID: 03c56b4de1ce
Revises: 281200e264e8
Create Date: 2025-12-21 05:04:06.029058
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import re

# revision identifiers, used by Alembic.
revision: str = "03c56b4de1ce"
down_revision: Union[str, None] = "281200e264e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


def upgrade() -> None:
    # 1️⃣ Add column as nullable
    op.add_column(
        "destinations",
        sa.Column("slug", sa.String(length=255), nullable=True),
    )

    # 2️⃣ Backfill existing rows
    conn = op.get_bind()

    destinations = sa.table(
        "destinations",
        sa.column("id"),
        sa.column("name"),
        sa.column("slug"),
    )

    rows = conn.execute(
        sa.select(destinations.c.id, destinations.c.name)
    ).fetchall()

    for row in rows:
        slug = slugify(row.name) or "destination"
        conn.execute(
            destinations.update()
            .where(destinations.c.id == row.id)
            .values(slug=slug)
        )

    # 3️⃣ Make slug NOT NULL + UNIQUE
    op.alter_column("destinations", "slug", nullable=False)
    op.create_unique_constraint(
        "uq_destinations_slug",
        "destinations",
        ["slug"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_destinations_slug", "destinations", type_="unique")
    op.drop_column("destinations", "slug")
