"""create-analyses

Revision ID: 5da3fe7a1605
Revises: 52bb4830260c
Create Date: 2022-01-08 14:46:52.878217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5da3fe7a1605'
down_revision = '52bb4830260c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "analyses",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("result", sa.Float, nullable=False),
        sa.Column("logId", sa.Integer)
    )


def downgrade():
    op.drop_table("analyses")
