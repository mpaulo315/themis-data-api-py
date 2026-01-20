from camara.models.Despesas import Despesas as DespesaModel
from camara.resources.base import CamaraResource
from camara.types import CamaraAPIResponse
from pathlib import Path
from datetime import datetime
from camara.config.data_file import DESPESAS_URL_BUILDER
from utils import download_file
from zipfile import ZipFile
import json
from io import TextIOWrapper

ROOT_PATH = Path("fetcher")

class DespesasResource(CamaraResource):
    model = DespesaModel

    def _validate_data(self, value):
        if isinstance(value, str):
            if len(value) == 0:
                return None
            return datetime.strptime(value.split("T")[0], "%Y-%m-%d").date()
        
        return value
    
    def fetch(self) -> CamaraAPIResponse:
        ano = 2025
        file_path = ROOT_PATH / "camara" / "data"
        download_file(DESPESAS_URL_BUILDER(ano), file_path, f"Ano-{ano}.zip")

        with ZipFile(file_path / f"Ano-{ano}.zip", 'r') as zip_file:
            with zip_file.open(f'Ano-{ano}.json', 'r') as json_file:
                t = TextIOWrapper(json_file, encoding="utf-8")
                data = json.load(t)
                self.last_downloaded = datetime.now()
                
        return data
    
    def transform(self, response: CamaraAPIResponse) -> list[dict[str, any]]:
        rows = []
        for d in response.get("dados", []):
            rows.append({
                "idDocumento": int(d.get("idDocumento")) if d.get("idDocumento") else None,
                "mes": int(d.get("mes")) if d.get("mes") else None,
                "ano": int(d.get("ano")) if d.get("ano") else None,
                "codigoLegislatura": int(d.get("codigoLegislatura")) if d.get("codigoLegislatura") else None,
                "nomeParlamentar": d.get("nomeParlamentar"),
                "idDeputado": int(d.get("idDeputado")) if d.get("idDeputado") else None,
                "descricao": d.get("descricao"),
                "fornecedor": d.get("fornecedor"),
                "dataEmissao": self._validate_data(d.get("dataEmissao")),
                "valorDocumento": float(d.get("valorDocumento")) if d.get("valorDocumento") else None,
                "valorGlosa": float(d.get("valorGlosa")) if d.get("valorGlosa") else None,
                "valorLiquido": float(d.get("valorLiquido")) if d.get("valorLiquido") else None,
                "restituicao": float(d.get("restituicao")) if d.get("restituicao") else None,
                "datPagamentoRestituicao": self._validate_data(d.get("datPagamentoRestituicao")) if d.get("datPagamentoRestituicao") else None,
                "tipoDocumento": int(d.get("tipoDocumento")) if d.get("tipoDocumento") else None,
                "urlDocumento": d.get("urlDocumento"),
                "passageiro": d.get("passageiro"),
                "trecho": d.get("trecho"),
            })

        return rows
