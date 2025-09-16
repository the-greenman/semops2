# Narrative 05 — Cross-Domain Source Sharing

## Purpose
Enable a domain to declare a relationship (e.g., `depends_on`) to another domain and optionally share sources according to policy.

## Actors
- Architect (primary)
- SemOps CLI

## Preconditions
- Two domains exist (e.g., "Cloud Security Governance" and "Platform Engineering")
- Relationship type configured in `entity_types.yaml` with `share_sources: true` and `max_depth`
- Domain A has attached sources

## Narrative
1. Architect establishes a relationship: Domain B `depends_on` Domain A.
2. Architect runs `semops relationships add --from B --to A --type depends_on`.
3. CLI records the relationship and validates `share_sources` policy.
4. Architect lists sources for Domain B with related included.
5. CLI unions eligible sources from Domain A into Domain B’s effective list, marking provenance and respecting `max_depth`.

## Success Criteria
- Relationship is stored and visible via `semops relationships list`.
- Listing sources for Domain B (with related) includes Domain A’s eligible sources with provenance.

## Mermaid (Sequence)
```mermaid
sequenceDiagram
    participant U as Architect
    participant CLI as SemOps CLI
    participant CFG as Config (entity_types)
    participant KS as KnowledgeService

    U->>CLI: relationships add --from B --to A --type depends_on
    CLI->>CFG: Validate relationship type & share_sources
    CFG-->>CLI: Valid
    CLI->>KS: Persist relationship (B depends_on A)
    KS-->>CLI: OK

    U->>CLI: sources list --entity B --include-related
    CLI->>KS: Resolve effective sources for B
    KS->>KS: Union B.attach + ancestors + related(A) within max_depth
    KS-->>CLI: Effective sources with provenance
    CLI-->>U: Display sources (incl. related from A)
```

## Related BDD
- Roots and cross-domain relationships
- Share sources across related domains
