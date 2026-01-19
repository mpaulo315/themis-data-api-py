from typing import Callable

BASE_URL = "https://dados.camara.leg.br/api/v2/"

DEPUTADOS_URL = BASE_URL + "deputados"

DEPUTADO_URL_BUILDER: Callable[[int], str] = lambda id: f"{DEPUTADOS_URL}/{id}"
