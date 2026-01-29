import os
from dotenv import load_dotenv


env = os.getenv("ENV", "development")

match env:
    case "development" | "dev":
        load_dotenv(dotenv_path=".env.development")
    case "production" | "prod":
        load_dotenv(dotenv_path=".env.production")
    case _:
        raise ValueError(f"Invalid environment: {env}")

from src.api.auth.header_auth import check_header_auth
from fastapi import Depends, FastAPI
from src.api.routers import deputado, legislatura, despesa_deputado

app = FastAPI()
private_api = FastAPI()

private_api.include_router(legislatura.router, prefix="/legislaturas", dependencies=[Depends(check_header_auth)])
private_api.include_router(deputado.router, prefix="/deputados", dependencies=[Depends(check_header_auth)])

@app.get("/health")
async def health():
    return {"status": "ok"}


app.mount("/api/v1", private_api)
