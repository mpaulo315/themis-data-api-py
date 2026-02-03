from fastapi import Request
from api.classes.response import PageParams, PaginatedResponse
from api.dependencies.db import DBSessionDep
from api.dependencies.repository import LegislaturaRepositoryDep
from api.repositories.legislatura import LegislaturaRepository
from typings.legislatura import LegislaturaID


class LegislaturaService:
    def __init__(self, db_session: DBSessionDep, repo: LegislaturaRepositoryDep):
        self.db_session = db_session
        self.repo = repo

    def get_all(self, request: Request, page_params: PageParams):
        return PaginatedResponse.parse_query(
            query=self.repo.get_all(),
            request_url=str(request.url),
            page_params=page_params,
        )

    def get_by_id(self, request: Request, legislatura_id: LegislaturaID):
        return PaginatedResponse.parse_query(
            query=self.repo.get_by_id(legislatura_id),
            request_url=str(request.url),
            page_params=PageParams(pagina=1, itens=10),
        )
