from datetime import datetime
from enum import IntEnum
from typing import Optional
from sqlalchemy import JSON, Column, Enum
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict

from fetcher.core.storage import UpdateStrategy

class DatasetType(str, Enum):
    DEPUTADO = "deputado"
    LEGISLATURA = "legislatura"
    DESPESA_DEPUTADO = "despesa_deputado"

class ResourceKind(str, Enum):
    JSON_ZIP = "json_zip"
    JSON = "json"

class JobStatus(IntEnum):
    DISABLED = 0
    ACTIVE = 1

class Job(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    __tablename__ = "jobs"

    id: Optional[int] = Field(primary_key=True, index=True, default=None)
    name: str
    dataset_type: DatasetType
    resource_kind: ResourceKind
    update_strategy: UpdateStrategy
    cron_expression: str
    status: int
    runs: int | None = Field(default=None)
    args: dict | None = Field(default_factory=dict, sa_column=Column(JSON))
    last_run_timestamp: datetime | None = Field(default=None)
    last_success_timestamp: datetime | None = Field(default=None)
    last_failure_timestamp: datetime | None = Field(default=None)
    last_run_message: str | None = Field(default=None)
    additional_info: dict | None = Field(default_factory=dict, sa_column=Column(JSON))
    execution_time_seconds: int | None = Field(default=None)

    def decrement_runs(self) -> None:
        self.runs = self.runs - 1 if self.runs is not None and self.runs > 0 else 0
        self.status = JobStatus.ACTIVE if self.runs > 0 or self.runs is None else JobStatus.DISABLED
