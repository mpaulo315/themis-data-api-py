from typing import Generic, TypeVar

from croniter import croniter
from datetime import datetime

from src.fetcher.core.job import Job
from src.fetcher.core.resource import Resource
from src.fetcher.core.storage import DatabaseStorage
from sqlalchemy.orm import Session

from src.fetcher.core.storage import DatabaseStorage

T = TypeVar("T")


class JobRunner(Generic[T]):
    def __init__(self, job: Job, resource: Resource[T], session: Session):
        self.job = job
        self.resource = resource
        self.session = session

    def is_stale(self) -> bool:
        # Significa que o job não foi executado com sucesso
        if (
            not self.job.last_success_timestamp
            or self.session.query(self.resource.model).count() == 0
        ):
            return True

        next_cron = croniter(
            self.job.cron_expression, self.job.last_success_timestamp
        ).get_next(datetime)
        return next_cron <= datetime.now()

    def run(self):
        if not self.is_stale():
            return

        try:
            start_datetime = datetime.now()
            print(f"Job {self.job.id} started")
            raw_data = self.resource.fetch()
            print(f"Job {self.job.id} fetched data")
            data = self.resource.parse(raw_data)
            print(f"Job {self.job.id} parsed data")

            print(
                f"Job {self.job.id} ({self.job.name}) applying strategy: {self.job.update_strategy}"
            )
            print(f"Data length: {len(data)}")
            DatabaseStorage.apply_strategy(
                strategy=self.job.update_strategy,
                session=self.session,
                model=self.resource.model,
                items=data,
                where_clause=self.job.args.get("where_clause"),
                index_elements=self.job.args.get("index_elements"),
            )
            print(f"Job {self.job.id} applied strategy")
            self.job.last_success_timestamp = datetime.now()
            self.job.last_run_message = f"Job {self.job.id} completed successfully"

            self.job.execution_time_seconds = (
                datetime.now() - start_datetime
            ).total_seconds()

            if self.job.runs is not None:
                self.job.decrement_runs()

            print(f"Job {self.job.id} executed successfully")

        except Exception as e:
            self.session.rollback()

            self.job.last_failure_timestamp = datetime.now()
            self.job.last_run_message = str(e)

            print(f"Job {self.job.id} failed: {e}")
        finally:
            self.job.last_run_timestamp = datetime.now()
            self.session.commit()
