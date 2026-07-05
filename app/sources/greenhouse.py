from app.domain.models import JobPosting


def _metadata_value(raw: dict, name: str) -> str | None:
    for item in raw.get("metadata", []):
        if item.get("name", "").lower() == name.lower():
            return item.get("value")
    return None


class GreenhouseNormalizer:
    def __init__(self, board_token: str) -> None:
        self.board_token = board_token

    def to_job_posting(self, raw: dict) -> JobPosting:
        workplace_type = (_metadata_value(raw, "Workplace Type") or "unknown").lower()
        remote_type = workplace_type if workplace_type in {"remote", "hybrid", "onsite"} else "unknown"
        office = raw.get("office") or {}
        return JobPosting(
            source="greenhouse",
            source_id=str(raw["id"]),
            company=self.board_token,
            title=raw["title"],
            description=raw["content"],
            department=raw.get("department"),
            location=office.get("name", "Unknown"),
            remote_type=remote_type,
            apply_url=raw["absolute_url"],
            raw_payload=raw,
            source_metadata={
                "board_token": self.board_token,
                "internal_job_id": raw.get("internal_job_id"),
                "metadata": raw.get("metadata", []),
            },
        )
