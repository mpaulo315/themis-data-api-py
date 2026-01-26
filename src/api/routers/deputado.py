from api.auth.header_auth import check_header_auth
from fastapi import APIRouter, Depends
from src.api.dependencies.service import DeputadoServiceDep

router = APIRouter(
    prefix="/deputados", 
    tags=["Deputados"],
    dependencies=[Depends(check_header_auth)]
)


@router.get("/")
async def read_deputados(deputado_service: DeputadoServiceDep):
    return deputado_service.get_all()

@router.get("/{deputado_id}")
async def read_deputado_by_id(deputado_id: int, deputado_service: DeputadoServiceDep):
    return deputado_service.get_by_id(deputado_id)
