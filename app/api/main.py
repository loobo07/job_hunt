from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings
from app.domain.models import JobPosting, UserFeedback, UserProfile
from app.services.ingestion import IngestionService
from app.services.matching import MatchingService
from app.storage.database import create_database, create_session_factory
from app.storage.repositories import FeedbackRepository, JobRepository, ProfileRepository
from app.storage.vector import DeterministicVectorStore


class IngestRequest(BaseModel):
    sources: list[str]
    greenhouse_boards: list[str] = ["acme"]


class MatchSearchRequest(BaseModel):
    profile_id: str


def create_app(session_factory: sessionmaker[Session]) -> FastAPI:
    app = FastAPI(title="Job Hunt Backend")

    def get_session() -> Session:
        with session_factory() as session:
            yield session

    def get_job_repo() -> JobRepository:
        return JobRepository(session_factory)

    def get_profile_repo() -> ProfileRepository:
        return ProfileRepository(session_factory)

    def get_feedback_repo() -> FeedbackRepository:
        return FeedbackRepository(session_factory)

    @app.post("/profiles", status_code=status.HTTP_201_CREATED)
    def create_profile(
        profile: UserProfile,
        repo: ProfileRepository = Depends(get_profile_repo),
    ) -> UserProfile:
        return repo.create(profile)

    @app.get("/profiles/{profile_id}")
    def get_profile(
        profile_id: str,
        repo: ProfileRepository = Depends(get_profile_repo),
    ) -> UserProfile:
        profile = repo.get(profile_id)
        if profile is None:
            raise HTTPException(status_code=404, detail="profile not found")
        return profile

    @app.post("/ingest/run")
    def ingest(
        request: IngestRequest,
        repo: JobRepository = Depends(get_job_repo),
    ) -> dict[str, int]:
        postings = IngestionService().fixture_postings(request.sources, request.greenhouse_boards)
        return {"inserted": repo.upsert_many(postings)}

    @app.get("/jobs")
    def list_jobs(repo: JobRepository = Depends(get_job_repo)) -> list[JobPosting]:
        return repo.list_jobs()

    @app.get("/jobs/{job_id}")
    def get_job(job_id: str, repo: JobRepository = Depends(get_job_repo)) -> JobPosting:
        job = repo.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="job not found")
        return job

    @app.post("/matches/search")
    def search_matches(
        request: MatchSearchRequest,
        profile_repo: ProfileRepository = Depends(get_profile_repo),
        job_repo: JobRepository = Depends(get_job_repo),
    ):
        profile = profile_repo.get(request.profile_id)
        if profile is None:
            raise HTTPException(status_code=404, detail="profile not found")
        return MatchingService(DeterministicVectorStore()).rank(profile, job_repo.list_jobs())

    @app.post("/matches/{job_id}/explain")
    def explain_match(
        job_id: str,
        request: MatchSearchRequest,
        profile_repo: ProfileRepository = Depends(get_profile_repo),
        job_repo: JobRepository = Depends(get_job_repo),
    ):
        profile = profile_repo.get(request.profile_id)
        job = job_repo.get(job_id)
        if profile is None or job is None:
            raise HTTPException(status_code=404, detail="profile or job not found")
        matches = MatchingService(DeterministicVectorStore()).rank(profile, [job])
        if not matches:
            raise HTTPException(status_code=404, detail="job does not match profile")
        return matches[0]

    @app.post("/feedback", status_code=status.HTTP_201_CREATED)
    def create_feedback(
        feedback: UserFeedback,
        repo: FeedbackRepository = Depends(get_feedback_repo),
    ) -> UserFeedback:
        return repo.create(feedback)

    @app.get("/sources")
    def list_sources() -> list[dict[str, str]]:
        return [
            {"name": "adzuna", "status": "configured"},
            {"name": "greenhouse", "status": "configured"},
        ]

    return app


def create_default_app() -> FastAPI:
    settings = get_settings()
    engine, session_factory = create_session_factory(settings.database_url)
    create_database(engine)
    return create_app(session_factory)
