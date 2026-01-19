import httpx
from pathlib import Path
from decorators.log import log
from typing import Any
from os import makedirs

@log
def download_file(url: str, save_path: str, file_name: str) -> None:
    with httpx.stream("GET", url) as response:
        response.raise_for_status()
        makedirs(save_path, exist_ok=True)
        with open(Path(save_path) / file_name, "wb") as file:
            for chunk in response.iter_bytes():
                file.write(chunk)

class CamaraAPIResponse[T]:
    dados: T
    links: dict[str, str]

@log
def fetch_data[T = list[Any]](url: str) -> CamaraAPIResponse[T]:
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()
