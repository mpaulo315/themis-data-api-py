from sqlmodel import Session
from api.dependencies.db import DBSessionDep
from api.repositories.base import BaseRepository
from typings.deputado import Deputado
from typings.legislatura import Legislatura, LegislaturaID


class DeputadoRepository(BaseRepository):
    def __init__(self, session: DBSessionDep):
        super().__init__(session, Deputado)
    

    def get_all(self, idLegislatura: LegislaturaID | None = None, municipio: str | None = None, uf: str | None = None):
        query = self.session.query(Deputado)

        if idLegislatura:
            query = query.filter(Deputado.idLegislaturaFinal == idLegislatura)
        
        if municipio:
            query = query.filter(Deputado.municipioNascimento.like(f'%{municipio}%'))
        
        if uf:
            query = query.filter(Deputado.ufNascimento == uf)
        
        total = query.count()
        query_result = (
            query
            .offset(self.query_first_page * self.query_limit)
            .limit(self.query_limit)
            .all()
        )
        return query_result

    def get_by_id(self, idDeputado):
        query_result = self.session.query(Deputado).filter(Deputado.id == idDeputado).first()
        return query_result, 1 if query_result else 0
