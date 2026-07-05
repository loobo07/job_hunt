from app.domain.models import JobPosting, UserProfile
from app.services.matching import MatchingService
from app.storage.vector import DeterministicVectorStore

from tests.fixtures import SAMPLE_PROFILE


def make_job(**overrides):
    data = {
        "id": "job-1",
        "source": "adzuna",
        "source_id": "adz-1",
        "company": "Acme Data",
        "title": "Senior Python Backend Engineer",
        "description": "Python FastAPI PostgreSQL services for data workflows.",
        "location": "Remote - United States",
        "remote_type": "remote",
        "salary_min": 150000,
        "salary_max": 190000,
        "apply_url": "https://example.com/jobs/1",
        "posted_at": "2026-06-20T12:00:00Z",
    }
    data.update(overrides)
    return JobPosting(**data)


def test_matching_scores_relevant_job_with_components_and_explanation():
    profile = UserProfile(**SAMPLE_PROFILE)
    job = make_job()

    result = MatchingService(DeterministicVectorStore()).rank(profile, [job])[0]

    assert result.job_id == "job-1"
    assert result.total_score > 0.70
    assert result.score_components["skill"] > 0
    assert result.score_components["vector"] > 0
    assert result.matched_skills == ["python", "fastapi", "postgresql"]
    assert result.missing_must_haves == []
    assert "python" in result.explanation.lower()


def test_matching_filters_excluded_company_and_missing_must_have_skill():
    profile = UserProfile(**SAMPLE_PROFILE)
    excluded = make_job(id="job-2", company="BadCo")
    missing_skill = make_job(
        id="job-3",
        source_id="adz-3",
        description="Java platform services.",
        title="Backend Engineer",
    )

    results = MatchingService(DeterministicVectorStore()).rank(profile, [excluded, missing_skill])

    assert results == []
