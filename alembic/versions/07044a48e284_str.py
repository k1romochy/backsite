"""str

Revision ID: 07044a48e284
Revises: 5ca651de666c
Create Date: 2025-02-10 14:43:01.907893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07044a48e284'
down_revision: Union[str, None] = '5ca651de666c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('message', 'message',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('message', 'message',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
