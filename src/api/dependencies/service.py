from typing import Annotated
from fastapi import Depends
from api.dependencies.db import DBSessionDep
from api.dependencies.repository import DeputadoRepositoryDep
from api.services.deputado import DeputadoService


def get_deputado_service(
        db: DBSessionDep, 
        deputado_repo: DeputadoRepositoryDep
    ) -> DeputadoService:
    return DeputadoService(db, deputado_repo)

DeputadoServiceDep = Annotated[DeputadoService, Depends(get_deputado_service)]
