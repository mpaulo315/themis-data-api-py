from datetime import date, datetime
from typing import Optional
from pydantic import field_validator, model_validator
from sqlmodel import Field, SQLModel

from src.typings.deputado import DeputadoID
from src.typings.legislatura import LegislaturaID

DespesaID = int


class DespesaDeputado(SQLModel, table=True):
    __tablename__ = "despesas_deputado"
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

    id: Optional[DespesaID] = Field(primary_key=True, index=True, default=None)
    idDocumento: int = Field(index=True)
    mes: int = Field(index=True)
    ano: int = Field(index=True)
    codigoLegislatura: LegislaturaID = Field(
        foreign_key="legislaturas.idLegislatura", index=True
    )
    nomeParlamentar: str = Field(index=True)
    idDeputado: DeputadoID | None = Field(
        foreign_key="deputados.id", index=True, default=None
    )
    descricao: str = Field(index=True)
    fornecedor: str
    dataEmissao: date | None

    valorDocumento: float
    valorGlosa: float | None = Field(
        description="Valor retido, isto é, não coberto pela CEAP, por qualquer razão (impedimento legal, insuficiência de comprovação, etc)."
    )
    valorLiquido: float | None = Field(
        description="Valor da despesa efetivamente debitado da Cota Parlamentar, correspondente ao vlrDocumento menos o vlrGlosa. Em despesas de Telefonia, é possível que este valor seja registrado como 0, significando que a despesa foi coberta pela franquia do contrato."
    )
    restituicao: float | None = Field(
        description="Valor que o parlamentar devolveu à Câmara. Nos registros em que este campo é preenchido, é comum que haja outro registro associado ao mesmo documento comprobatório da despesa."
    )
    datPagamentoRestituicao: date | None = Field(
        description="Data do pagamento da restituição."
    )
    tipoDocumento: int
    urlDocumento: str | None

    passageiro: str | None = Field(
        description="Nos registros referentes a passagens aéreas, o campo traz o nome da pessoa para quem foi emitida a passagem."
    )
    trecho: str | None = Field(
        description="Também nos registros referentes a passagens aéreas, traz como texto livre a descrição do(s) trecho(s) de viagem do bilhete. Normalmente utiliza o padrão, popularizado por companhias aéreas, de siglas de três letras que identificam aeroportos, separadas pelo caractere barra (/)."
    )
