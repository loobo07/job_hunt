# Lever Ingestion Design

## Purpose

Lever is a common startup and tech-company careers-board source. It works well for employer-targeted ingestion because the job boards expose list and posting endpoints with rich job content.

Official docs: [Lever Developer Documentation](https://hire.lever.co/developer/documentation)

## Source Contract

- Endpoint: `GET /postings`
- Optional query params used by this design: `include=content`, `expand=followers`
- Response fields consumed: `id`, `text`, `state`, `categories`, `team`, `commitment`, `location`, `salary`, `urls.list`, `urls.show`, `urls.apply`, `workplaceType`, `tags`
- Only postings in `state=published` are indexed

## UML

```mermaid
classDiagram
class LeverAdapter {
  +fetch_postings(account)
  +fetch_posting(account, posting_id)
  +normalize(raw_posting)
}
class LeverClient {
  +list_postings(account, include_content)
  +get_posting(account, posting_id)
}
class LeverNormalizer {
  +to_job_posting(raw)
}
class JobPosting {
  +source
  +source_id
  +title
  +state
  +workplace_type
  +salary_range
  +urls
}

LeverAdapter --> LeverClient
LeverAdapter --> LeverNormalizer
LeverNormalizer --> JobPosting
```

## API Sequence

```mermaid
sequenceDiagram
participant Scheduler as Scheduler
participant Adapter as LeverAdapter
participant API as Lever API
participant Norm as LeverNormalizer
participant DB as Relational Store
participant VS as Vector Store

Scheduler->>Adapter: run ingestion for configured accounts
Adapter->>API: GET /postings?include=content
API-->>Adapter: posting list with content
Adapter->>API: GET /postings/{posting}
API-->>Adapter: full posting payload
Adapter->>Norm: normalize posting
Norm-->>Adapter: canonical JobPosting
Adapter->>DB: upsert canonical record
Adapter->>VS: index job text
Adapter-->>Scheduler: run summary
```

## Ingestion Notes

- Use the account slug as the board identifier.
- Prefer the posting list endpoint with `include=content` so the description is available without a second lookup.
- Preserve list/show/apply URLs as first-class fields.
- Treat workplace type, salary, and tags as useful ranking features.

## Normalization Rules

- Map `id` to `source_id`.
- Map `text` to `title`.
- Map `state` to a publishing-status field and index only `published` records.
- Map `commitment` and `categories` into employment-type and role-family fields.
- Map `location` to the canonical location string.
- Map the salary structure into the normalized compensation model when present.
- Map `urls.apply` to `apply_url` and `urls.show` to `source_url`.
- Preserve `workplaceType` as `remote`, `hybrid`, or `onsite` where available.
- Preserve `tags` as ranking metadata.

## Validation

- Verify posting state is published before indexing.
- Preserve the apply URL and show URL.
- Carry workplace type through to the canonical model for remote/hybrid filtering.
