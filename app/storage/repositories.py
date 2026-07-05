from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.domain.models import JobPosting, UserFeedback, UserProfile
from app.storage.database import FeedbackRecord, JobRecord, ProfileRecord


class JobRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def upsert_many(self, postings: list[JobPosting]) -> int:
        with self.session_factory() as session:
            changed = 0
            for posting in postings:
                existing = session.scalar(
                    select(JobRecord).where(
                        JobRecord.source == posting.source,
                        JobRecord.source_id == posting.source_id,
                    )
                )
                if existing:
                    posting = posting.model_copy(update={"id": existing.id})
                    self._update_record(existing, posting)
                else:
                    session.add(self._record_from_posting(posting))
                changed += 1
            session.commit()
            return changed

    def list_jobs(self) -> list[JobPosting]:
        with self.session_factory() as session:
            records = session.scalars(select(JobRecord).order_by(JobRecord.title)).all()
            return [self._posting_from_record(record) for record in records]

    def get(self, job_id: str) -> JobPosting | None:
        with self.session_factory() as session:
            record = session.get(JobRecord, job_id)
            return self._posting_from_record(record) if record else None

    def _record_from_posting(self, posting: JobPosting) -> JobRecord:
        return JobRecord(**self._record_payload(posting))

    def _update_record(self, record: JobRecord, posting: JobPosting) -> None:
        for key, value in self._record_payload(posting).items():
            setattr(record, key, value)

    def _record_payload(self, posting: JobPosting) -> dict:
        return posting.model_dump(mode="python")

    def _posting_from_record(self, record: JobRecord) -> JobPosting:
        return JobPosting(
            id=record.id,
            source=record.source,
            source_id=record.source_id,
            company=record.company,
            title=record.title,
            description=record.description,
            location=record.location,
            remote_type=record.remote_type,
            apply_url=record.apply_url,
            posted_at=record.posted_at,
            expires_at=record.expires_at,
            salary_min=record.salary_min,
            salary_max=record.salary_max,
            employment_type=record.employment_type,
            seniority=record.seniority,
            department=record.department,
            requirements=record.requirements,
            responsibilities=record.responsibilities,
            benefits=record.benefits,
            raw_payload=record.raw_payload,
            raw_payload_hash=record.raw_payload_hash,
            source_metadata=record.source_metadata,
        )


class ProfileRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def create(self, profile: UserProfile) -> UserProfile:
        with self.session_factory() as session:
            session.add(ProfileRecord(id=profile.id, payload=profile.model_dump(mode="json")))
            session.commit()
            return profile

    def get(self, profile_id: str) -> UserProfile | None:
        with self.session_factory() as session:
            record = session.get(ProfileRecord, profile_id)
            return UserProfile(**record.payload) if record else None


class FeedbackRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def create(self, feedback: UserFeedback) -> UserFeedback:
        with self.session_factory() as session:
            session.add(FeedbackRecord(id=feedback.id, job_id=feedback.job_id, payload=feedback.model_dump(mode="json")))
            session.commit()
            return feedback
