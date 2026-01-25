from typing import Annotated
from fastapi import Depends

from src.api.dependencies.db import DBSessionDep
from src.api.repositories.deputado import DeputadoRepository


def get_deputado_repository(db: DBSessionDep) -> DeputadoRepository:
    return DeputadoRepository(db)

DeputadoRepositoryDep = Annotated[DeputadoRepository, Depends(get_deputado_repository)]
