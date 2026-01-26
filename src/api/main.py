from dotenv import load_dotenv
import os

load_dotenv()
ENV_MODE = os.getenv("ENV_MODE", "development")

if ENV_MODE in ("production", "prod"):
    load_dotenv(dotenv_path=".env.production", override=True)
else:
    load_dotenv(dotenv_path=".env.development", override=True)

from fastapi import FastAPI
from src.api.routers import deputado, legislatura

app = FastAPI()

app.include_router(legislatura.router)
app.include_router(deputado.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
