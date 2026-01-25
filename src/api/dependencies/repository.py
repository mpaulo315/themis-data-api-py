from typing import Annotated
from fastapi import Depends

from api.dependencies.db import DBSessionDep
from api.repositories.deputado import DeputadoRepository


def get_deputado_repository(db: DBSessionDep) -> DeputadoRepository:
    return DeputadoRepository(db)

DeputadoRepositoryDep = Annotated[DeputadoRepository, Depends(get_deputado_repository)]
