from api.repositories.despesa_deputado import DespesaDeputadoFilterParam
from fastapi import Request
from api.dependencies.db import DBSessionDep
from api.dependencies.repository import DespesaDeputadoRepositoryDep
from api.classes.response import PageParams, PaginatedResponse


class DespesaDeputadoService:
    def __init__(self, db_session: DBSessionDep, repo: DespesaDeputadoRepositoryDep):
        self.db_session = db_session
        self.repo = repo

    def get_all(self, filter_param: DespesaDeputadoFilterParam, page_params: PageParams, request: Request):
        return PaginatedResponse.parse_query(
            query=self.repo.get_all(filter_param),
            page_params=page_params,
            request_url=str(request.url)
        )
    
