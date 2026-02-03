from functools import partial
from math import ceil
from typing import TypeVar
from api.utils.url import build_paginated_url
from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Query
from functools import wraps
from api.config.main import QUERY_MIN_LIMIT, QUERY_LIMIT, QUERY_MAX_LIMIT
from sqlalchemy.orm import Query


class PageParams(BaseModel):
    pagina: int = Field(default=0, ge=0, description="Número da página (começando em 0)")
    itens : int = Field(default=QUERY_LIMIT, gt=QUERY_MIN_LIMIT, le=QUERY_MAX_LIMIT, description="Número de itens por página")


T= TypeVar('T', bound=BaseModel)

class PaginatedResponse(BaseModel):
    data: list[T]
    meta: dict  
    links: dict

    @classmethod
    def parse_query(cls, request_url: str, query: Query, page_params: PageParams):
        total_count = query.count()

        if total_count == 0:
            return cls(data=[], meta={}, links={})
        
        query_result = query.limit(page_params.itens).offset(page_params.pagina * page_params.itens).all()
        
        base_url = request_url.split("?")[0].rstrip("/")
        url_builder = partial(
                        build_paginated_url, 
                        base_url=base_url, 
                        page_size=page_params.itens
                        )
        
        self_link = url_builder(page_number=page_params.pagina)


        prev_link = url_builder(page_number=page_params.pagina - 1) if page_params.pagina > 1 else None
        next_link = url_builder(page_number=page_params.pagina + 1) if page_params.pagina < ceil(total_count / page_params.itens) - 1 else None

        return cls(
            data=query_result,
            meta={
                "pagina": page_params.pagina,
                "itens": min(page_params.itens, len(query_result)),
                "total": total_count,
            },
            links={"self": self_link, "prev": prev_link, "next": next_link},
        )
