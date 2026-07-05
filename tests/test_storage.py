from app.domain.models import JobPosting
from app.storage.database import create_database, create_session_factory
from app.storage.repositories import JobRepository


def test_job_repository_upserts_by_source_and_source_id():
    engine, session_factory = create_session_factory("sqlite+pysqlite:///:memory:")
    create_database(engine)
    repo = JobRepository(session_factory)
    first = JobPosting(
        source="adzuna",
        source_id="adz-1",
        company="Acme Data",
        title="Senior Python Backend Engineer",
        description="Build APIs with Python.",
        location="New York, NY",
        remote_type="hybrid",
        apply_url="https://example.com/jobs/adz-1",
        raw_payload={"id": "adz-1"},
    )
    updated = first.model_copy(update={"title": "Principal Python Backend Engineer"})

    repo.upsert_many([first])
    repo.upsert_many([updated])
    jobs = repo.list_jobs()

    assert len(jobs) == 1
    assert jobs[0].title == "Principal Python Backend Engineer"
    assert jobs[0].raw_payload_hash == first.raw_payload_hash
