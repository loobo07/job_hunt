from app.sources.adzuna import AdzunaNormalizer
from app.sources.greenhouse import GreenhouseNormalizer

from tests.fixtures import ADZUNA_RAW_JOB, GREENHOUSE_RAW_JOB


def test_adzuna_normalizer_maps_raw_payload_to_job_posting():
    posting = AdzunaNormalizer().to_job_posting(ADZUNA_RAW_JOB)

    assert posting.source == "adzuna"
    assert posting.source_id == "adz-1"
    assert posting.company == "Acme Data"
    assert posting.title == "Senior Python Backend Engineer"
    assert posting.apply_url == "https://example.com/adzuna/acme-python"
    assert posting.posted_at.isoformat().startswith("2026-06-20T12:00:00")
    assert posting.salary_min == 150000
    assert posting.salary_max == 190000
    assert posting.employment_type == "full_time"
    assert posting.source_metadata["category"] == "it-jobs"
    assert posting.source_metadata["salary_is_predicted"] is False


def test_greenhouse_normalizer_maps_raw_payload_to_job_posting():
    posting = GreenhouseNormalizer(board_token="acme").to_job_posting(GREENHOUSE_RAW_JOB)

    assert posting.source == "greenhouse"
    assert posting.source_id == "2001"
    assert posting.company == "acme"
    assert posting.title == "Backend Platform Engineer"
    assert posting.department == "Engineering"
    assert posting.location == "Remote - United States"
    assert posting.remote_type == "remote"
    assert posting.apply_url == "https://boards.greenhouse.io/acme/jobs/2001"
    assert posting.source_metadata["internal_job_id"] == 901
