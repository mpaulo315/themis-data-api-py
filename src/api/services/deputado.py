from typing import NamedTuple
from src.api.repositories.deputado import FilterParams
from sqlalchemy.sql.expression import func

from src.api.dependencies.db import DBSessionDep
from src.api.dependencies.repository import DeputadoRepositoryDep
from src.typings.legislatura import Legislatura

class DeputadoService:
    def __init__(self, db_session: DBSessionDep, repo: DeputadoRepositoryDep):
        self.db_session = db_session
        self.repo = repo

    def get_all(self, filter_params: FilterParams) -> NamedTuple:
        ultima_legislatura = self.db_session.query(func.max(Legislatura.idLegislatura)).scalar()
        
        if ultima_legislatura is None:
            return []

        return self.repo.get_all(idLegislatura=ultima_legislatura, filter_params=filter_params)

    def get_by_id(self, idDeputado) -> NamedTuple:
        return self.repo.get_by_id(idDeputado)
