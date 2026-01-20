from datetime import date, datetime
from typing import Optional
from pydantic import computed_field, field_validator
from sqlmodel import SQLModel, Field

from typings.legislatura import LegislaturaID

DeputadoID = int

class Deputado(SQLModel, table=True):
    __tablename__ = "deputados"
    # __table_args__ = {"schema": "camara"}

    @field_validator("dataNascimento", "dataFalecimento", mode="before")
    @classmethod
    def validate_data(cls, value):
        if value is None or not isinstance(value, str):
            return None
        return datetime.strptime(value.split("T")[0], "%Y-%m-%d").date()

    @field_validator("id", mode="before")
    @classmethod
    def extract_id_from_uri(cls, value, info):
        if value is None and "uri" in info.data:
            return int(info.data["uri"].split("/")[-1])
        return value
    
    id: DeputadoID = Field(primary_key=True, index=True)
    uri: str
    nome: str = Field(index=True)
    nomeCivil: str = Field(index=True)
    siglaSexo: str = Field(index=True)

    idLegislaturaInicial: LegislaturaID = Field(foreign_key="legislaturas.idLegislatura", index=True)
    idLegislaturaFinal: LegislaturaID = Field(foreign_key="legislaturas.idLegislatura", index=True)

    ufNascimento: str = Field(index=True)
    municipioNascimento: str = Field(index=True)
    dataNascimento: Optional[date] = None
    dataFalecimento: Optional[date] = None
