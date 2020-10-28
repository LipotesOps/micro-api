"""add flow

Revision ID: d90b753ee69b
Revises: e87c25e17fb6
Create Date: 2020-10-16 23:52:48.632647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d90b753ee69b"
down_revision = "e87c25e17fb6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "flow",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("flow")
    # ### end Alembic commands ###
