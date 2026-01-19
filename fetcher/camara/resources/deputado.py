from datetime import datetime
from utils import download_file
from camara.config.data_file import DEPUTADOS_URL
from pathlib import Path
import json
from schemas.Deputado import Deputado


ROOT_PATH = Path("fetcher") 

def fetch_deputados():
    date = datetime.now().strftime("%Y-%m-%d")
    file_path = ROOT_PATH / "camara" / "data" / date
    download_file(DEPUTADOS_URL, file_path, "deputados")

def transform_deputados():
    with open(ROOT_PATH / "camara" / "data" / "deputados.json", "r") as f:
        data = json.load(f)

    deputados = [Deputado(**d) for d in data]
    return deputados

