# USAJOBS Documentation Agent Brief

## Mission

Produce and maintain source-specific documentation for USAJOBS ingestion.

## Inputs

- [USAJOBS GET /api/Search](https://developer.usajobs.gov/api-reference/get-api-search)
- [Job Board Ingestion Requirements](../requirements/job-board-ingestion-requirements.md)
- [DevOps and Infra Architecture](../architecture/devops-infra-architecture.md)

## Outputs

- UML class diagram for the USAJOBS ingestion adapter
- API sequence diagram for the ingestion flow
- USAJOBS ingestion design notes
- Validation rules and failure handling notes

## Scope

- Keyword, title, salary, location, series, and grade filtering
- Federal metadata mapping
- Active announcement ingestion only
- Preservation of clearance and travel requirements

## Acceptance Criteria

- The doc explains how federal-specific fields map to the canonical schema.
- The doc explains how salary buckets are normalized.
- The doc explains how the connector handles active announcements versus historical records.

