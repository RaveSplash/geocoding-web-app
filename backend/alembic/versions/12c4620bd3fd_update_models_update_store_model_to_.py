"""Update(Models): Update store model to make address unique

Revision ID: 12c4620bd3fd
Revises: bae18f95d488
Create Date: 2023-12-21 23:21:49.477189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12c4620bd3fd'
down_revision: Union[str, None] = 'bae18f95d488'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     # Create a new table with the unique constraint
    op.create_table(
        'stores_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), index=True),
        sa.Column('address', sa.String(), unique=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data from the old table to the new table
    op.execute('INSERT INTO stores_new (id, name, address) SELECT id, name, address FROM stores')

    # Drop the old table
    op.drop_table('stores')

    # Rename the new table to the original table name
    op.rename_table('stores_new', 'stores')

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'stores', type_='unique')
    # ### end Alembic commands ###
