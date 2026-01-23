from db.session import SessionLocal
from sqlalchemy import select

from fetcher.core.job import Job, JobStatus
from fetcher.core.job_runner import JobRunner
from fetcher.core.resource_factory import ResourceFactory


class Scheduler:

    @classmethod
    def run_all_jobs(cls):
        with SessionLocal() as session:
            jobs = (
                session.execute(select(Job).where(Job.status == JobStatus.ACTIVE))
                .scalars()
                .all()
            )

            for job in jobs:
                resource = ResourceFactory.create(job)
                runner = JobRunner(job, resource, session)
                runner.run()
