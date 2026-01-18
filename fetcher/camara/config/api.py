from typing import Callable

BASE_URL = "https://dados.camara.leg.br/api/v2/"

DESPESAS_URL_BUILDER: Callable[[int], str] = lambda ano: f"http://www.camara.leg.br/cotas/Ano-{ano}.json.zip"

