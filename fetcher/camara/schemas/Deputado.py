from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator
from camara.schemas.Legislatura import LegislaturaID
from typing import Annotated
from datetime import date, datetime

DeputadoID = int

class Deputado(BaseModel):

    @field_validator('dataFalecimento', 'dataNascimento', mode='before')
    @classmethod
    def validate_data(cls, value):
        if isinstance(value, str):
            if len(value) == 0:
                return None
            return datetime.strptime(value, "%Y-%m-%d").date()
        
        return value

    @computed_field
    @property
    def id(self) -> DeputadoID:
        return int(self.uri.split("/")[-1])

    uri: Annotated[str, Field(description="URI do deputado")]
    nome: str
    nomeCivil: str
    siglaSexo: str
    idLegislaturaInicial: LegislaturaID
    idLegislaturaFinal: LegislaturaID
    ufNascimento: str
    municipioNascimento: str
    dataNascimento: date | None
    dataFalecimento: date | None

    model_config = ConfigDict(from_attributes=True)
