# Lever Documentation Agent Brief

## Mission

Produce and maintain source-specific documentation for Lever ingestion.

## Inputs

- [Lever Developer Documentation](https://hire.lever.co/developer/documentation)
- [Job Board Ingestion Requirements](../requirements/job-board-ingestion-requirements.md)
- [DevOps and Infra Architecture](../architecture/devops-infra-architecture.md)

## Outputs

- UML class diagram for the Lever ingestion adapter
- API sequence diagram for the ingestion flow
- Lever ingestion design notes
- Validation rules and failure handling notes

## Scope

- Public posting feeds with rich content
- Board/account slug routing
- Preserve list, show, and apply URLs
- Support remote, hybrid, and onsite metadata

## Acceptance Criteria

- The doc explains how the posting list endpoint supports content retrieval.
- The doc explains how salary and workplace type are normalized.
- The doc explains how published state gating works before indexing.

