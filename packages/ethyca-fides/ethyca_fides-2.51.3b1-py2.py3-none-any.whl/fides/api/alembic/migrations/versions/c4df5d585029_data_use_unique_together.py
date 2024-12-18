"""Data use unique together

Revision ID: c4df5d585029
Revises: cf88efa1ad89
Create Date: 2022-09-26 23:12:00.816657

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c4df5d585029"
down_revision = "cf88efa1ad89"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("consent_data_use_key", "consent", type_="unique")
    op.create_unique_constraint(
        "uix_identity_data_use", "consent", ["provided_identity_id", "data_use"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("uix_identity_data_use", "consent", type_="unique")
    op.create_unique_constraint("consent_data_use_key", "consent", ["data_use"])
    # ### end Alembic commands ###
