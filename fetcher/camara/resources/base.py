from abc import ABC, abstractmethod
from utils import CamaraAPIResponse
from camara.db.session import Base as Model
from datetime import datetime
from croniter import croniter
from sqlalchemy.orm import Session
from sqlalchemy import insert

class CamaraResource(ABC):
    model: Model
    last_downloaded: datetime
    last_updated: datetime
    last_updated_message: str
    cron_expression: str

    def __init__(self, cron_expression: str):
        self.cron_expression = cron_expression

    def is_stale(self) -> bool:
        if not self.last_updated:
            return True
        
        cron_iter = croniter(self.cron_expression, self.last_updated)
        return cron_iter.get_next(datetime) <= datetime.now()


    @abstractmethod
    def fetch(self) -> CamaraAPIResponse:
        pass

    @abstractmethod
    def transform(self, response: CamaraAPIResponse) -> list[dict[str, any]]:
        pass
    
    # Criar alguns decorators específicos para essa função e fazer a limpeza da tabela
    # antes da inserção. Opções: Delete geral, delete por parâmetro, sem deleção
    def save(self, db: Session, data: list[dict[str, any]]) -> None:
        try:
            models = [self.model(**item) for item in data]
            db.add_all(models)
            db.commit()
            self.last_updated = datetime.now()
            self.last_updated_message = "Sucesso"
            print("Dados salvos com sucesso")
        except Exception as e:
            db.rollback()
            self.last_updated_message = str(e)
            print("Erro ao salvar dados:", e)
        finally:
            db.close()



