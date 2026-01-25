from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from src.api.config.main import QUERY_FIRST_PAGE, QUERY_LIMIT


class BaseRepository:
    def __init__(self, session: Session, model: type[SQLModel]):
        self.session = session
        self.query_first_page = QUERY_FIRST_PAGE
        self.query_limit = QUERY_LIMIT
        self.model = model
