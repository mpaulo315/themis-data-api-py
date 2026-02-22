from datetime import datetime
from typing import Any, Literal
from api.classes.query import GroupingQuery
from pydantic import BaseModel, Field
# from typings.deputado import DeputadoID
from api.dependencies.db import DBSessionDep
from api.repositories.base import BaseRepository
from sqlalchemy import distinct
from typings.despesa_deputado import DespesaDeputado, DespesaID
from sqlalchemy.orm import Query
from fetcher.config.data_file import MIN_ANO_DESPESAS
from sqlalchemy.sql import func


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

    def query(self, query_param: GroupingQuery):

        select_fields = []

        for group_field in query_param.group_fields_list:

            agg_func = group_field.agg_func
            field = group_field.field
            label = group_field.label

            match agg_func:
                case "max":
                    select_fields.append(
                        func.max(getattr(DespesaDeputado, field)).label(label)
                    )
                case "min":
                    select_fields.append(
                        func.min(getattr(DespesaDeputado, field)).label(label)
                    )
                case "count":
                    select_fields.append(
                        func.count(getattr(DespesaDeputado, field)).label(label)
                    )
                # Count distinct
                case "dcount":
                    select_fields.append(
                        func.count(distinct(getattr(DespesaDeputado, field))).label(label)
                    )
                case "sum":
                    select_fields.append(
                        func.sum(getattr(DespesaDeputado, field)).label(label)
                    )
                case "avg":
                    select_fields.append(
                        func.avg(getattr(DespesaDeputado, field)).label(label)
                    )
                case "stddev":
                    select_fields.append(
                        func.stddev(getattr(DespesaDeputado, field)).label(label)
                    )
                case _:
                    pass
        
        group_by_columns = [
            getattr(DespesaDeputado, field)
            for field in query_param.group_by_fields
        ]

        query = self.session.query(
            *group_by_columns,
            *select_fields
        )

        query = query.group_by(*group_by_columns)

        result = query.all()

        return [row._asdict() for row in result]
        

