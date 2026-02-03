from typing import Annotated
from api.classes.response import PageParams
from api.dependencies.service import DespesaDeputadoServiceDep
from api.repositories.despesa_deputado import DespesaDeputadoFilterParam
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
