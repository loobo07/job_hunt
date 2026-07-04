# Ashby Documentation Agent Brief

## Mission

Produce and maintain source-specific documentation for Ashby ingestion.

## Inputs

- Intended Ashby careers board source and any company-provided public feed
- [Job Board Ingestion Requirements](../requirements/job-board-ingestion-requirements.md)
- [DevOps and Infra Architecture](../architecture/devops-infra-architecture.md)

## Outputs

- UML class diagram for the Ashby ingestion adapter
- API sequence diagram for the ingestion flow
- Ashby ingestion design notes
- Validation rules and failure handling notes

## Scope

- Curated employer ingestion
- Remote and hybrid metadata capture
- Company-specific public feeds only
- Dedupe across source id and canonical URL

## Acceptance Criteria

- The doc explains that Ashby is handled as a curated employer connector.
- The doc explains how workplace type and tags support ranking.
- The doc explains how the connector avoids unsupported scraping.

