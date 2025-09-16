# Narrative 01 — Create Domain Root Entity

## Purpose
Establish a new domain as the root of a knowledge tree, creating the directory and initial definition document with deterministic ID and slug.

## Actors
- Strategist (primary)
- SemOps CLI

## Preconditions
- Repo at `LW-Products/`
- Valid `config/entity_types.yaml` with `domain` defined as a root
- Jinja2 templates available for `domain`

## Narrative
1. Strategist decides to define a new domain: "Cloud Security Governance".
2. Runs `semops domain create --domain-name "Cloud Security Governance"`.
3. CLI validates configuration and computes slug `cloud-security-governance`.
4. CLI generates a deterministic ID `DOM-cloud-security-governance` (kebab-case format) and writes `domain/cloud-security-governance/domain.md` (type-based filename).
5. Frontmatter includes ID, slug, timestamps, and placeholders for content.

## Success Criteria
- New domain directory created with a markdown file.
- Frontmatter contains deterministic ID and slug.

## Mermaid (Flow)
```mermaid
flowchart TD
    A[Start] --> B[User invokes semops domain create]
    B --> C[Load entity_types.yaml]
    C --> D{Config valid?}
    D -- No --> E[Return error with hints]
    D -- Yes --> F[Compute slug + ID]
    F --> G[Render Jinja2 template]
    G --> H[Write domain/{slug}/domain.md]
    H --> I[Show success + path]
    E --> X[End]
    I --> X[End]
```

## Related BDD
- Configuration valid before use
- Create domain with deterministic ID and slug
