import os
from dotenv import load_dotenv

load_dotenv(override=True)

from api.auth.header_auth import check_header_auth
from fastapi import Depends, FastAPI
from api.routers import deputado, legislatura, despesa_deputado

app = FastAPI()
private_api = FastAPI()

private_api.include_router(legislatura.router, prefix="/legislaturas", dependencies=[Depends(check_header_auth)])
private_api.include_router(deputado.router, prefix="/deputados", dependencies=[Depends(check_header_auth)])

@app.get("/health")
async def health():
    return {"status": "ok"}


app.mount("/api/v1", private_api)
