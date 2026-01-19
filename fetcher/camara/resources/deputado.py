from datetime import datetime
from camara.resources.base import CamaraResource
from camara.types import CamaraAPIResponse
from utils import download_file
from camara.config.data_file import DEPUTADOS_URL
from pathlib import Path
import json
from camara.models.Deputado import Deputado as DeputadoModel

ROOT_PATH = Path("fetcher") 

class DeputadoResource(CamaraResource):
    model = DeputadoModel

    def _validate_data(self, value):
        if isinstance(value, str):
            if len(value) == 0:
                return None 
            return datetime.strptime(value, "%Y-%m-%d").date()
        
        return value


    def fetch(self) -> CamaraAPIResponse:
        file_path = ROOT_PATH / "camara" / "data"
        download_file(DEPUTADOS_URL, file_path, "deputados.json")
        
        with open(ROOT_PATH / "camara" / "data" / "deputados.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            self.last_downloaded = datetime.now()
            
        return data


    def transform(self, response: CamaraAPIResponse) -> list[dict[str, any]]:
        rows = []

        for d in response.get("dados", []):
            rows.append({
                **{k: v for k, v in d.items()},
                "id": int(d["uri"].split("/")[-1]),
                "idLegislaturaInicial": int(d["idLegislatura"]),
                "idLegislaturaFinal": int(d["idLegislatura"]),
                "dataNascimento": self._validate_data(d.get("dataNascimento")),
                "dataFalecimento": self._validate_data(d.get("dataFalecimento")),
            })

        return rows


