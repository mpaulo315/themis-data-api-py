from abc import ABC, abstractmethod
import io
import json
from typing import Generic, Iterable, Type, TypeVar, TypedDict
from zipfile import ZipFile
import httpx
from sqlmodel import SQLModel


T = TypeVar("T", bound=SQLModel) # Tipo ligado a tabela
V = TypeVar("V") # Tipo ligado ao retorno do fetch


class Resource(Generic[T, V], ABC):
    model: Type[T]

    def __init__(self, model: Type[T]):
        self.model = model
    
    @abstractmethod
    def fetch(self) -> V:
        """Fetch dado bruto (API, arquivo, etc. )"""
        pass

    @abstractmethod
    def parse(self, data: V) -> Iterable[T]:
        """Transforma dado bruto em um modelo"""
        pass

K = TypedDict("CamaraFile", {"dados": list[dict]})

class CamaraJSONZIPResource(Resource[T, K]):
    def __init__(self, model: Type[T], url: str, json_filename: str):
        self.model = model
        self.url = url
        self.json_filename = json_filename
    
    def fetch(self) -> K:
        response = httpx.get(self.url)
        response.raise_for_status()

        with ZipFile(io.BytesIO(response.content)) as zip_file:
            with zip_file.open(self.json_filename) as json_file:
                t = io.TextIOWrapper(json_file, encoding="utf-8")
                return json.load(t)
            
    def parse(self, data: K) -> Iterable[T]:
        rows: list[T] = []

        for row in data.get("dados", []):
            rows.append(self.model.model_validate(row))
        return rows
    
class CamaraJSONResource(Resource[T, K]):
    def __init__(self, model: Type[T], url: str):
        self.model = model
        self.url = url
    
    def fetch(self) -> K:
        response = httpx.get(self.url)
        response.raise_for_status()

        t = io.TextIOWrapper(io.BytesIO(response.content), encoding="utf-8")
        return json.load(t)
            
    def parse(self, data: K) -> Iterable[T]:
        rows: list[T] = []

        for row in data.get("dados", []):
            rows.append(self.model.model_validate(row))
        return rows
