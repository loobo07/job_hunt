# Workable Ingestion Design

## Purpose

Workable is a practical SMB and startup source. It should be integrated only through public, permitted board feeds or official endpoint patterns.

## Source Contract

- Endpoint: company-specific public job board or public feed
- Required configuration: employer identifier or public board URL
- Response fields consumed: job id, title, company name, location, apply URL, description, compensation if exposed, and any public metadata fields
- Exact endpoint shape must be confirmed for each employer before implementation

## UML

```mermaid
classDiagram
class WorkableAdapter {
  +fetch_board(company)
  +fetch_jobs(company)
  +normalize(raw_job)
}
class WorkableClient {
  +get_board(company)
  +get_jobs(company)
}
class WorkableNormalizer {
  +to_job_posting(raw)
}
class JobPosting {
  +source
  +source_id
  +title
  +company
  +location
  +apply_url
}

WorkableAdapter --> WorkableClient
WorkableAdapter --> WorkableNormalizer
WorkableNormalizer --> JobPosting
```

## API Sequence

```mermaid
sequenceDiagram
participant Scheduler as Scheduler
participant Adapter as WorkableAdapter
participant Feed as Workable Board
participant Norm as WorkableNormalizer
participant DB as Relational Store
participant VS as Vector Store

Scheduler->>Adapter: run ingestion for configured boards
Adapter->>Feed: GET public board feed
Feed-->>Adapter: job list
Adapter->>Norm: normalize job payload
Norm-->>Adapter: canonical JobPosting
Adapter->>DB: upsert canonical record
Adapter->>VS: index job text
Adapter-->>Scheduler: run summary
```

## Ingestion Notes

- Keep this connector behind explicit configuration.
- Prefer public board feeds and avoid brittle scraping.
- Preserve company and role metadata even when a posting has minimal structured fields.

## Normalization Rules

- Map the public job identifier to `source_id`.
- Map the posting title to `title`.
- Map the employer name to `company`.
- Map the canonical public job link to `apply_url`.
- Preserve description text as the canonical body text.
- Preserve any salary or location metadata that the feed exposes.
- Mark the source as employer-specific and optional.

## Validation

- Verify the board is public and reachable before indexing.
- Require a non-empty title, company, and apply URL or canonical posting URL.
- Reject postings that do not have enough text to be useful for matching.
