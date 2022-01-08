"""create-logs

Revision ID: 52bb4830260c
Revises: af4faadbe399
Create Date: 2022-01-08 14:20:28.757860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52bb4830260c'
down_revision = 'af4faadbe399'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("content", sa.String, nullable=False),
        sa.Column("dateTime", sa.DateTime, nullable=False),
        sa.Column("userId", sa.Integer)
    )


def downgrade():
    op.drop_table("logs")
