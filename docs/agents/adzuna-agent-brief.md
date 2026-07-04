# Adzuna Documentation Agent Brief

## Mission

Produce and maintain source-specific documentation for Adzuna ingestion.

## Inputs

- [Adzuna Search API](https://developer.adzuna.com/docs/search)
- [Job Board Ingestion Requirements](../requirements/job-board-ingestion-requirements.md)
- [DevOps and Infra Architecture](../architecture/devops-infra-architecture.md)

## Outputs

- UML class diagram for the Adzuna ingestion adapter
- API sequence diagram for the ingestion flow
- Adzuna ingestion design notes
- Validation rules and failure handling notes

## Scope

- Search query construction
- Salary, location, and employment-type filtering
- Snippet-based description handling
- Deduplication by source id and redirect URL

## Acceptance Criteria

- The doc explains that Adzuna returns job advertisements and truncated description snippets.
- The doc explains how the adapter maps search results into the canonical `JobPosting`.
- The doc explains how the worker handles missing salary and partial descriptions.

