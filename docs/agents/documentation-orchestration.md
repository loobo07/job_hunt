# Documentation Orchestration Plan

## Goal

Use separate documentation agents to generate and maintain source-specific ingestion docs for each intended job board, while keeping the requirements, architecture, and vocabulary consistent across the whole document set.

## Agent Split

- `adzuna-doc-agent`: writes and updates Adzuna source documentation.
- `usajobs-doc-agent`: writes and updates USAJOBS source documentation.
- `greenhouse-doc-agent`: writes and updates Greenhouse source documentation.
- `lever-doc-agent`: writes and updates Lever source documentation.
- `ashby-doc-agent`: writes and updates Ashby source documentation.
- `workable-doc-agent`: writes and updates Workable source documentation.
- `remotive-doc-agent`: writes and updates Remotive source documentation.
- `infra-doc-agent`: writes and updates the DevOps and infra architecture document.
- `requirements-doc-agent`: owns the shared requirements/spec document.

## Responsibilities

Each source agent must:

- Use the intended source API or board feed as the authoritative reference.
- Document the ingestion contract for that source only.
- Include one UML class diagram and one API sequence diagram.
- Describe normalization rules into the shared canonical models.
- Call out source-specific validation and failure handling.
- Link back to the shared requirements and infra docs.

The infra agent must:

- Document the runtime, storage, vector-store, queue, and deployment stack.
- Explain local, CI, and production environments.
- Define operational, security, and observability requirements.

The requirements agent must:

- Own the cross-source scope and acceptance criteria.
- Define the canonical schema and API surface.
- Keep the board-specific docs aligned to one vocabulary.

## Workflow

1. Requirements agent updates the shared scope and canonical model.
2. Infra agent updates deployment assumptions and operational constraints.
3. Source agents generate or revise source docs independently.
4. A final review pass reconciles naming, fields, and sequence diagrams.

## Consistency Rules

- All source docs must refer to `JobPosting`, `UserProfile`, `MatchResult`, and `UserFeedback` using the same field vocabulary.
- All sequence diagrams must show ingestion flowing through source client, normalizer, relational store, and vector store.
- No source doc may invent a source-specific storage model that conflicts with the shared requirements doc.
- No source doc may imply browser scraping unless the shared requirements doc explicitly allows it.
- All rendered diagram artifacts must be generated from the checked-in Mermaid sources or from a clearly labeled derived export.
