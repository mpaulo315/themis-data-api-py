from sqlalchemy import Integer, Date
from sqlalchemy.orm import Mapped, mapped_column
from camara.db.session import Base

LegislaturaID = Integer

class Legislatura(Base):
    __tablename__ = "legislatura"

    idLegislatura = mapped_column(LegislaturaID, primary_key=True, index=True)
    numero = mapped_column(Integer, nullable=False)
    dataInicio = mapped_column(Date, nullable=False)
    dataFim = mapped_column(Date, nullable=False)
    anoEleicao = mapped_column(Integer, nullable=False)
