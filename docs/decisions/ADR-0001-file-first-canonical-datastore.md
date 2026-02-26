# ADR-0001: File-First Canonical Datastore

- **Status:** Accepted
- **Date:** 2026-02-26
- **Owners:** Architecture / Platform Governance
- **Decision Type:** Persistence and consistency model

## Context

SemOps2 currently has conflicting documentation about canonical persistence:

- Some sections define markdown + frontmatter as canonical and graph/vector as derived indexes.
- Other sections imply graph-first commit semantics in workflow examples.

This creates implementation ambiguity and increases risk of drift, split-brain behavior, and policy/audit inconsistency.

## Decision

SemOps2 adopts a **file-first canonical datastore** model:

1. **Canonical source of truth:** Markdown + frontmatter entity documents.
2. **Derived stores:** Entity graph, knowledge graph, and vector indexes are projections derived from canonical documents.
3. **Mutation boundary:** All mutations must pass through Entity Server.
4. **Write contract:** A mutation is complete when canonical document write succeeds and index updates are either:
   - completed successfully, or
   - queued via durable outbox with guaranteed reconciliation.

## Non-Goals

- Graph-first canonical persistence is not adopted in this decision.
- Direct client writes to graph/vector stores are prohibited.

## Alternatives Considered

### A. Graph-first canonical

Rejected for now due to:

- weaker human-auditable primary record,
- higher lock-in and schema coupling risk,
- conflict with existing canonical-document architecture invariants.

### B. Dual-canonical (files + graph)

Rejected due to:

- high reconciliation complexity,
- ambiguous conflict resolution,
- emergent failure behavior under partial outages.

## Consequences

### Positive

- Strong auditability and inspectability (diff-friendly, portable records).
- Clear governance path for authority and provenance checks.
- Deterministic rebuild path for graph/vector indexes.

### Costs

- Requires disciplined outbox/retry/reconciliation implementation.
- Requires explicit sync-state metadata and operational repair tooling.

## Required Runtime Guardrails

1. Entity Server is the only mutation boundary.
2. No direct writes to graph/vector from clients, workflows, MCP tools, or auxiliary scripts.
3. Sync status fields must be persisted and observable for each mutation.
4. Reconciliation workflows must be idempotent and retry-safe.
5. Read paths for governance-critical views should prefer canonical docs or strongly consistent projections.

## Auditability and Verification

This decision is auditable when all of the following are true:

1. Mutation logs include document revision and index sync status metadata.
2. A reconciliation report can prove eventual consistency for failed/queued index updates.
3. Tests assert that graph/vector indexes can be rebuilt from canonical documents.
4. Architecture docs consistently describe file-first canonical semantics.

## Follow-Up Documentation Updates (Required)

- Update all architecture docs to remove graph-first wording.
- Align workflow examples to commit canonical docs first, then update/queue indexes.
- Clarify two-graph model as derived, role-separated projections.
- Ensure IDL examples and MCP examples do not imply bypassing canonical write semantics.

## Change Control

Any proposal to adopt graph-first or dual-canonical persistence must:

1. Introduce a new ADR that supersedes this decision.
2. Include failure-mode analysis, rollback design, and operational SLO impact.
3. Provide an audit plan for canonical document integrity and projection consistency.
