"""create deputados table

Revision ID: 16b9ba954471
Revises: d599383c15f2
Create Date: 2026-01-18 20:41:44.115423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '16b9ba954471'
down_revision: Union[str, Sequence[str], None] = 'd599383c15f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('deputados',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('uri', sa.VARCHAR(), nullable=False),
    sa.Column('nome', sa.VARCHAR(), nullable=False),
    sa.Column('nomeCivil', sa.VARCHAR(), nullable=False),
    sa.Column('siglaSexo', sa.VARCHAR(), nullable=False),
    sa.Column('idLegislaturaInicial', sa.INTEGER(), nullable=False),
    sa.Column('idLegislaturaFinal', sa.INTEGER(), nullable=False),
    sa.Column('ufNascimento', sa.VARCHAR()),
    sa.Column('municipioNascimento', sa.VARCHAR()),
    sa.Column('dataNascimento', sa.DATE()),
    sa.Column('dataFalecimento', sa.DATE()),
    sa.PrimaryKeyConstraint('id', name=op.f('deputados_pkey'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('deputados')
