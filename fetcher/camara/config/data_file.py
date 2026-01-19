
from typing import Callable

DESPESAS_URL_BUILDER: Callable[[int], str] = lambda ano: f"https://www.camara.leg.br/cotas/Ano-{ano}.json.zip"

DEPUTADOS_URL = "https://dadosabertos.camara.leg.br/arquivos/deputados/json/deputados.json"

LEGISLATURAS_URL = "https://dadosabertos.camara.leg.br/arquivos/legislaturas/json/legislaturas.json"