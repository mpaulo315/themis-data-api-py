from fastapi import FastAPI
from src.api.routers import deputado, legislatura

app = FastAPI()

app.include_router(legislatura.router)
app.include_router(deputado.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
