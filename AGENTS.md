# AGENTS.md

## Project Grounding

This repository is a Python/FastAPI backend MVP for a job-posting ingestion and matching system. It grew out of the docs in `docs/`, which remain the source of truth for product scope, canonical vocabulary, source-ingestion expectations, and infrastructure direction.

Do not treat this as a generic job-board scraper. The intended system ingests API-friendly or explicitly configured sources, normalizes postings into canonical models, ranks them against a user profile, and returns explainable matches.

## Current Architecture

- API boundary: `app/api/main.py`
- Domain models: `app/domain/models.py`
- Matching logic: `app/services/matching.py`
- Ingestion orchestration: `app/services/ingestion.py`
- Source fixtures/adapters: `app/sources/`
- Persistence: `app/storage/`
- Tests: `tests/`
- Planning and source designs: `docs/`

Use the canonical names and field vocabulary from the docs and models:

- `UserProfile`
- `JobPosting`
- `MatchResult`
- `UserFeedback`
- `source_id`
- `apply_url`
- `posted_at`
- `remote_type`

## Development Commands

Use `uv` for Python dependency management and command execution.

```bash
uv run pytest
```

Run the API locally with:

```bash
uv run uvicorn --factory app.api.main:create_default_app --reload
```

Start local Postgres with:

```bash
podman compose up -d postgres
```

## Working Rules

- Run `uv run pytest` after modifying Python code or API behavior.
- Keep deterministic scoring in plain Python so tests can validate ranking without an LLM.
- Preserve raw source payloads or enough fixture data to debug normalization decisions.
- Keep source connectors isolated so one source failure does not break the whole ingestion run.
- Do not add new production dependencies without explicit user confirmation.
- Prefer focused changes over broad refactors.
- Keep docs aligned when changing canonical models, endpoint behavior, or source-ingestion assumptions.

## Source Policy

Prefer API-backed or explicitly configured source ingestion. Do not add browser scraping for large job boards unless the docs and user request explicitly allow it.

Adzuna and Greenhouse are the current fixture-backed MVP sources. USAJOBS, Lever, Ashby, Workable, and Remotive are documented as planned or optional sources.

## Testing Expectations

Tests should cover:

- Pydantic validation and normalization rules.
- Source fixture normalization.
- Repository persistence behavior.
- Matching score components and explanations.
- FastAPI endpoint behavior.

When adding behavior, prefer fixture-based tests that make the expected canonical fields and score components obvious.
