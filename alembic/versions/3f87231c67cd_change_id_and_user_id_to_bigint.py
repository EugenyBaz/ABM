"""change id and user_id to bigint

Revision ID: 3f87231c67cd
Revises: bigint_user_id
Create Date: 2025-12-24 23:25:55.289543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f87231c67cd'
down_revision: Union[str, Sequence[str], None] = 'bigint_user_id'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Если есть первичный ключ, нужно временно его убрать или использовать batch_alter_table
    with op.batch_alter_table('tasks') as batch_op:
        batch_op.alter_column('id', type_=sa.BigInteger(), existing_type=sa.Integer())
        batch_op.alter_column('user_id', type_=sa.BigInteger(), existing_type=sa.Integer())

def downgrade():
    with op.batch_alter_table('tasks') as batch_op:
        batch_op.alter_column('id', type_=sa.Integer(), existing_type=sa.BigInteger())
        batch_op.alter_column('user_id', type_=sa.Integer(), existing_type=sa.BigInteger())