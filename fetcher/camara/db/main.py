from pydantic import Database
from schemas.Deputado import Deputado

DATABASE_URL = "sqlite:///db.sqlite3"
db = Database(DATABASE_URL)
