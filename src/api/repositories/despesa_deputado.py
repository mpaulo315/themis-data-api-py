from datetime import datetime
from pydantic import BaseModel, Field
# from typings.deputado import DeputadoID
from api.dependencies.db import DBSessionDep
from api.repositories.base import BaseRepository
from typings.despesa_deputado import DespesaDeputado, DespesaID
from sqlalchemy.orm import Query
from fetcher.config.data_file import MIN_ANO_DESPESAS

CURRENT_YEAR = datetime.now().year

class DespesaDeputadoFilterParam(BaseModel):
    deputado_id: int | None = Field(None, description="ID do deputado")
    ano: int | None = Field(None, ge=MIN_ANO_DESPESAS, le=CURRENT_YEAR, description="Ano da despesa")
    mes: int | None = Field(None, ge=1, le=12, description="Mês da despesa")


class DespesaDeputadoRepository(BaseRepository):
    def __init__(self, session: DBSessionDep):
        super().__init__(session, DespesaDeputado)

    def get_all(self, filter_param: DespesaDeputadoFilterParam) -> Query:
        query = self.session.query(DespesaDeputado)

        if filter_param.deputado_id:
            query = query.filter(DespesaDeputado.idDeputado == filter_param.deputado_id)
        if filter_param.ano:
            query = query.filter(DespesaDeputado.ano == filter_param.ano)
        if filter_param.mes:
            query = query.filter(DespesaDeputado.mes == filter_param.mes)
        return query
    
    def get_by_id(self, idDespesa: DespesaID) -> Query:
        return self.session.query(DespesaDeputado).filter(DespesaDeputado.id == idDespesa)
