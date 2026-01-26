from api.auth.header_auth import check_header_auth
from fastapi import APIRouter, Depends
from src.api.dependencies.service import LegislaturaServiceDep

router = APIRouter(
    prefix="/legislaturas", 
    tags=["Legislaturas"],
    dependencies=[Depends(check_header_auth)]
)


@router.get("/")
async def read_legislatura(legislatura_service: LegislaturaServiceDep):
    return legislatura_service.get_all()

@router.get("/{legislatura_id}")
async def read_legislatura_by_id(legislatura_id: int, legislatura_service: LegislaturaServiceDep):
    return legislatura_service.get_by_id(legislatura_id)
