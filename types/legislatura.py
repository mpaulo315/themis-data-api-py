from datetime import date
from sqlmodel import Field, SQLModel

LegislaturaID = int

class Legislatura(SQLModel, table=True):
    __tablename__ = "legislatura"
    __table_args__ = {"schema": "camara"}

    idLegislatura: LegislaturaID = Field(primary_key=True, index=True)
    uri: str
    dataInicio: date = Field(index=True)
    dataFim: date = Field(index=True)
    anoEleicao: int = Field(index=True)
