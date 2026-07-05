from app.domain.models import JobPosting


class AdzunaNormalizer:
    def to_job_posting(self, raw: dict) -> JobPosting:
        return JobPosting(
            source="adzuna",
            source_id=str(raw["id"]),
            company=raw["company"]["display_name"],
            title=raw["title"],
            description=raw["description"],
            location=raw["location"]["display_name"],
            remote_type="unknown",
            apply_url=raw["redirect_url"],
            posted_at=raw.get("created"),
            salary_min=raw.get("salary_min"),
            salary_max=raw.get("salary_max"),
            employment_type=raw.get("contract_time") or raw.get("contract_type"),
            raw_payload=raw,
            source_metadata={
                "location_area": raw.get("location", {}).get("area", []),
                "category": raw.get("category", {}).get("tag"),
                "contract_type": raw.get("contract_type"),
                "salary_is_predicted": raw.get("salary_is_predicted"),
            },
        )
