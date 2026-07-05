import pytest
from pydantic import ValidationError

from app.domain.models import JobPosting, UserFeedback, UserProfile


def test_job_posting_requires_canonical_identifiers_and_apply_url():
    posting = JobPosting(
        source="adzuna",
        source_id="adz-1",
        company="Acme Data",
        title="Senior Python Backend Engineer",
        description="Build APIs with Python and FastAPI.",
        location="New York, NY",
        remote_type="hybrid",
        apply_url="https://example.com/jobs/adz-1",
        posted_at="2026-06-20T12:00:00Z",
    )

    assert posting.source == "adzuna"
    assert posting.source_id == "adz-1"
    assert posting.remote_type == "hybrid"
    assert posting.raw_payload_hash


def test_job_posting_rejects_invalid_remote_type():
    with pytest.raises(ValidationError):
        JobPosting(
            source="adzuna",
            source_id="adz-1",
            company="Acme Data",
            title="Senior Python Backend Engineer",
            description="Build APIs with Python and FastAPI.",
            location="New York, NY",
            remote_type="anywhere",
            apply_url="https://example.com/jobs/adz-1",
        )


def test_user_profile_normalizes_skills_and_exclusions():
    profile = UserProfile(
        target_titles=["Backend Engineer"],
        must_have_skills=["Python", " FastAPI "],
        nice_to_have_skills=["PostgreSQL"],
        years_experience=6,
        locations=["New York, NY"],
        remote_preference="remote",
        salary_min=140000,
        excluded_companies=["BadCo"],
        excluded_keywords=["frontend-only"],
    )

    assert profile.must_have_skills == ["python", "fastapi"]
    assert profile.nice_to_have_skills == ["postgresql"]
    assert profile.excluded_companies == ["badco"]


def test_user_feedback_limits_status_values():
    feedback = UserFeedback(job_id="job-1", status="saved", rating=5)

    assert feedback.status == "saved"

    with pytest.raises(ValidationError):
        UserFeedback(job_id="job-1", status="maybe_later", rating=5)
