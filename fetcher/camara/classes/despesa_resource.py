import json
from pathlib import Path
from zipfile import ZipFile
from classes.resource import ROOT_PATH, CamaraResource
from camara.config.data_file import DESPESAS_URL_BUILDER, MIN_ANO_DESPESAS
from camara.types import CamaraAPIResponse
from utils import download_file
from typings.despesa import Despesa
from io import TextIOWrapper


class DespesaResource(CamaraResource[Despesa]):
    model = Despesa
    path = ROOT_PATH / "data" / "camara"

    def _is_downloaded(self):
        return self.path / "despesas.json" in Path.iterdir(self.path)
    
    def fetch(self) -> CamaraAPIResponse:
        year = MIN_ANO_DESPESAS
        if not self._is_downloaded():
            download_file(DESPESAS_URL_BUILDER(year), self.path, f"Ano-{year}.zip")

        with ZipFile(self.path / f"Ano-{year}.zip", 'r') as zip_file:
            with zip_file.open(f'Ano-{year}.json', 'r') as json_file:
                t = TextIOWrapper(json_file, encoding="utf-8")
                return json.load(t)
        
    def parse(self, response: CamaraAPIResponse) -> list[Despesa]:
        rows = []
        for despesa in response.get("dados", []):
            rows.append(self.model(**despesa))
        return rows

    

