# Job Board Ingestion Requirements

## Objective

Build a job-posting ingestion and matching system that normalizes postings from multiple job sources, ranks them against a user skill profile, and exposes reliable APIs for search, explanation, and feedback.

## Scope

In scope:

- API-driven ingestion from Adzuna, USAJOBS, Greenhouse, Lever, Ashby, Workable, and Remotive.
- Canonical normalization of each posting into a shared schema.
- Semantic retrieval and deterministic scoring against a user profile.
- Feedback capture for saves, ignores, applications, and false positives.
- Local development with Chroma and production-ready vector-store abstraction.

Out of scope:

- Browser scraping of large boards without explicit permission.
- Multi-user enterprise permissioning.
- Full ATS write-back or application submission automation.
- Real-time chat or recruiter messaging.

## Functional Requirements

1. The system shall ingest jobs from each configured source on a schedule or on demand.
2. The system shall preserve the raw source payload for debugging and replay.
3. The system shall normalize each posting into a common `JobPosting` model.
4. The system shall deduplicate postings across repeated fetches and across overlapping sources where possible.
5. The system shall extract and store skill signals, title signals, salary signals, location signals, and seniority signals.
6. The system shall build a user profile from manual input or resume text.
7. The system shall rank jobs with a hybrid algorithm that combines hard filters, vector similarity, and rule-based scoring.
8. The system shall explain why a job matched or failed.
9. The system shall record user feedback and use it to tune ranking weights.
10. The system shall expose the primary workflows through FastAPI.

## Data Requirements

- `UserProfile`: target titles, must-have skills, nice-to-have skills, years of experience, location, remote preference, salary range, work authorization constraints, excluded keywords, excluded companies.
- `JobPosting`: source, source id, company, title, description, responsibilities, requirements, salary range, location, remote type, apply URL, posted date, raw payload hash.
- `MatchResult`: score components, matched skills, missing requirements, explanation, source reliability score, recency score.
- `UserFeedback`: job id, decision, rating, reason tags, notes, timestamp.

## API Requirements

- `POST /profiles`
- `GET /profiles/{profile_id}`
- `POST /ingest/run`
- `GET /jobs`
- `GET /jobs/{job_id}`
- `POST /matches/search`
- `POST /matches/{job_id}/explain`
- `POST /feedback`
- `GET /sources`

## Non-Functional Requirements

- Deterministic scoring must be testable without an LLM.
- LLM output must be validated with Pydantic.
- Source connectors must fail independently so one broken source does not stop the entire ingestion run.
- Vector-store implementation must be swappable by configuration.
- The system must support fixture-based tests for normalization and ranking.
- The system must be deployable locally with Docker Compose and in production with container orchestration.

## Acceptance Criteria

- At least one source connector ingests jobs end to end into canonical storage.
- Ranked search returns explainable results for a sample profile.
- A user can mark a job as relevant or irrelevant and see the ranking inputs persist.
- A source outage does not break ingestion for other sources.
- A deployment can run the API, relational store, and vector store together in a reproducible environment.

