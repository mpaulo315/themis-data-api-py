"""create legislatura table

Revision ID: d599383c15f2
Revises: 
Create Date: 2026-01-18 17:09:47.869448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd599383c15f2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "legislaturas",
        sa.Column("idLegislatura", sa.Integer, primary_key=True),
        sa.Column("uri", sa.String, nullable=False),
        sa.Column("dataInicio", sa.Date, nullable=False),
        sa.Column("dataFim", sa.Date, nullable=False),
        sa.Column("anoEleicao", sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("legislaturas")
