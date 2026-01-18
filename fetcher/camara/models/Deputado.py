from pydantic import BaseModel, Field
from Legislatura import LegislaturaID
from typing import Annotated, Optional

DeputadoID = int

class DeputadoAPIGeneral(BaseModel):
    id: DeputadoID
    uri: Annotated[str, Field(description="URI do deputado")]
    nome: str
    siglaPartido: str
    uriPartido: str
    siglaUf: str
    idLegislatura: LegislaturaID
    urlFoto: str

class DeputadoAPI(BaseModel):
    id: DeputadoID
    uri: Annotated[str, Field(description="URI do deputado")]
    nomeCivil: str
    urlWebsite: Optional[str]
    redeSocial: Optional[list[str]]
    dataNascimento: str
    dataFalecimento: Optional[str]
    ufNascimento: str
    municipioNascimento: str
    escolaridade: str

class DeputadoJSON(BaseModel):
    id: DeputadoID
    uri: Annotated[str, Field(description="URI do deputado")]
    nome: str
    idLegislaturaInicial: LegislaturaID
    idLegislaturaFinal: LegislaturaID
    nomeCivil: str
    siglaSexo: str
    urlRedeSocial: list[str]
    urlWebsite: list[str]
    dataNascimento: str
    dataFalecimento: str
    ufNascimento: str
    municipioNascimento: str
