from src.db.session import SessionLocal
from src.fetcher.core.job import Job
from src.fetcher.core.scheduler import Scheduler
from src.fetcher.seed.jobs import seed_jobs


def main():
    with SessionLocal() as session:
        if not session.query(Job).first():
            seed_jobs(session)

    scheduler = Scheduler()
    scheduler.run_all_jobs()


if __name__ == "__main__":
    main()
