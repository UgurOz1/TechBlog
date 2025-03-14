"""Add cascade delete to comments and likes

Revision ID: f3ef9cc5f4d9
Revises: 
Create Date: 2025-01-27 22:15:05.855208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3ef9cc5f4d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('image_file',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
        batch_op.drop_column('is_visible')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_visible', sa.BOOLEAN(), nullable=True))
        batch_op.alter_column('image_file',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)

    # ### end Alembic commands ###
