from sqlalchemy.orm import Session
from sqlmodel import SQLModel


class BaseRepository:
    def __init__(self, session: Session, model: type[SQLModel]):
        self.session = session
        self.model = model
