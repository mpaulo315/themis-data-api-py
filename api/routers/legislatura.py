from fastapi import APIRouter

router = APIRouter(prefix="/legislatura", tags=["legislatura"])

@router.get("/")
async def read_legislatura():
    return ["2023", "2024"]

@router.get("/{legislatura_id}")
async def read_legislatura_by_id(legislatura_id: int):
    return {"legislatura_id": legislatura_id}
