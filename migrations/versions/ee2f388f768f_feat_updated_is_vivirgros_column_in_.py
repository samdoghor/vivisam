"""feat: updated is_vivirgros column in email_lists table constrain to not be nullable

Revision ID: ee2f388f768f
Revises: f4674a9dc644
Create Date: 2023-12-20 15:17:11.966376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee2f388f768f'
down_revision = 'f4674a9dc644'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('email_lists', schema=None) as batch_op:
        batch_op.alter_column('is_vivirgros',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('email_lists', schema=None) as batch_op:
        batch_op.alter_column('is_vivirgros',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###
