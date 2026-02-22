import os
from dotenv import load_dotenv
load_dotenv(override=True)

from api.auth.header_auth import check_header_auth
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import deputado, legislatura, despesa_deputado

CORS_ORIGINS = os.getenv("CORS_ORIGINS")

app = FastAPI()
private_api = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

private_api.include_router(legislatura.router, prefix="/legislaturas", dependencies=[Depends(check_header_auth)])
private_api.include_router(deputado.router, prefix="/deputados", dependencies=[Depends(check_header_auth)])
private_api.include_router(despesa_deputado.router, prefix="/despesa-deputado", dependencies=[Depends(check_header_auth)])

@app.get("/health")
async def health():
    return {"status": "ok"}


app.mount("/api/v1", private_api)
