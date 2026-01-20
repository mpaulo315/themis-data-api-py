from fastapi import APIRouter
from sqlalchemy import select
from db.session import SessionLocal
from typings.deputado import Deputado


router = APIRouter(prefix="/deputados", tags=["Deputados"])

@router.get("/")
async def read_deputados():
    with SessionLocal() as db:
        result = db.execute(select(Deputado))
        
        return result.scalars().all()

@router.get("/{deputado_id}")
async def read_deputado_by_id(deputado_id: int):
    with SessionLocal() as db:
        result = db.execute(select(Deputado).where(Deputado.id == deputado_id))
        
        return result.scalars().first()
