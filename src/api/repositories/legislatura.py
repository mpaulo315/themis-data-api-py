from typing import NamedTuple
from src.api.dependencies.db import DBSessionDep
from src.api.repositories.base import BaseRepository
from src.typings.legislatura import Legislatura, LegislaturaID


class LegislaturaRepository(BaseRepository):
    def __init__(self, session: DBSessionDep):
        super().__init__(session, Legislatura)

    def get_all(self) -> NamedTuple:
        query_result = (
            self.session.query(Legislatura)
            .order_by(Legislatura.idLegislatura.desc())
            .all()
        )

        return NamedTuple(
            "ResponseListLegislatura", data=query_result, total=len(query_result)
        )

    def get_by_id(self, legislatura_id: LegislaturaID) -> NamedTuple:
        legislatura = (
            self.session.query(Legislatura)
            .filter(Legislatura.idLegislatura == legislatura_id)
            .first()
        )
        return NamedTuple(
            "ResponseLegislatura", data=legislatura, total=1 if legislatura else 0
        )
