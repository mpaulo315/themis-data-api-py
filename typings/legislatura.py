from datetime import date, datetime
from pydantic import field_validator
from sqlmodel import Field, SQLModel

LegislaturaID = int

class Legislatura(SQLModel, table=True):
    __tablename__ = "legislaturas"
    # __table_args__ = {"schema": "camara"}

    @field_validator("dataInicio", "dataFim", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value.split("T")[0], "%Y-%m-%d").date()
        return None

    idLegislatura: LegislaturaID = Field(primary_key=True, index=True)
    uri: str
    dataInicio: date = Field(index=True)
    dataFim: date = Field(index=True)
    anoEleicao: int = Field(index=True)
