import httpx
from pathlib import Path
from fetcher.decorators.log import log

@log
def download_file(url: str, save_path: str) -> None:
    with httpx.stream("GET", url) as response:
        response.raise_for_status()
        with open(Path(save_path), "wb") as file:
            for chunk in response.iter_bytes():
                file.write(chunk)

@log
def fetch_data(url: str) -> dict:
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()
