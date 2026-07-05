import re

from app.domain.models import JobPosting, MatchResult, UserProfile
from app.storage.vector import DeterministicVectorStore


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9+#.]+", text.lower()))


def _job_text(job: JobPosting) -> str:
    return " ".join(
        value
        for value in [
            job.title,
            job.company,
            job.description,
            job.requirements or "",
            job.responsibilities or "",
            job.location,
        ]
        if value
    )


class MatchingService:
    def __init__(self, vector_store: DeterministicVectorStore) -> None:
        self.vector_store = vector_store

    def rank(self, profile: UserProfile, jobs: list[JobPosting]) -> list[MatchResult]:
        results = [self._score(profile, job) for job in jobs]
        return sorted([result for result in results if result is not None], key=lambda item: item.total_score, reverse=True)

    def _score(self, profile: UserProfile, job: JobPosting) -> MatchResult | None:
        text = _job_text(job)
        lower_text = text.lower()
        if job.company.lower() in profile.excluded_companies:
            return None
        if any(keyword in lower_text for keyword in profile.excluded_keywords):
            return None
        if profile.remote_preference == "remote" and job.remote_type not in {"remote", "hybrid"}:
            return None
        if profile.salary_min and job.salary_max and job.salary_max < profile.salary_min:
            return None

        matched_must = [skill for skill in profile.must_have_skills if skill in lower_text]
        missing = [skill for skill in profile.must_have_skills if skill not in matched_must]
        if missing:
            return None

        matched_nice = [skill for skill in profile.nice_to_have_skills if skill in lower_text]
        matched_skills = matched_must + matched_nice
        skill_denominator = max(len(profile.must_have_skills) + len(profile.nice_to_have_skills), 1)
        skill_score = len(matched_skills) / skill_denominator
        title_score = self._title_score(profile, job)
        location_score = self._location_score(profile, job)
        salary_score = self._salary_score(profile, job)
        vector_score = self.vector_store.similarity(" ".join(profile.target_titles + profile.must_have_skills), text)
        recency_score = 0.8 if job.posted_at else 0.5
        source_score = 0.9 if job.source in {"adzuna", "greenhouse"} else 0.5
        total = (
            skill_score * 0.35
            + vector_score * 0.20
            + title_score * 0.15
            + location_score * 0.10
            + salary_score * 0.10
            + recency_score * 0.05
            + source_score * 0.05
        )
        components = {
            "skill": round(skill_score, 3),
            "vector": round(vector_score, 3),
            "title": round(title_score, 3),
            "location": round(location_score, 3),
            "salary": round(salary_score, 3),
            "recency": round(recency_score, 3),
            "source": round(source_score, 3),
        }
        explanation = f"Matched {job.title} at {job.company} because it includes {', '.join(matched_skills)}."
        return MatchResult(
            job_id=job.id,
            total_score=round(total, 3),
            score_components=components,
            matched_skills=matched_skills,
            missing_must_haves=missing,
            explanation=explanation,
        )

    def _title_score(self, profile: UserProfile, job: JobPosting) -> float:
        job_tokens = _tokens(job.title)
        best = 0.0
        for title in profile.target_titles:
            title_tokens = _tokens(title)
            if title_tokens:
                best = max(best, len(job_tokens & title_tokens) / len(title_tokens))
        return best

    def _location_score(self, profile: UserProfile, job: JobPosting) -> float:
        if not profile.locations:
            return 0.5
        job_location = job.location.lower()
        return 1.0 if any(location.lower() in job_location for location in profile.locations) else 0.25

    def _salary_score(self, profile: UserProfile, job: JobPosting) -> float:
        if profile.salary_min is None:
            return 0.5
        if job.salary_min and job.salary_min >= profile.salary_min:
            return 1.0
        if job.salary_max and job.salary_max >= profile.salary_min:
            return 0.75
        return 0.25
