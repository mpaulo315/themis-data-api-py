from pathlib import Path
from config.data_file import LEGISLATURAS_URL   
from datetime import datetime
from utils import download_file
from schemas.Legislatura import Legislatura
import json

ROOT_PATH = Path("fetcher")

def fetch_legislaturas():
    date = datetime.now().strftime("%Y-%m-%d")
    file_path = ROOT_PATH / "camara" / "data" / date
    download_file(LEGISLATURAS_URL, file_path, "legislaturas")


def transform_legislaturas():
    with open(ROOT_PATH / "camara" / "data" / "legislaturas.json", "r") as f:
        data = json.load(f)

    legislaturas = [Legislatura(**l) for l in data]
    return legislaturas
