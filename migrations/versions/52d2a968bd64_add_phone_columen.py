"""Add phone columen

Revision ID: 52d2a968bd64
Revises: d216c98fc461
Create Date: 2024-11-25 00:41:12.427217

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '52d2a968bd64'
down_revision = 'd216c98fc461'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attachment')
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone', sa.String(length=10), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.drop_column('phone')

    op.create_table('attachment',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('ticket_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('file_name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('file_path', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('uploaded_at', mysql.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.id'], name='attachment_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
