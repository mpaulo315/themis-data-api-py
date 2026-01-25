from src.api.dependencies.db import DBSessionDep
from src.api.repositories.base import BaseRepository
from src.typings.legislatura import Legislatura


class LegislaturaRepository(BaseRepository):
    def __init__(self, db: DBSessionDep):
        super().__init__(db, Legislatura)
    
    def get_all(self):
        return self.db.query(Legislatura)\
            .order_by(Legislatura.idLegislatura.desc())\
            .all()
    

