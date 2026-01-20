import json
from pathlib import Path
from classes.resource import ROOT_PATH, CamaraResource
from camara.types import CamaraAPIResponse
from camara.config.data_file import LEGISLATURAS_URL
from utils import download_file
from typings.legislatura import Legislatura


class LegislaturaResource(CamaraResource[Legislatura]):
    model = Legislatura
    path = ROOT_PATH / "data" / "camara"

    def _is_downloaded(self):
        return self.path / "legislaturas.json" in Path.iterdir(self.path)
    
    def fetch(self) -> CamaraAPIResponse:
        if not self._is_downloaded():
            download_file(LEGISLATURAS_URL, self.path, "legislaturas.json")
        
        with open(self.path / "legislaturas.json", "r", encoding="utf-8") as f:
            return json.load(f)
        
    def parse(self, response: CamaraAPIResponse) -> list[Legislatura]:
        legislaturas = []

        for l in response.get("dados", []):
            legislaturas.append(self.model(**l))
        
        return legislaturas
