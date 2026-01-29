from typing import Annotated

from src.api.routers import despesa_deputado

from src.api.classes.response import PageParams, PaginatedResponse
from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import JSONResponse
from src.api.dependencies.service import DeputadoServiceDep
from src.api.repositories.deputado import DeputadosQueryParams

router = APIRouter(
    tags=["Deputados"],
)

router.include_router(despesa_deputado.router, prefix="/despesas")

@router.get("/")
async def read_deputados(
    request: Request,
    deputado_service: DeputadoServiceDep,
    page_params: Annotated[PageParams, Depends()],
    filter_params: Annotated[DeputadosQueryParams, Depends()],
):
    print("page_params", page_params)
    print("filter_params", filter_params)
    return deputado_service.get_all(request, page_params, filter_params)


@router.get("/{deputado_id:int}")
async def read_deputado_by_id(deputado_id: int, deputado_service: DeputadoServiceDep):
    return deputado_service.get_by_id( deputado_id)
