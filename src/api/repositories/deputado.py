import src.api.config.main as query_config
from pydantic import BaseModel, Field
from src.api.dependencies.db import DBSessionDep
from src.api.repositories.base import BaseRepository
from src.typings.deputado import Deputado
from src.typings.legislatura import LegislaturaID


class FilterParams(BaseModel):
    page_size: int = Field(
        query_config.QUERY_LIMIT,
        gt=query_config.QUERY_MIN_LIMIT,
        le=query_config.QUERY_MAX_LIMIT,
    )
    page: int = Field(query_config.QUERY_FIRST_PAGE, ge=0)


class DeputadoRepository(BaseRepository):
    def __init__(self, session: DBSessionDep):
        super().__init__(session, Deputado)

    def get_all(
        self,
        filter_params: FilterParams,
        idLegislatura: LegislaturaID | None = None,
        municipio: str | None = None,
        uf: str | None = None,
    ) -> dict:
        query = self.session.query(Deputado)

        if idLegislatura:
            query = query.filter(Deputado.idLegislaturaFinal == idLegislatura)

        if municipio:
            query = query.filter(Deputado.municipioNascimento.like(f"%{municipio}%"))

        if uf:
            query = query.filter(Deputado.ufNascimento == uf)

        count = query.count()

        query_result = (
            query.offset(filter_params.page * filter_params.page_size)
            .limit(filter_params.page_size)
            .all()
        )
        return {"data": [x.model_dump() for x in query_result], "count": count}

    def get_by_id(self, idDeputado) -> dict:
        query_result = (
            self.session.query(Deputado).filter(Deputado.id == idDeputado).first()
        )
        return {"data": query_result.model_dump() if query_result else None}
