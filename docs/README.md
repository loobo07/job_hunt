# Job Hunt Spec Package

This package contains the shared requirements, per-source ingestion designs, agent briefs, and infra architecture for the job-matching system.

## Package Map

- [Requirements](./requirements/job-board-ingestion-requirements.md)
- [DevOps and Infra Architecture](./architecture/devops-infra-architecture.md)
- [Documentation Orchestration Plan](./agents/documentation-orchestration.md)
- [Source Documentation Agents](./agents/README.md)
- [Adzuna Ingestion Design](./designs/adzuna-ingestion-design.md)
- [USAJOBS Ingestion Design](./designs/usajobs-ingestion-design.md)
- [Greenhouse Ingestion Design](./designs/greenhouse-ingestion-design.md)
- [Lever Ingestion Design](./designs/lever-ingestion-design.md)
- [Ashby Ingestion Design](./designs/ashby-ingestion-design.md)
- [Workable Ingestion Design](./designs/workable-ingestion-design.md)
- [Remotive Ingestion Design](./designs/remotive-ingestion-design.md)

## Naming Rules

- Use `JobPosting`, `UserProfile`, `MatchResult`, and `UserFeedback` everywhere.
- Use `source_id` for the source-native identifier.
- Use `apply_url` for the primary action link.
- Use `posted_at` for the publication timestamp.
- Use `remote_type` for remote, hybrid, or onsite classification.

## Diagram Artifacts

- [Diagram Artifacts README](./assets/diagrams/README.md)
- Rendered SVG and PNG diagrams can be added under `docs/assets/diagrams/` when the export step is run.
