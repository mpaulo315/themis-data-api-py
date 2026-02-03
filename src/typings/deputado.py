from datetime import date, datetime
from typing import Any
from pydantic import field_serializer, field_validator, model_validator
from sqlmodel import SQLModel, Field

from typings.legislatura import LegislaturaID

DeputadoID = int


class Deputado(SQLModel, table=True):
    __tablename__ = "deputados"

    @model_validator(mode="before")
    @classmethod
    def normalize_and_derive(cls, data):
        if isinstance(data, cls):
            return data

        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")

        data = {
            k: (None if isinstance(v, str) and not v.strip() else v)
            for k, v in data.items()
        }

        if data.get("uri") is not None:
            data["id"] = int(data["uri"].split("/")[-1])

            return data

        raise ValueError(f"Invalid data: {data}")

    @field_validator("dataNascimento", "dataFalecimento", mode="before")
    @classmethod
    def validate_data(cls, value):
        if not isinstance(value, str):
            return None

        return datetime.strptime(value.strip().split("T")[0], "%Y-%m-%d").date()

    id: DeputadoID | None = Field(default=None)
    uri: str = Field(primary_key=True)
    nome: str = Field(index=True)
    nomeCivil: str = Field(index=True)
    siglaSexo: str = Field(index=True)

    idLegislaturaInicial: LegislaturaID = Field(
        foreign_key="legislaturas.idLegislatura", index=True
    )
    idLegislaturaFinal: LegislaturaID = Field(
        foreign_key="legislaturas.idLegislatura", index=True
    )

    @field_serializer("dataNascimento", "dataFalecimento")
    def serialize_date(self, value: Any):
        if value is None:
            return None
        return str(value)

    ufNascimento: str | None = Field(index=True)
    municipioNascimento: str | None = Field(index=True)
    dataNascimento: date | None = Field(default=None)
    dataFalecimento: date | None = Field(default=None)
