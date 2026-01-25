from os import getenv
import dotenv

dotenv.load_dotenv(".env.prod")

DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_DATABASE = getenv("DB_DATABASE")
DB_PORT = getenv("DB_PORT")
DB_HOST = getenv("DB_HOST")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
