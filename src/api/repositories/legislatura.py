from typing import NamedTuple
from src.api.dependencies.db import DBSessionDep
from src.api.repositories.base import BaseRepository
from src.typings.legislatura import Legislatura, LegislaturaID
from sqlalchemy.orm import Query

class LegislaturaRepository(BaseRepository):
    def __init__(self, session: DBSessionDep):
        super().__init__(session, Legislatura)

    def get_all(self) -> Query:
        query = (
            self.session.query(Legislatura)
            .order_by(Legislatura.idLegislatura.desc())
        )

        return query

    def get_by_id(self, legislatura_id: LegislaturaID) -> Query:
        query = (
            self.session.query(Legislatura)
            .filter(Legislatura.idLegislatura == legislatura_id)
        )
        return query
