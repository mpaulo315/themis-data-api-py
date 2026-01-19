from pydantic import BaseModel, Field
from typing import Annotated

LegislaturaID = int

class Legislatura(BaseModel):
    idLegislatura: Annotated[LegislaturaID, Field(description="ID da legislatura")]
    uri: Annotated[str, Field(description="URI da legislatura")]
    dataInicio: Annotated[str, Field(description="Data de início da legislatura")]
    dataFim: Annotated[str, Field(description="Data de fim da legislatura")]
    anoEleicao: Annotated[int, Field(description="Ano da eleição")]
