from typing import Generic, TypeVar

from croniter import croniter
from datetime import datetime

from fetcher.core.job import Job
from fetcher.core.resource import Resource
from fetcher.core.storage import DatabaseStorage
from sqlalchemy.orm import Session

from fetcher.core.storage import DatabaseStorage

T = TypeVar('T')

class JobRunner(Generic[T]):
    def __init__(self, job: Job, resource: Resource[T], session: Session):
        self.job = job
        self.resource = resource
        self.session = session
        
    
    def is_stale(self) -> bool:
        # It means the job has never run successfully
        if not self.job.last_success_timestamp or self.session.query(self.resource.model).count() == 0:
            return True
        
        next_cron = croniter(self.job.cron_expression, self.job.last_success_timestamp).get_next(datetime)
        print(f"Next cron: {next_cron}")
        print(f"Current time: {datetime.now()}")
        print(f"Is stale: {next_cron <= datetime.now()}")
        return next_cron <= datetime.now()

    def run(self):
        if not self.is_stale():
            return
        
        try:
            raw_data = self.resource.fetch()
            data = self.resource.parse(raw_data)
            DatabaseStorage.bulk_insert(self.session, self.resource.model, data)

            self.job.last_success_timestamp = datetime.now()
            self.job.last_run_message = "Job completed successfully"
            
            if self.job.runs is not None:
                self.job.decrement_runs()

        except Exception as e:
            self.session.rollback()

            self.job.last_failure_timestamp = datetime.now()
            self.job.last_run_message = str(e)

            print(f"Job {self.job.id} failed: {e}")
        finally:
            self.job.last_run_timestamp = datetime.now()
            self.session.commit()
