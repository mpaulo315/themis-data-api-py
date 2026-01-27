from typing import Annotated

from api.classes.response import PaginatedResponse
from src.api.repositories.deputado import FilterParams
from fastapi import APIRouter, Query, Request, status
from fastapi.responses import JSONResponse
from src.api.dependencies.service import DeputadoServiceDep

router = APIRouter(
    prefix="/deputados",
    tags=["Deputados"],
)


@router.get("/")
async def read_deputados(
    request: Request,
    deputado_service: DeputadoServiceDep,
    filter_params: Annotated[FilterParams, Query()],
):
    result = deputado_service.get_all(filter_params)

    return PaginatedResponse.parse(
        data=result.get("data", []),
        page=filter_params.page,
        page_size=filter_params.page_size,
        total_count=result.get("count", 0),
        request_url=str(request.url),
    )


@router.get("/{deputado_id}")
async def read_deputado_by_id(deputado_id: int, deputado_service: DeputadoServiceDep):
    data = deputado_service.get_by_id(deputado_id)

    return JSONResponse(status_code=status.HTTP_200_OK, content=data)
