# Workable Documentation Agent Brief

## Mission

Produce and maintain source-specific documentation for Workable ingestion.

## Inputs

- Intended Workable public board source or company-provided feed
- [Job Board Ingestion Requirements](../requirements/job-board-ingestion-requirements.md)
- [DevOps and Infra Architecture](../architecture/devops-infra-architecture.md)

## Outputs

- UML class diagram for the Workable ingestion adapter
- API sequence diagram for the ingestion flow
- Workable ingestion design notes
- Validation rules and failure handling notes

## Scope

- Public board feeds only
- SMB and startup employer ingestion
- Minimal structured field handling
- Apply URL preservation

## Acceptance Criteria

- The doc explains that the connector is behind explicit configuration.
- The doc explains how jobs are rejected when there is not enough text to match.
- The doc explains how missing structured fields are handled.

