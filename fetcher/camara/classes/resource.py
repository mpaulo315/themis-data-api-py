from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Generic, Type, TypeVar
from sqlalchemy.orm import Session
import croniter
from sqlmodel import SQLModel

from fetcher.camara.types import CamaraAPIResponse

T = TypeVar("T", bound=SQLModel)

ROOT_PATH = Path("fetcher")

class CamaraResource(Generic[T], ABC):
    model: Type[T]
    cron_expression: str

    last_updated: datetime | None = None
    last_updated_message: str | None = None

    def __init__(self, cron_expression: str):
        self.cron_expression = cron_expression

    @abstractmethod
    def fetch(self) -> CamaraAPIResponse:
        pass

    @abstractmethod
    def parse(self, response: CamaraAPIResponse) -> list[T]:
        pass

    def _bulk_save(self, session: Session, data: list[T], chunk_size: int = 5000):
        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            session.add_all(chunk)
            session.commit()

    def is_stale(self) -> bool:
        if self.last_updated is None:
            return True
        cron = croniter(self.cron_expression, self.last_updated)
        return cron.get_next(datetime) <= datetime.now()


    def save(self, session: Session, data: list[T]):
        try:
            self._bulk_save(session, data)
            self.last_updated = datetime.now()
            self.last_updated_message = "OK"
        except Exception as e:
            session.rollback()
            self.last_updated_message = str(e)
            raise
        session.refresh(data[0])
