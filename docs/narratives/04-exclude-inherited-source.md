# Narrative 04 — Exclude Inherited Source at Problem Level

## Purpose
Allow a child entity (problem) to exclude a specific source inherited from its ancestor (domain), refining effective context for that subtree.

## Actors
- Strategist (primary)
- SemOps CLI

## Preconditions
- Domain exists with at least one attached source (Narrative 02)
- Problem exists under the domain (Narrative 03)

## Narrative
1. Strategist reviews inherited sources at the problem and finds an irrelevant domain source.
2. Adds the source ID to the problem frontmatter under `sources.exclude`.
3. Runs `semops sources list --entity problem --include-inherited` to verify.
4. CLI lists effective sources for the problem, excluding the specified domain source.

## Success Criteria
- The excluded source no longer appears in the problem's effective source list.
- The source remains attached at the domain and continues to be inherited elsewhere.

## Mermaid (Flow)
```mermaid
flowchart TD
    A[Start] --> B[List problem sources (incl. inherited)]
    B --> C[Identify irrelevant inherited source]
    C --> D[Add source_id to problem frontmatter sources.exclude]
    D --> E[Run sources list again]
    E --> F[Resolution: attach@domain - exclude@problem]
    F --> G[Display list without excluded source]
    G --> X[End]
```

## Related BDD
- Exclude inherited source at problem level
