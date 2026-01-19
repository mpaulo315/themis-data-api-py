from datetime import datetime
from camara.resources.base import CamaraResource
from camara.types import CamaraAPIResponse
from utils import download_file
from camara.config.data_file import DEPUTADOS_URL
from pathlib import Path
import json
from camara.schemas.Deputado import Deputado as DeputadoSchema
from camara.models.Deputado import Deputado as DeputadoModel

ROOT_PATH = Path("fetcher") 

class DeputadoResource(CamaraResource):
    model = DeputadoModel
    schema = DeputadoSchema

    def fetch(self) -> CamaraAPIResponse:
        file_path = ROOT_PATH / "camara" / "data"
        download_file(DEPUTADOS_URL, file_path, "deputados.json")
        
        with open(ROOT_PATH / "camara" / "data" / "deputados.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            self.last_downloaded = datetime.now()
            
        return data


    def parse(self, response: CamaraAPIResponse) -> list[DeputadoSchema]:
        deputados = [DeputadoSchema(**d) for d in response.get("dados", [])]
        return deputados


