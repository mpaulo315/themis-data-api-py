from typing import Annotated
from fastapi import Depends

from src.api.dependencies.db import DBSessionDep
from src.api.repositories.deputado import DeputadoRepository
from src.api.repositories.legislatura import LegislaturaRepository


def get_deputado_repository(session: DBSessionDep) -> DeputadoRepository:
    return DeputadoRepository(session)

DeputadoRepositoryDep = Annotated[DeputadoRepository, Depends(get_deputado_repository)]

def get_legislatura_repository(session: DBSessionDep) -> LegislaturaRepository:
    return LegislaturaRepository(session)

LegislaturaRepositoryDep = Annotated[LegislaturaRepository, Depends(get_legislatura_repository)]
