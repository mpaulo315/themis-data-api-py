from datetime import date, datetime
from typing import Optional
from pydantic import field_validator, model_validator
from sqlmodel import Field, SQLModel

from typings.deputado import DeputadoID
from typings.legislatura import LegislaturaID

DespesaID = int

class DespesaDeputado(SQLModel, table = True):
    __tablename__ = "despesas"
    # __table_args__ = {"schema": "camara"}

    @model_validator(mode="before")
    @classmethod
    def normalize_empty_string(cls, values):
        for key, value in values.items():
            if value == "":
                values[key] = None
        return values

    @field_validator("dataEmissao", "datPagamentoRestituicao", mode="before")
    @classmethod
    def validate_data(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value.split("T")[0], "%Y-%m-%d").date()
        return value

    id: DespesaID | None = Field(primary_key=True, index=True)
    idDocumento: int = Field(index=True)
    mes : int = Field(index=True)
    ano: int = Field(index=True)
    codigoLegislatura: LegislaturaID = Field(foreign_key="legislaturas.idLegislatura", index=True)
    nomeParlamentar: str = Field(index=True)
    idDeputado: DeputadoID | None = Field(foreign_key="deputados.id", index=True, default=None)
    descricao: str = Field(index=True)
    fornecedor: str 
    dataEmissao: date 

    valorDocumento: float
    valorGlosa: float | None
    valorLiquido: float | None
    restituicao: float | None
    datPagamentoRestituicao: date | None
    tipoDocumento: int 
    urlDocumento: str 

    passageiro: str | None
    trecho: str | None
