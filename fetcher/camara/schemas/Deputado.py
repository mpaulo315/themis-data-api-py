from pydantic import BaseModel, ConfigDict, HttpUrl, Field, computed_field
from Legislatura import LegislaturaID
from typing import Annotated
from datetime import date

DeputadoID = int

class Deputado(BaseModel):

    @computed_field
    @property
    def id(self) -> DeputadoID:
        return int(self.uri.split("/")[-1])

    uri: Annotated[HttpUrl, Field(description="URI do deputado")]
    nome: str
    idLegislaturaInicial: LegislaturaID
    idLegislaturaFinal: LegislaturaID
    nomeCivil: str
    siglaSexo: str
    # urlRedeSocial: list[HttpUrl]
    # urlWebsite: list[HttpUrl]
    dataNascimento: date
    dataFalecimento: date
    ufNascimento: str
    municipioNascimento: str

    model_config = ConfigDict(from_attributes=True)
