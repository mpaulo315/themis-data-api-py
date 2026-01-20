from fastapi import FastAPI
from api.routers import legislaturas, deputados

app = FastAPI()


app.include_router(legislaturas.router)
app.include_router(deputados.router)
