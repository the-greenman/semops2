# Narrative 03 — Create Problem and Inherit Sources

## Purpose
Create a problem under a domain using context resolution, and verify inherited sources appear as effective context.

## Actors
- Strategist (primary)
- SemOps CLI

## Preconditions
- Domain exists with attached sources (Narratives 01 and 02)
- Working directory is within the domain folder

## Narrative
1. Strategist decides to formalize a problem under the domain: "Operating Model Fragmentation".
2. Runs `semops problem create operating-model-fragmentation --name "Operating Model Fragmentation" --part-of DOM-<domain-slug>` from the domain directory.
3. CLI computes slug `operating-model-fragmentation`, creates `problems/operating-model-fragmentation/problem.md` with a deterministic ID `PROB-operating-model-fragmentation` (kebab-case), and records a relationship to the domain.
4. Strategist lists effective sources at the problem level.
5. CLI shows domain-attached sources as `inherited` with provenance set to the domain.

## Success Criteria
- Problem file exists with resolved `domain_id` in frontmatter.
- Listing problem sources shows inherited domain sources with `scope: inherited`.

## Mermaid (Flow)
```mermaid
flowchart TD
    A[Start] --> B[User runs semops problem create]
    B --> C[Detect context (domain)]
    C --> D[Compute slug + ID]
    D --> E[Render template + write problems/{problem-slug}/problem.md]
    E --> F[User runs semops sources list --entity problem]
    F --> G[Resolve inherited sources from domain]
    G --> H[Display effective sources with provenance]
    H --> X[End]
```

## Related BDD
- Create problem with context-resolved parent
- Problem lists inherited sources from domain
