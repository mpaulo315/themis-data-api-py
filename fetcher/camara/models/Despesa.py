from pydantic import BaseModel, Field
from abc import Enum
from typing import Annotated
from Deputado import Deputado
from Legislatura import LegislaturaID

class Despesa(BaseModel):
    ano: Annotated[int, Field(description="Ano")]
    mes: Annotated[int, Field(description="Mês")]
    dataEmissao: Annotated[str, Field(description="Data de emissão")]
    codigoLegislatura: Annotated[LegislaturaID, Field(description="Código da legislatura")]
    idDeputado: Annotated[Deputado['id'], Field(description="ID do deputado")]
    siglaPartido: Annotated[str, Field(description="Sigla do partido do deputado")]
    siglaUF: Annotated[str, Field(description="Sigla da UF do deputado")]
    descricao: Annotated[str, Field(description="Natureza da despesa")]
    tipoDocumento: Annotated[str, Field(description="Tipo de documento")]
    valorDocumento: Annotated[float, Field(description="Valor do documento")]
    valorGlosa: Annotated[float, Field(description="Valor não coberto pela Cota Parlamentar")]
    valorLiquido: Annotated[float, Field(description="Valor líquido; Valor do documento menos o valor não coberto pela Cota Parlamentar")]
    restituicao: Annotated[float, Field(description="Valor da restituição")]
    cnpjCpf: Annotated[str, Field(description="CNPJ ou CPF do deputado")]
    numeroSubCota: Annotated[int, Field(description="Número da subcota")]
    numeroCota: Annotated[int, Field(description="Número da cota")]
    idDocumento: Annotated[int, Field(description="ID do documento")]
    urlDocumento: Annotated[str, Field(description="URL do documento")]
    trecho: Annotated[str, Field(description="Em caso de passagem aérea, o trecho do vôo")]
    passageiro: Annotated[str, Field(description="Em caso de passagem aérea, o nome do passageiro")]


class TipoDocumento(Enum):
    0 = "Nota Fiscal"
    1 = "Recibo ou outros"
    2 = "Documento Emitido no exterior"
    3 = "Despesa do Parlasul (Parlamento do Mercosul)"
    4 = "Nota Fiscal Eletrônica"
    5 = "Nota Fiscal Eletrônica"
