"""schemas correction

Revision ID: a6efe86d55da
Revises: ff11bd0c618a
Create Date: 2025-02-16 19:50:49.844269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6efe86d55da'
down_revision = 'ff11bd0c618a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('doctors', 'password',
               existing_type=sa.VARCHAR(),
               nullable=True,
               existing_server_default=sa.text("'default_password'::character varying"))
    op.drop_column('doctors', 'hashed_password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('doctors', sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.alter_column('doctors', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False,
               existing_server_default=sa.text("'default_password'::character varying"))
    # ### end Alembic commands ###
