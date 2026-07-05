from app.domain.models import JobPosting
from app.sources.adzuna import AdzunaNormalizer
from app.sources.fixtures import ADZUNA_RAW_JOB, GREENHOUSE_RAW_JOB
from app.sources.greenhouse import GreenhouseNormalizer


class IngestionService:
    def fixture_postings(self, sources: list[str], greenhouse_boards: list[str]) -> list[JobPosting]:
        postings: list[JobPosting] = []
        source_set = set(sources)
        if "adzuna" in source_set:
            postings.append(AdzunaNormalizer().to_job_posting(ADZUNA_RAW_JOB))
        if "greenhouse" in source_set:
            for board in greenhouse_boards:
                postings.append(GreenhouseNormalizer(board_token=board).to_job_posting(GREENHOUSE_RAW_JOB))
        return postings
