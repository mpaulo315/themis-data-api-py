from typing import Iterable, TypeVar
from sqlalchemy import insert
from sqlalchemy.orm import Session
from sqlmodel import SQLModel

T = TypeVar("T", bound=SQLModel)

class DatabaseStorage:
    CHUNK_SIZE = 2

    @classmethod
    def bulk_insert(cls, session: Session, model: type[SQLModel], items: Iterable[T]):
        table = model.__table__
        
        try:
            for i in range(0, len(items), cls.CHUNK_SIZE):
                payload = items[i:i+cls.CHUNK_SIZE]
                session.add_all(payload)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
