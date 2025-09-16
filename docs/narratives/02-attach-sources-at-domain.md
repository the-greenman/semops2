# Narrative 02 — Attach Sources at Domain Level

## Purpose
Attach broad, foundational sources to a domain so that descendants inherit context by default.

## Actors
- Strategist (primary)
- SemOps CLI

## Preconditions
- Domain exists (see Narrative 01)
- `config/source_types.yaml` defines `web_page` (or relevant types)

## Narrative
1. Strategist identifies a key reference (e.g., NCSC Cloud Security Principles).
2. Runs `semops source attach --type web_page --url https://www.ncsc.gov.uk/collection/cloud-security-principles` in the domain directory.
3. CLI validates the source type and generates a stable `source_id` (URL-hash-based).
4. CLI processes the source (extract → process → chunk → enrich), then indexes it.
5. Domain frontmatter is updated: `sources.attach` includes the `source_id` with metadata.

## Success Criteria
- Domain frontmatter includes the attached `source_id` with metadata.
- Source is processed and indexed; ready for inheritance.

## Mermaid (Flow)
```mermaid
flowchart TD
    A[Start] --> B[User runs semops source attach]
    B --> C[Validate source_types.yaml]
    C --> D{Type valid?}
    D -- No --> E[Error + hint]
    D -- Yes --> F[Generate stable source_id]
    F --> G[Extract/Process/Chunk/Enrich]
    G --> H[Index vector/metadata]
    H --> I[Write to domain frontmatter sources.attach]
    I --> J[Show success + source_id]
    E --> X[End]
    J --> X[End]
```

## Related BDD
- Attach sources at the domain level
- Inherit sources from ancestors (see Narrative 03)
