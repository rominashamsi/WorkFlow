
"""add task creator

Revision ID: d7d7932fb45b
Revises: 1c97b17a7c37
Create Date: 2026-10-12 15:31:23.908521
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d7d7932fb45b"
down_revision: Union[str, Sequence[str], None] = "1c97b17a7c37"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column("created_by", sa.Integer(), nullable=True),
    )

    with op.batch_alter_table("tasks") as batch_op:
        batch_op.create_foreign_key(
            "fk_tasks_created_by_users",
            "users",
            ["created_by"],
            ["id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.drop_constraint(
            "fk_tasks_created_by_users",
            type_="foreignkey",
        )

    op.drop_column("tasks", "created_by")
