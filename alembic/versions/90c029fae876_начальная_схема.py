from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "bigint_user_id"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.alter_column(
        "tasks",
        "user_id",
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
    )
    op.alter_column(
        "tasks",
        "id",
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
    )

def downgrade() -> None:
    op.alter_column(
        "tasks",
        "user_id",
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
    )
    op.alter_column(
        "tasks",
        "id",
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
    )
