from sqlalchemy.sql.expression import func

from src.api.dependencies.db import DBSessionDep
from src.api.dependencies.repository import DeputadoRepositoryDep
from src.typings.legislatura import Legislatura

class DeputadoService:
    def __init__(self, db_session: DBSessionDep, repo: DeputadoRepositoryDep):
        self.db_session = db_session
        self.repo = repo

    def get_all(self):
        ultima_legislatura = self.db_session.query(func.max(Legislatura.idLegislatura)).scalar()
        
        if ultima_legislatura is None:
            return []

        return self.repo.get_all(idLegislatura=ultima_legislatura)

    def get_by_id(self, id):
        return self.repo.get_by_id(id)
