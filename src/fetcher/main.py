from db.session import SessionLocal
from fetcher.core.job import Job
from fetcher.core.scheduler import Scheduler
from fetcher.seed.jobs import seed_jobs


def main():
    with SessionLocal() as session:
        if not session.query(Job).first():
            seed_jobs(session)

    scheduler = Scheduler()
    scheduler.run_all_jobs()


if __name__ == "__main__":
    main()
