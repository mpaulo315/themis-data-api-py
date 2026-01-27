from src.api.typings.response import Links
from fastapi.responses import JSONResponse


async def format_response(request, call_next):
    response = await call_next(request)

    if response.status_code == 200:
        data = response.json()

        if "type" in data:
            match data["type"]:
                case "dict":

                    links = Links(
                        self=request.url,
                        next_link=None,
                        prev_link=None,
                    )

                    return JSONResponse(content=data, status_code=200)
                case "list":
                    return JSONResponse(content=data, status_code=200)
        else:
            return JSONResponse(data=data, status_code=200)
    else:
        return response
