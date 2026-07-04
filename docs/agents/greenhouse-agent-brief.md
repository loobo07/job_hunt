# Greenhouse Documentation Agent Brief

## Mission

Produce and maintain source-specific documentation for Greenhouse ingestion.

## Inputs

- [Greenhouse Job Board API](https://developers.greenhouse.io/job-board.html)
- [Job Board Ingestion Requirements](../requirements/job-board-ingestion-requirements.md)
- [DevOps and Infra Architecture](../architecture/devops-infra-architecture.md)

## Outputs

- UML class diagram for the Greenhouse ingestion adapter
- API sequence diagram for the ingestion flow
- Greenhouse ingestion design notes
- Validation rules and failure handling notes

## Scope

- Public job board access by board token
- Optional `content=true` fetching
- Company-specific curated ingestion
- Department and office metadata mapping

## Acceptance Criteria

- The doc explains that public GET endpoints do not require authentication.
- The doc explains how the board token identifies the employer.
- The doc explains how `internal_job_id` and `metadata` are handled.

