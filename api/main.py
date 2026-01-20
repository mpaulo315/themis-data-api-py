from fastapi import FastAPI
from api.routers import legislatura

app = FastAPI()


app.include_router(legislatura.router)

@app.get("/")
async def root():
    