from src.api.dependencies.db import DBSessionDep
from src.api.dependencies.repository import LegislaturaRepositoryDep
from src.api.repositories.legislatura import LegislaturaRepository
from src.typings.legislatura import LegislaturaID


class LegislaturaService:
    def __init__(self, db_session: DBSessionDep, repo: LegislaturaRepositoryDep):
        self.db_session = db_session
        self.repo = repo

    def get_all(self):
        return self.repo.get_all()
    
    def get_by_id(self, legislatura_id: LegislaturaID):
        return self.repo.get_by_id(legislatura_id)
