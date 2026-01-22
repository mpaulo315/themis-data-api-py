from db.session import SessionLocal
from fetcher.core.scheduler import Scheduler
from fetcher.seed.jobs import seed_jobs


def main():
    print("Starting fetcher...")
    with SessionLocal() as session:
        seed_jobs(session)

    scheduler = Scheduler()
    scheduler.run_all_jobs()

if __name__ == "__main__":
    main()
