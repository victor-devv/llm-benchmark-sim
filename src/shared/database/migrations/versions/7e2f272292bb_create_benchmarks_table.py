"""create_benchmarks_table

Revision ID: 7e2f272292bb
Revises: ef463acebe5a
Create Date: 2024-10-23 18:37:09.935814

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7e2f272292bb"
down_revision: Union[str, None] = "ef463acebe5a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "benchmarks",
        sa.Column(
            "id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("llm_id", sa.UUID(), nullable=False),
        sa.Column("metric_id", sa.UUID(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["llm_id"], ["llms.id"]),
        sa.ForeignKeyConstraint(["metric_id"], ["metrics.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index("benchmarks_llm_id_idx", "benchmarks", ["llm_id"], unique=False)
    op.create_index(
        "benchmarks_metric_id_idx", "benchmarks", ["metric_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("benchmarks_metric_id_idx", table_name="benchmarks")
    op.drop_index("benchmarks_llm_id_idx", table_name="benchmarks")
    op.drop_table("benchmarks")
