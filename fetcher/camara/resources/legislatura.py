from pathlib import Path
from camara.config.data_file import LEGISLATURAS_URL   
from utils import download_file
from camara.models.Legislatura import Legislatura as LegislaturaModel
import json
from camara.resources.base import CamaraResource
from camara.types import CamaraAPIResponse
from datetime import datetime

import json

ROOT_PATH = Path("fetcher")

class LegislaturaResource(CamaraResource):
    model = LegislaturaModel

    def _validate_data(self, value):
        if isinstance(value, str):
            if len(value) == 0:
                return None
            return datetime.strptime(value, "%Y-%m-%d").date()
        
        return value

    def fetch(self) -> CamaraAPIResponse:
        file_path = ROOT_PATH / "camara" / "data"
        download_file(LEGISLATURAS_URL, file_path, "legislaturas.json")

        with open(ROOT_PATH / "camara" / "data" / "legislaturas.json", "r") as f:
            data = json.load(f)
            self.last_downloaded = datetime.now()
        
        return data

    def transform(self, response: CamaraAPIResponse) -> list[dict[str, any]]:
        rows = []

        for l in response.get("dados", []):
            rows.append({
                **{k: v for k, v in l.items()},
                "idLegislatura": int(l["idLegislatura"]),
                "dataInicio":  self._validate_data(l["dataInicio"]),
                "dataFim": self._validate_data(l["dataFim"]),
                "anoEleicao": int(l["anoEleicao"]),
            })
        return rows
