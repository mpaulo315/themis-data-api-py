from typing import Annotated

from api.classes.response import PageParams
from api.auth.header_auth import check_header_auth
from fastapi import APIRouter, Depends, Request
from api.dependencies.service import LegislaturaServiceDep

router = APIRouter(
    tags=["Legislaturas"],
)


@router.get("/")
async def read_legislatura(legislatura_service: LegislaturaServiceDep, request: Request, page_params: Annotated[PageParams, Depends()]):
    return legislatura_service.get_all(request=request, page_params=page_params)


@router.get("/{legislatura_id}")
async def read_legislatura_by_id(
    legislatura_id: int, legislatura_service: LegislaturaServiceDep
):
    return legislatura_service.get_by_id(legislatura_id)
