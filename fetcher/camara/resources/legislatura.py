from pathlib import Path
from camara.config.data_file import LEGISLATURAS_URL   
from utils import download_file
from camara.schemas.Legislatura import Legislatura
import json

ROOT_PATH = Path("fetcher")

def fetch_legislaturas():
    file_path = ROOT_PATH / "camara" / "data"
    download_file(LEGISLATURAS_URL, file_path, "legislaturas.json")


def transform_legislaturas():
    with open(ROOT_PATH / "camara" / "data" / "legislaturas.json", "r") as f:
        data = json.load(f)

    legislaturas = [Legislatura(**l) for l in data.get("dados", [])]
    return legislaturas
