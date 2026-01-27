from typing import Annotated
from src.api.auth.header_auth import check_header_auth
from functools import partial
from src.api.repositories.deputado import FilterParams
from src.api.typings.response import PaginatedResponse, ResponseLinks, ResponseMeta, SingleResponse
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from src.api.dependencies.service import DeputadoServiceDep
from src.api.utils.url import build_paginated_url

router = APIRouter(
    prefix="/deputados", 
    tags=["Deputados"],
    dependencies=[Depends(check_header_auth)]
)

@router.get("/", response_model=PaginatedResponse)
async def read_deputados(request: Request, deputado_service: DeputadoServiceDep, filter_params: Annotated[FilterParams, Query()]):
    response = deputado_service.get_all(filter_params)
    count = response.count
    data = response.data
    print("Total: ", count, type(count))

    base_url = str(request.url).split('?')[0]

    url_builder = partial(build_paginated_url, base_url=base_url, page_size=filter_params.page_size)
    url = url_builder(page_number=filter_params.page)
    next_link = url_builder(page_number=filter_params.page + 1) if filter_params.page * filter_params.page_size <= count else None
    prev_link = url_builder(page_number=filter_params.page - 1) if filter_params.page > 1 else None

    return JSONResponse(
        status_code=200,
        content=PaginatedResponse(
            meta=ResponseMeta(total=count, page=filter_params.page, per_page=filter_params.page_size), 
            data=data, 
            links=ResponseLinks(self=url, next=next_link, prev=prev_link)
            )
    ) 


@router.get("/{deputado_id}", response_model=SingleResponse)
async def read_deputado_by_id(request: Request, deputado_id: int, deputado_service: DeputadoServiceDep):
    data = deputado_service.get_by_id(deputado_id)

    base_url = str(request.url)

    return SingleResponse(data=data)
