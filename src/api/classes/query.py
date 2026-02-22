from typing import Any, Literal, TypeVar
from pydantic import BaseModel, model_validator, Field
from typings.despesa_deputado import DespesaDeputado


type DBFunc = Literal[
    "max", "min", "count", "dcount", "avg", "sum", "stddev"
    ]

T = TypeVar("T", bound=BaseModel)

class GroupField(BaseModel):
    agg_func: DBFunc
    field: str
    label: str 

class GroupingQuery(BaseModel):
    select_fields_list: list[GroupField]
    group_by_fields: list[str]

    @model_validator(mode="before")
    @classmethod
    def validate(cls, data: Any) -> Any:
        if isinstance(data, dict):
            match data.get("table"):
                case "despesa_deputado":
                    model = DespesaDeputado
                case _:
                    raise ValueError(f"Table doesn't exist: {data.get("table")}.")

            for f in data.get("group_by_fields"):
                if not f in model.model_fields:
                    raise ValueError(f"Field doesn't exist: {f}.")

            for obj in data.get("select_fields_list"):
                if not obj.get("field") in model.model_fields:
                    raise ValueError(f"Grouping field doesn't exist: {obj.get("field")}.")

            return data
        
        raise ValueError("Data format not allowed")