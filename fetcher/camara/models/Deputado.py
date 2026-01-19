from sqlalchemy import String, Integer, Date, ForeignKey
from sqlalchemy.orm import mapped_column
from camara.db.session import Base
from camara.models.Legislatura import Legislatura, LegislaturaID

DeputadoID = Integer

class Deputado(Base):
    __tablename__ = "deputados"

    id = mapped_column(DeputadoID, primary_key=True, index=True)
    uri = mapped_column(String)
    nome = mapped_column(String, index=True)
    nomeCivil = mapped_column(String, index=True)
    siglaSexo = mapped_column(String, index=True)
    idLegislaturaInicial = mapped_column(LegislaturaID, ForeignKey(Legislatura.idLegislatura), index=True)
    idLegislaturaFinal = mapped_column(LegislaturaID, ForeignKey(Legislatura.idLegislatura), index=True) 
    ufNascimento = mapped_column(String, index=True)
    municipioNascimento = mapped_column(String, index=True)
    dataNascimento = mapped_column(Date)
    dataFalecimento = mapped_column(Date)

