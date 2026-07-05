# Job Hunt Backend MVP

This repository now includes a test-first FastAPI backend MVP for job ingestion and matching.

## Local Setup

Install and run tests with `uv`:

```bash
uv run pytest
```

Start the local Postgres service with Podman Compose:

```bash
podman compose up -d postgres
```

Run the API against the local Postgres database:

```bash
uv run uvicorn --factory app.api.main:create_default_app --reload
```

The default database URL is:

```text
postgresql+psycopg://job_hunt:job_hunt@localhost:5432/job_hunt
```

Override it with `DATABASE_URL` or a local `.env` file.

## Current MVP Scope

- Canonical `UserProfile`, `JobPosting`, `MatchResult`, and `UserFeedback` models.
- Fixture-backed Adzuna and Greenhouse ingestion.
- Local SQLAlchemy persistence with Postgres support.
- Deterministic fake vector scoring for stable tests.
- FastAPI endpoints for profiles, ingestion, jobs, matching, explanations, feedback, and source status.
