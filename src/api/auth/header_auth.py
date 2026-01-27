from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
import os
from uuid import UUID


async def check_header_auth(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
        )
