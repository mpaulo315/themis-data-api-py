import os
from dotenv import load_dotenv
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
load_dotenv(override=True)

from api.auth.header_auth import check_header_auth
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from api.routers import deputado, legislatura, despesa_deputado
from sqlalchemy.exc import OperationalError

CORS_ORIGINS = os.getenv("CORS_ORIGINS")

app = FastAPI()
private_api = FastAPI(dependencies=[Depends(check_header_auth)])


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

private_api.include_router(legislatura.router, prefix="/legislaturas")
private_api.include_router(deputado.router, prefix="/deputados")
private_api.include_router(despesa_deputado.router, prefix="/despesa-deputado")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def test():
    raise ValueError("Teste")

app.mount("/api/v1", private_api)


# EXCEPTION HANDLERS
@private_api.exception_handler(OperationalError)
async def operational_error_handler(req, exc):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Database is not responding properly."
        }
    )

@private_api.exception_handler(HTTPException)
async def http_exception_handler(req, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail
        }
    )

@private_api.exception_handler(RequestValidationError)
async def general_exception_handler(req, exc: RequestValidationError):
    print("Entrei")
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation error",
            "count": len(exc.errors()),
            "errors": [{
                "message": e.get("msg"),
                "type": e.get("type"),
                "loc": e.get("loc")
            } for e in exc.errors()]
        }
    )

