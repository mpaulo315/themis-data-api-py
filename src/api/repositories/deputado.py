from pydantic import BaseModel
from src.api.dependencies.db import DBSessionDep
from src.api.repositories.base import BaseRepository
from src.typings.deputado import Deputado
from src.typings.legislatura import LegislaturaID
from sqlalchemy.orm import Query


class DeputadosQueryParams(BaseModel):
    idLegislatura: LegislaturaID | None = None
    municipio: str | None = None
    uf: str | None = None

class DeputadoRepository(BaseRepository):
    def __init__(self, session: DBSessionDep):
        super().__init__(session, Deputado)

    def get_all(
        self,
        filter_params: DeputadosQueryParams,
    ) -> Query:
        query = self.session.query(Deputado)

        if filter_params.idLegislatura:
            query = query.filter(Deputado.idLegislaturaFinal == filter_params.idLegislatura)

        if filter_params.municipio:
            query = query.filter(Deputado.municipioNascimento.like(f"%{filter_params.municipio}%"))

        if filter_params.uf:
            query = query.filter(Deputado.ufNascimento == filter_params.uf)

        return query


    def get_by_id(self, idDeputado) -> Query:
        return self.session.query(Deputado).filter(Deputado.id == idDeputado)
