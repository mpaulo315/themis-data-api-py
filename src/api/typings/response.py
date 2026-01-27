from collections import namedtuple
from typing import Any, Literal, NamedTuple, TypeVar

class ResponseLinks(NamedTuple):
    self: str
    next: str | None
    prev: str | None

class ResponseMeta(NamedTuple):
    total: int
    page: int
    per_page: int

class GeneralResponse(NamedTuple):
    status: int
    message: str

class ErrorResponse(GeneralResponse):
    pass

class SingleResponse(NamedTuple):
    data: Any | None

class PaginatedResponse(NamedTuple):
    data: list
    links: ResponseLinks
    meta: ResponseMeta

ListResult = namedtuple("ListResponse", ["data", "count"])
