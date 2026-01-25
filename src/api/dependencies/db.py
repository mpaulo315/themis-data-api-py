from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.session import SessionLocal


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

DBSessionDep = Annotated[Session, Depends(get_db_session)]
