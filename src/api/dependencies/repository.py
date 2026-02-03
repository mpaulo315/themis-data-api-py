from typing import Annotated
from fastapi import Depends

from api.dependencies.db import DBSessionDep
from api.repositories.deputado import DeputadoRepository
from api.repositories.legislatura import LegislaturaRepository
from api.repositories.despesa_deputado import DespesaDeputadoRepository


def get_deputado_repository(session: DBSessionDep) -> DeputadoRepository:
    return DeputadoRepository(session)


DeputadoRepositoryDep = Annotated[DeputadoRepository, Depends(get_deputado_repository)]


def get_legislatura_repository(session: DBSessionDep) -> LegislaturaRepository:
    return LegislaturaRepository(session)


LegislaturaRepositoryDep = Annotated[
    LegislaturaRepository, Depends(get_legislatura_repository)
]

def get_despesa_deputado_repository(session: DBSessionDep) -> DespesaDeputadoRepository:
    return DespesaDeputadoRepository(session)


DespesaDeputadoRepositoryDep = Annotated[
    DespesaDeputadoRepository, Depends(get_despesa_deputado_repository)
]
