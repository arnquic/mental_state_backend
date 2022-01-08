"""create_users

Revision ID: af4faadbe399
Revises: 
Create Date: 2022-01-08 14:02:21.027059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af4faadbe399'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("firstName", sa.String, nullable=False),
        sa.Column("lastName", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("password", sa.String, nullable=False)
    )


def downgrade():
    op.drop_table("users")
