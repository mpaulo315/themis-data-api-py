from sqlalchemy import String, Date, Float, Integer
from camara.db.session import Base
from sqlalchemy.orm import mapped_column

from camara.models.Deputado import DeputadoID
from camara.models.Legislatura import LegislaturaID

class Despesas(Base):
    __tablename__ = "despesas"
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    idDocumento = mapped_column(Integer, index=True)
    mes= mapped_column(Integer, index=True)
    ano= mapped_column(Integer, index=True)
    codigoLegislatura = mapped_column(LegislaturaID, index=True)
    nomeParlamentar = mapped_column(String, index=True)
    idDeputado = mapped_column(DeputadoID, index=True)
    descricao = mapped_column(String, index=True)
    fornecedor = mapped_column(String)
    dataEmissao = mapped_column(Date)
    valorDocumento = mapped_column(Float)
    valorGlosa = mapped_column(Float)
    valorLiquido = mapped_column(Float)
    restituicao = mapped_column(Float)
    datPagamentoRestituicao = mapped_column(Date)
    tipoDocumento = mapped_column(Integer)
    urlDocumento = mapped_column(String)

    passageiro = mapped_column(String)
    trecho = mapped_column(String)
