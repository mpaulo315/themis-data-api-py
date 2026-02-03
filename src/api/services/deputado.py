from typing import NamedTuple

from api.repositories.deputado import DeputadosQueryParams

from api.classes.response import PageParams, PaginatedResponse
from fastapi import HTTPException, Request
from sqlalchemy.sql.expression import func

from api.dependencies.db import DBSessionDep
from api.dependencies.repository import DeputadoRepositoryDep
from typings.legislatura import Legislatura


class DeputadoService:
    def __init__(self, db_session: DBSessionDep, repo: DeputadoRepositoryDep):
        self.db_session = db_session
        self.repo = repo

    def get_all(self, request: Request, page_params: PageParams, filter_params: DeputadosQueryParams) -> dict:
        ultima_legislatura = self.db_session.query(
            func.max(Legislatura.idLegislatura)
        ).scalar()

        if ultima_legislatura is None:
            raise HTTPException(status_code=404, detail="Nenhuma legislatura encontrada")

        query = self.repo.get_all(
            filter_params=DeputadosQueryParams(
                idLegislatura=filter_params.idLegislatura if filter_params.idLegislatura is not None else ultima_legislatura,
                municipio=filter_params.municipio if filter_params.municipio is not None else None,
                uf=filter_params.uf if filter_params.uf is not None else None,
            ),
        )

        return PaginatedResponse.parse_query(
            request_url=str(request.url),
            query=query,
            page_params=page_params
        )

    def get_by_id(self, request: Request, idDeputado) -> dict:
        query_result = self.repo.get_by_id(idDeputado).scalar()

        if query_result is None:
            raise HTTPException(status_code=404, detail="Deputado não encontrado")

        return PaginatedResponse.parse_query(
            request_url=str(request.url),
            query=query_result,
            page_params=PageParams(page=1, size=1)
        )
