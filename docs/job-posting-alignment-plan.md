# Job Posting Alignment Application Plan

## Goal

Build a custom job-discovery application that finds postings aligned with a user's skills, experience, role preferences, compensation needs, location constraints, and work-style preferences. The application should combine structured filtering with semantic matching so it can find good-fit roles even when postings use different wording than the user's resume or preferred skill list.

## Recommended Job Sources

Prioritize sources with stable APIs or predictable public job-board feeds. Avoid relying on scraping large boards that prohibit it or change markup frequently.

| Source | Why it fits | Integration notes | Priority |
| --- | --- | --- | --- |
| Adzuna Jobs API | Broad aggregator with keyword, location, salary, full-time, permanent, and category filters. Useful for initial coverage. | Requires API credentials. The search endpoint returns listings and a description snippet, so plan to enrich with the apply/original URL where terms allow. | High |
| USAJOBS API | Official U.S. federal job source with a documented API, strong filters, and open federal roles. | Requires API key. Strong for public-sector, cleared, policy, data, software, and analyst roles. | High if federal roles are acceptable |
| Greenhouse Job Board API | Many tech companies publish jobs through Greenhouse. Public GET endpoints can return job content by company board token. | Best used with a curated employer list. Normalization is straightforward. | High |
| Lever Postings API | Many startups and tech companies publish via Lever. Useful for company-targeted discovery. | Public company job pages are common; API access patterns vary by endpoint and account. Use for curated employers first. | High |
| Ashby job postings | Common among high-growth startups. Useful for targeted company ingestion. | Treat as an employer-feed connector. Verify access and terms per endpoint/company before production ingestion. | Medium |
| Workable job board feeds | Useful for SMB and startup postings. | Use only where official/public feed access is available. | Medium |
| Remote-specific boards, such as Remotive | Focused remote listings can reduce noise for remote-first preferences. | Good secondary feed for remote roles; validate current API terms before production use. | Medium |
| LinkedIn, Indeed, ZipRecruiter, Google Jobs | High coverage and useful manual-discovery references. | Do not build the MVP around scraping them. Prefer official partner/API programs, saved-search alerts, user-provided URLs, or browser-assisted manual import where terms permit. | Low for automated ingestion |

## Recommended MVP Scope

The first version should be a local or single-user service that ingests jobs from API-friendly sources, ranks them against a user profile, and exposes a FastAPI interface for search, review, and feedback.

MVP outcomes:

- User can define a skillset manually or by uploading/pasting resume text.
- System expands skills into normalized aliases, seniority signals, role families, and deal-breakers.
- System ingests postings from at least Adzuna plus either USAJOBS or curated Greenhouse/Lever employers.
- System stores canonical job records and embeddings.
- System ranks jobs with an explainable fit score.
- User can mark jobs as relevant, ignored, applied, or false positive.
- Feedback improves future ranking without requiring retraining.

## Architecture

Use a modular Python backend with FastAPI at the boundary, Pydantic models for contracts, LangChain for LLM and embedding orchestration, and a pluggable vector store.

Recommended initial storage:

- PostgreSQL or SQLite for canonical job records, user profiles, source metadata, and feedback.
- Chroma for local development and rapid iteration.
- Pinecone or S3-backed vector storage for hosted/cloud deployment once ingestion volume and query latency justify it.

Core services:

- `source_connectors`: Fetch postings from Adzuna, USAJOBS, Greenhouse, Lever, and later optional boards.
- `normalization`: Convert each source payload into one canonical `JobPosting` schema.
- `profile_builder`: Turn a resume or preference form into a structured `UserProfile`.
- `embedding_service`: Embed job text and user profiles.
- `matching_service`: Combine vector similarity, structured filters, and rule-based boosts/penalties.
- `explanation_service`: Generate concise reasons a job matched or failed.
- `feedback_service`: Store user decisions and tune scoring weights.
- `api`: Expose ingestion, search, profile, job detail, feedback, and admin endpoints.

## Canonical Data Model

Use Pydantic as the source of truth for API contracts and internal normalized objects.

Important models:

- `UserProfile`: target titles, skills, years of experience, industries, locations, remote preference, salary range, authorization constraints, excluded companies, excluded keywords, must-have skills, nice-to-have skills.
- `JobPosting`: source, source job id, title, company, location, remote type, salary range, employment type, seniority, description, requirements, responsibilities, benefits, apply URL, posted date, expiration date, raw payload hash.
- `JobEmbeddingDocument`: job id, text chunks, embedding namespace, vector ids, embedding model, chunking strategy.
- `MatchResult`: job id, total score, vector score, skill score, title score, seniority score, location score, compensation score, penalties, explanation, matched skills, missing must-haves.
- `UserFeedback`: user id, job id, status, rating, rejection reasons, notes, timestamp.

## Matching Strategy

Use a hybrid ranker rather than pure vector search.

1. Hard filters remove obvious mismatches:
   - Location and remote constraints.
   - Salary minimum where known.
   - Visa/authorization constraints if user specifies them.
   - Excluded companies, industries, agencies, keywords, or contract types.
   - Required clearance or travel constraints.

2. Semantic retrieval finds candidates:
   - Embed the user's profile summary and target-role prompts.
   - Retrieve top candidates from Chroma/Pinecone/S3 vector index.
   - Use separate vectors for full description, requirements, responsibilities, and title/company metadata when useful.

3. Structured scoring ranks candidates:
   - Must-have skill coverage.
   - Nice-to-have skill coverage.
   - Role-title alignment.
   - Seniority alignment.
   - Domain/industry alignment.
   - Compensation/location fit.
   - Recency and source reliability.

4. LLM explanation summarizes fit:
   - Why this role matched.
   - Which skills were found.
   - Which important requirements are missing.
   - Suggested resume keywords for this specific job.

## LangChain Usage

Keep LangChain focused on orchestration rather than business logic.

Use it for:

- Resume/profile extraction chains.
- Skill normalization and alias expansion.
- Embedding pipelines.
- Retrieval from vector stores.
- Optional explanation generation.

Keep deterministic scoring in plain Python so it is testable and transparent.

## API Plan

FastAPI endpoints:

- `POST /profiles`: create or update a user skill/preference profile.
- `GET /profiles/{profile_id}`: retrieve profile.
- `POST /ingest/run`: run selected source connectors.
- `GET /jobs`: list normalized jobs with filters.
- `GET /jobs/{job_id}`: retrieve full normalized job detail.
- `POST /matches/search`: return ranked matches for a profile.
- `POST /matches/{job_id}/explain`: generate or retrieve match explanation.
- `POST /feedback`: record user feedback on a job.
- `GET /sources`: list enabled sources and sync status.

## Implementation Phases

### Phase 1: Discovery and Data Contracts

- Confirm target roles, geography, remote preference, salary expectations, and deal-breakers.
- Define Pydantic schemas for profiles, postings, matches, sources, and feedback.
- Create a small fixture set of representative job postings.
- Write unit tests for normalization and scoring rules.

### Phase 2: Ingestion MVP

- Implement Adzuna connector.
- Implement USAJOBS connector or a curated Greenhouse connector, depending on target market.
- Normalize source payloads into `JobPosting`.
- Add deduplication by source id, company/title/location hash, and apply URL.
- Store raw payloads for debugging and normalized rows for matching.

### Phase 3: Embeddings and Vector Search

- Add embedding generation for user profiles and job postings.
- Start with Chroma for local development.
- Define a vector-store interface so Pinecone or S3-backed storage can replace Chroma later.
- Add incremental indexing so unchanged postings are not re-embedded.

### Phase 4: Hybrid Ranking

- Implement hard filters.
- Implement vector retrieval.
- Add structured scoring weights.
- Return ranked `MatchResult` objects with component scores.
- Add tests that prove must-have filters, location filters, and seniority scoring work.

### Phase 5: Explanation and Feedback

- Add LLM-generated explanations with strict Pydantic output validation.
- Add feedback capture.
- Feed user feedback into weight adjustments, source blocking, and excluded-keyword learning.
- Add a review queue: `new`, `saved`, `ignored`, `applied`, `interviewing`, `rejected`.

### Phase 6: Productization

- Add scheduled ingestion.
- Add email or dashboard digests.
- Add observability for source failures and ranking drift.
- Add deployment profile: local SQLite/Chroma, then hosted Postgres/Pinecone or S3 vector backend.
- Add source-specific compliance review before enabling broad automated ingestion.

## Suggested Repository Structure

```text
job_hunt/
  app/
    api/
      routes_profiles.py
      routes_jobs.py
      routes_matches.py
      routes_sources.py
    core/
      config.py
      logging.py
    models/
      profile.py
      job.py
      match.py
      feedback.py
      source.py
    sources/
      base.py
      adzuna.py
      usajobs.py
      greenhouse.py
      lever.py
    services/
      normalization.py
      embeddings.py
      matching.py
      explanations.py
      feedback.py
    storage/
      relational.py
      vector_base.py
      chroma_store.py
      pinecone_store.py
      s3_vector_store.py
  tests/
    fixtures/
    test_normalization.py
    test_matching.py
    test_sources.py
  docs/
    job-posting-alignment-plan.md
```

## Key Decisions

- Start with API-friendly sources. Add high-coverage commercial boards later only through official access, partner access, alerts, or user-provided URLs.
- Start with Chroma locally. Keep a vector-store abstraction so Pinecone or S3 vector storage can be selected by configuration.
- Use hybrid scoring. Pure embeddings are useful for recall but too opaque for job-search decision making.
- Keep LLM-generated output advisory. The application should not hide deterministic scores or missing requirements.
- Treat feedback as first-class data from day one.

## Risks and Mitigations

- Job-board terms vary: add source-specific terms review before production use.
- Job descriptions are noisy: normalize text, preserve raw payloads, and score only relevant sections when possible.
- Salary is often missing: support unknown salary instead of penalizing too heavily, but allow user to require salary transparency.
- LLM extraction can drift: validate with Pydantic, store extraction confidence, and write regression tests over fixture postings.
- Duplicate postings are common: dedupe across source id, company/title/location, canonical URL, and text similarity.

## Immediate Next Steps

1. Pick the first two sources: recommended default is Adzuna plus Greenhouse curated employers, or Adzuna plus USAJOBS if federal roles are relevant.
2. Define the initial user profile manually before adding resume parsing.
3. Implement Pydantic schemas and fixture-based tests.
4. Implement one connector and one local vector store.
5. Build the first `/matches/search` endpoint with transparent component scores.

## Reference Links

- Adzuna Search API: https://developer.adzuna.com/docs/search
- USAJOBS Search API: https://developer.usajobs.gov/api-reference/get-api-search
- Greenhouse Job Board API: https://developers.greenhouse.io/job-board.html
- Lever developer documentation: https://hire.lever.co/developer/documentation
- Remotive remote jobs API: https://remotive.com/api/remote-jobs
