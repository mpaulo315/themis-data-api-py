from typing import Annotated
from fastapi import Depends
from src.api.dependencies.db import DBSessionDep
from src.api.dependencies.repository import (
    DeputadoRepositoryDep,
    DespesaDeputadoRepositoryDep,
    LegislaturaRepositoryDep,
)
from src.api.services.deputado import DeputadoService
from src.api.services.legislatura import LegislaturaService
from src.api.services.despesa_deputado import DespesaDeputadoService


def get_deputado_service(
    db: DBSessionDep, deputado_repo: DeputadoRepositoryDep
) -> DeputadoService:
    return DeputadoService(db, deputado_repo)


DeputadoServiceDep = Annotated[DeputadoService, Depends(get_deputado_service)]


def get_legislatura_service(
    db: DBSessionDep, legislatura_repo: LegislaturaRepositoryDep
) -> LegislaturaService:
    return LegislaturaService(db, legislatura_repo)


LegislaturaServiceDep = Annotated[LegislaturaService, Depends(get_legislatura_service)]

def get_despesa_deputado_service(
    db: DBSessionDep, despesa_deputado_repo: DespesaDeputadoRepositoryDep
) -> DespesaDeputadoService:
    return DespesaDeputadoService(db, despesa_deputado_repo)

DespesaDeputadoServiceDep = Annotated[DespesaDeputadoService, Depends(get_despesa_deputado_service)]
