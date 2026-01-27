from functools import partial
from math import ceil
from src.api.utils.url import build_paginated_url
from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    @classmethod
    def parse(
        cls, data: list, page: int, page_size: int, total_count: int, request_url: str
    ):
        base_url = request_url.split("?")[0].rstrip("/")

        url_builder = partial(
            build_paginated_url, base_url=base_url, page_size=page_size
        )
        self_link = url_builder(page_number=page)
        prev_link = url_builder(page_number=page - 1) if page > 1 else None
        next_link = (
            url_builder(page_number=page + 1)
            if page < ceil(total_count / page_size) - 1
            else None
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "data": data,
                "links": {"self": self_link, "prev": prev_link, "next": next_link},
                "meta": {
                    "page": page,
                    "page_size": min(page_size, len(data)),
                    "total_count": total_count,
                },
            },
        )
