from sqlalchemy import Integer, Date, String
from sqlalchemy.orm import mapped_column
from camara.db.session import Base

LegislaturaID = Integer

class Legislatura(Base):
    __tablename__ = "legislaturas"

    idLegislatura = mapped_column(LegislaturaID, primary_key=True, index=True)
    uri = mapped_column(String, nullable=False)
    dataInicio = mapped_column(Date)
    dataFim = mapped_column(Date)
    anoEleicao = mapped_column(Integer)
