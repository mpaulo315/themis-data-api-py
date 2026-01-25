from fastapi import APIRouter
from sqlalchemy import select
from src.api.config.main import QUERY_LIMIT
from src.db.session import SessionLocal
from src.typings.legislatura import Legislatura

router = APIRouter(prefix="/legislaturas", tags=["Legislaturas"])


@router.get("/")
async def read_legislatura(skip: int = 0, limit: int = QUERY_LIMIT):
    with SessionLocal() as db:
        result = db.execute(select(Legislatura).offset(skip).limit(limit))
        return result.scalars().all()


@router.get("/{legislatura_id}")
async def read_legislatura_by_id(legislatura_id: int):
    with SessionLocal() as db:
        result = db.execute(
            select(Legislatura).where(Legislatura.idLegislatura == legislatura_id)
        )
        return result.scalars().first()
