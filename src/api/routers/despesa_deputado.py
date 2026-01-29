from typing import Annotated
from src.api.classes.response import PageParams
from src.api.dependencies.service import DespesaDeputadoServiceDep
from src.api.repositories.despesa_deputado import DespesaDeputadoFilterParam
from fastapi import APIRouter, Depends, Request


router = APIRouter(
    tags=["Despesas de Deputados"],
)

@router.get("/")
async def read_despesas_deputados(
    request: Request,
    despesa_deputado_service: DespesaDeputadoServiceDep,
    page_params: Annotated[PageParams, Depends()],
    filter_param: Annotated[DespesaDeputadoFilterParam, Depends()],
):
    return despesa_deputado_service.get_all(filter_param, page_params, request)
