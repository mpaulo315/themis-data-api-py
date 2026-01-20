from fastapi import APIRouter
from sqlalchemy import select
from db.session import SessionLocal
from typings.legislatura import Legislatura

router = APIRouter(prefix="/legislaturas", tags=["Legislaturas"])

@router.get("/")
async def read_legislatura():
    with SessionLocal() as db:
        result = db.execute(select(Legislatura))
        
        return result.scalars().all()

@router.get("/{legislatura_id}")
async def read_legislatura_by_id(legislatura_id: int):
    with SessionLocal() as db:
        result = db.execute(
            select(Legislatura).where(Legislatura.idLegislatura == legislatura_id)
        )
        return result.scalars().first()
