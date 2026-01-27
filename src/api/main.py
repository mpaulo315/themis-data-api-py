from src.api.auth.header_auth import check_header_auth
from dotenv import load_dotenv
import os

load_dotenv()
ENV_MODE = os.getenv("ENV_MODE", "development")

if ENV_MODE in ("production", "prod"):
    load_dotenv(dotenv_path=".env.production", override=True)
else:
    load_dotenv(dotenv_path=".env.development", override=True)

from fastapi import APIRouter, Depends, FastAPI
from src.api.routers import deputado, legislatura

app = FastAPI()
private_api = FastAPI()

private_api.include_router(legislatura.router, dependencies=[Depends(check_header_auth)])
private_api.include_router(deputado.router, dependencies=[Depends(check_header_auth)])

@app.get("/health")
async def health():
    return {"status": "ok"}


app.mount("/api/v1", private_api)
