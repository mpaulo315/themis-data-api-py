from datetime import date, datetime
from pydantic import field_validator
from sqlmodel import Field, SQLModel

from types.deputado import DeputadoID
from types.legislatura import LegislaturaID

DespesaID = int

class Despesa(SQLModel, table = True):
    __tablename__ = "despesas"
    __table_args__ = {"schema": "camara"}

    @field_validator("dataEmissao", mode="before")
    @classmethod
    def validate_data(cls, value):
        if value is None or not isinstance(value, str):
            return None
        return datetime.strptime(value.split("T")[0], "%Y-%m-%d").date()

    id: DespesaID = Field(primary_key=True, index=True)
    idDocumento: int = Field(index=True)
    mes : int = Field(index=True)
    ano: int = Field(index=True)
    codigoLegislatura: LegislaturaID = Field(foreign_key="legislaturas.idLegislatura", index=True)
    nomeParlamentar: str = Field(index=True)
    idDeputado: DeputadoID = Field(foreign_key="deputados.id", index=True)
    descricao: str = Field(index=True)
    fornecedor: str 
    dataEmissao: date 

    valorDocumento: float
    valorGlosa: float 
    valorLiquido: float 
    restituicao: float 
    datPagamentoRestituicao: date 
    tipoDocumento: int 
    urlDocumento: str 

    passageiro: str 
    trecho: str 
