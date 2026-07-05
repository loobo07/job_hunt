from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

RemoteType = Literal["remote", "hybrid", "onsite", "unknown"]
FeedbackStatus = Literal["saved", "ignored", "applied", "false_positive"]


def _normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def _normalize_lower_list(values: list[str]) -> list[str]:
    return [_normalize_text(value).lower() for value in values if value and value.strip()]


def _stable_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class UserProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: str(uuid4()))
    target_titles: list[str]
    must_have_skills: list[str] = []
    nice_to_have_skills: list[str] = []
    years_experience: int = 0
    locations: list[str] = []
    remote_preference: RemoteType = "unknown"
    salary_min: int | None = None
    excluded_companies: list[str] = []
    excluded_keywords: list[str] = []

    @field_validator("target_titles", "locations")
    @classmethod
    def normalize_text_list(cls, values: list[str]) -> list[str]:
        return [_normalize_text(value) for value in values if value and value.strip()]

    @field_validator(
        "must_have_skills",
        "nice_to_have_skills",
        "excluded_companies",
        "excluded_keywords",
    )
    @classmethod
    def normalize_lower_values(cls, values: list[str]) -> list[str]:
        return _normalize_lower_list(values)


class JobPosting(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: str(uuid4()))
    source: str
    source_id: str
    company: str
    title: str
    description: str
    location: str
    remote_type: RemoteType = "unknown"
    apply_url: str
    posted_at: datetime | None = None
    expires_at: datetime | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    employment_type: str | None = None
    seniority: str | None = None
    department: str | None = None
    requirements: str | None = None
    responsibilities: str | None = None
    benefits: str | None = None
    raw_payload: dict[str, Any] = Field(default_factory=dict)
    raw_payload_hash: str | None = None
    source_metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("source", "source_id", "company", "title", "description", "location")
    @classmethod
    def normalize_required_string(cls, value: str) -> str:
        normalized = _normalize_text(value)
        if not normalized:
            raise ValueError("field cannot be empty")
        return normalized

    @field_validator("apply_url")
    @classmethod
    def require_http_url(cls, value: str) -> str:
        normalized = _normalize_text(value)
        if not normalized.startswith(("http://", "https://")):
            raise ValueError("apply_url must be an http(s) URL")
        return normalized

    @field_validator("posted_at", "expires_at", mode="before")
    @classmethod
    def parse_datetime(cls, value: Any) -> Any:
        if isinstance(value, str) and value.endswith("Z"):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value

    @model_validator(mode="after")
    def fill_payload_hash(self) -> JobPosting:
        if self.raw_payload_hash is None:
            payload = self.raw_payload or {
                "source": self.source,
                "source_id": self.source_id,
                "apply_url": self.apply_url,
            }
            self.raw_payload_hash = _stable_hash(payload)
        if self.posted_at and self.posted_at.tzinfo is None:
            self.posted_at = self.posted_at.replace(tzinfo=timezone.utc)
        return self


class MatchResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    job_id: str
    total_score: float
    score_components: dict[str, float]
    matched_skills: list[str]
    missing_must_haves: list[str]
    explanation: str


class UserFeedback(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: str(uuid4()))
    job_id: str
    status: FeedbackStatus
    rating: int | None = Field(default=None, ge=1, le=5)
    reason_tags: list[str] = []
    notes: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("reason_tags")
    @classmethod
    def normalize_reason_tags(cls, values: list[str]) -> list[str]:
        return _normalize_lower_list(values)
