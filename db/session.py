from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.db import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
