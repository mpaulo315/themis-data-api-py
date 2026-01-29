from fastapi import Request
from src.api.classes.response import PageParams, PaginatedResponse
from src.api.dependencies.db import DBSessionDep
from src.api.dependencies.repository import LegislaturaRepositoryDep
from src.api.repositories.legislatura import LegislaturaRepository
from src.typings.legislatura import LegislaturaID


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
