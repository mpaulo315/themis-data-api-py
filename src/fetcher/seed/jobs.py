from sqlalchemy.orm import Session
from fetcher.core.job import Job
from fetcher.core.job import DatasetType, ResourceKind, JobStatus
from fetcher.config.data_file import (
    DEPUTADOS_URL,
    DESPESAS_URL_BUILDER,
    LEGISLATURAS_URL,
    MIN_ANO_DESPESAS,
)
from fetcher.core.storage import UpdateStrategy


def seed_jobs(session: Session):
    seed_deputados_job(session)
    seed_legislatura_job(session)
    seed_despesas_deputados_job(session)


def seed_deputados_job(session: Session):
    if session.query(Job).filter_by(name="deputados").first():
        return

    job = Job(
        name="deputados",
        dataset_type=DatasetType.DEPUTADO,
        resource_kind=ResourceKind.JSON,
        update_strategy=UpdateStrategy.UPSERT,
        cron_expression="0 23 * * 0",  # 23:00 do domingo
        status=JobStatus.ACTIVE,
        args={"url": DEPUTADOS_URL, "index_elements": ["id"]},
    )

    session.add(job)
    session.commit()
    session.refresh(job)


def seed_legislatura_job(session: Session):
    if session.query(Job).filter_by(name="legislatura").first():
        return

    job = Job(
        name="legislatura",
        dataset_type=DatasetType.LEGISLATURA,
        resource_kind=ResourceKind.JSON,
        cron_expression="0 23 * * 0",  # 23:00 do domingo
        update_strategy=UpdateStrategy.FULL_REPLACE,
        status=JobStatus.ACTIVE,
        args={"url": LEGISLATURAS_URL, "index_elements": ["idLegislatura"]},
    )

    session.add(job)
    session.commit()
    session.refresh(job)


def seed_despesas_deputados_job(session: Session):
    for i in range(MIN_ANO_DESPESAS, 2025):
        if session.query(Job).filter_by(name=f"despesas-deputados-{i}").first():
            continue

        job = Job(
            name=f"despesas-deputados-{i}",
            dataset_type=DatasetType.DESPESA_DEPUTADO,
            resource_kind=ResourceKind.JSON_ZIP,
            cron_expression="0 23 * * 0",  # 23:00 do domingo
            update_strategy=UpdateStrategy.PARTIAL_REPLACE,
            status=JobStatus.ACTIVE,
            args={
                "url": DESPESAS_URL_BUILDER(i),
                "json_filename": f"Ano-{i}.json",
                "where_clause": {"column": "ano", "value": i, "comparison": "="},
            },
            runs=1,
        )

        session.add(job)
        session.commit()
        session.refresh(job)
