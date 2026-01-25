from fastapi import APIRouter
from sqlalchemy import select
from src.api.dependencies.service import DeputadoServiceDep
from src.db.session import SessionLocal
from src.typings.deputado import Deputado

router = APIRouter(prefix="/deputados", tags=["Deputados"])


@router.get("/")
async def read_deputados(deputado_service: DeputadoServiceDep):
    return deputado_service.get_all()

@router.get("/{deputado_id}")
async def read_deputado_by_id(deputado_id: int, deputado_service: DeputadoServiceDep):
    return deputado_service.get_by_id(deputado_id)
