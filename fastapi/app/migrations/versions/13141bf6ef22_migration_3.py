"""migration 3

Revision ID: 13141bf6ef22
Revises: 6c9e3a150bc3
Create Date: 2025-01-30 01:09:04.338144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13141bf6ef22'
down_revision: Union[str, None] = '6c9e3a150bc3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('people_count', sa.Integer(), nullable=True),
    sa.Column('cost', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('room')
    # ### end Alembic commands ###
