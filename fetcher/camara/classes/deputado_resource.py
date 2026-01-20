from pathlib import Path
import json

from classes.resource import ROOT_PATH, CamaraResource
from camara.config.data_file import DEPUTADOS_URL
from fetcher.camara.types import CamaraAPIResponse
from utils import download_file
from typings.deputado import Deputado

class DeputadoResource(CamaraResource[Deputado]):
    model = Deputado
    path = ROOT_PATH  / "data" / "camara"

    def _is_downloaded(self):
        return self.path / "deputados.json" in Path.iterdir(self.path)
    
    def fetch(self) -> CamaraAPIResponse:
        if not self._is_downloaded():
            download_file(DEPUTADOS_URL, self.path, "deputados.json")           

        with open(self.path / "deputados.json", "r", encoding="utf-8") as f:
            return json.load(f)
    
    def parse(self, response: CamaraAPIResponse) -> list[Deputado]:
        deputados = []

        for d in response.get("dados", []):
            deputados.append(self.model(**d))
            
        return deputados
