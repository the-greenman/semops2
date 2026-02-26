# SemOps2 Directory Structure Examples

Ops entity types use **flat root collections** — each type has its own top-level directory, not a nested hierarchy.

Relationships are **canonical first-class records** stored as `EntityRelationship` messages and managed through the `EntityService` interface (CLI/API/MCP). Entity documents may mirror relationship links in YAML frontmatter for human readability, but the authoritative mutation boundary is the interface so validation, ID resolution, and projections remain consistent.

## Standard Ops Workspace

```
my-ops-workspace/
├── .semops-project                      # Workspace root marker
├── .semops/
│   └── config/
│       └── entity_types.yaml            # Entity types and relationship types
│
├── domain/                              # Root collection: domains
│   ├── cloud-governance/
│   │   ├── domain.md
│   │   └── sources/
│   ├── platform-engineering/
│   │   └── domain.md
│   └── security-operations/
│       └── domain.md
│
├── libraries/                           # Root collection: libraries (reference source lists)
│   ├── cloud-security-standards/
│   │   └── library.md
│   └── vendor-reference/
│       └── library.md
│
├── roles/                               # Root collection: roles (cross-cutting)
│   ├── ciso/
│   │   └── role.md
│   ├── platform-lead/
│   │   └── role.md
│   └── security-engineer/
│       └── role.md
│
├── meetings/                            # Root collection: meetings
│   ├── 2026-02-15-governance-review/
│   │   ├── meeting.md
│   │   └── sources/
│   └── 2026-02-08-platform-standup/
│       └── meeting.md
│
├── decisions/                           # Root collection: decisions
│   ├── adopt-zero-trust-model/
│   │   └── decision.md
│   └── migrate-to-platform-engineering/
│       └── decision.md
│
├── conversations/                       # Root collection: conversations
│   ├── slack-ciso-2026-02-12/
│   │   └── conversation.md
│   └── email-vendor-review-2026-02-10/
│       └── conversation.md
│
└── artefacts/                           # Root collection: artefacts
    ├── zero-trust-architecture-diagram/
    │   └── artefact.md
    └── platform-roadmap-q1-2026/
        └── artefact.md
```

## Entity Frontmatter and Relationship Links

Relationships between entities may be mirrored in the entity's YAML frontmatter. The canonical relationship records are stored as `EntityRelationship` messages and indexed separately for querying.

### decision.md example

```yaml
---
entity_type: "semops.core/decision"
entity_id: "DEC-adopt-zero-trust-model"
namespace: "semops.core"
decision_name: "Adopt Zero Trust Model"
decision_date: "2026-02-15"
status: "active"

# Typed relationships — validated against relationship_types config
relationships:
  - type: "semops.core/made_in"
    to: "MTG-2026-02-15-governance-review"
  - type: "semops.core/part_of"
    to: "DOM-cloud-governance"
  - type: "semops.core/affects"
    to: "DOM-cloud-governance"
  - type: "semops.core/affects"
    to: "ROLE-ciso"
  - type: "semops.core/references"
    to: "ART-zero-trust-architecture-diagram"
---

## Decision

...
```

### library.md example

```yaml
---
entity_type: "semops.core/library"
entity_id: "LIB-cloud-security-standards"
namespace: "semops.core"
library_name: "Cloud Security Standards"

relationships:
  - type: "semops.core/library_for"
    to: "DOM-cloud-governance"

sources:
  attach:
    - src_id: SRC-NCSC-CloudSecurityPrinciples-5fdbec50
      type: web_page
      title: "NCSC Cloud Security Principles"
---

## Library

...
```

### meeting.md example

```yaml
---
entity_type: "semops.core/meeting"
entity_id: "MTG-2026-02-15-governance-review"
namespace: "semops.core"
meeting_name: "Governance Review 2026-02-15"
meeting_date: "2026-02-15"

relationships:
  - type: "semops.core/part_of"
    to: "DOM-cloud-governance"
  - type: "semops.core/produces"
    to: "ART-zero-trust-architecture-diagram"

# Participants stored as participates_in relationships on the role entities,
# or inlined here for convenience:
participants:
  - role_id: "ROLE-ciso"
    capacity: "chair"
  - role_id: "ROLE-platform-lead"
    capacity: "contributor"
---

## Notes

...
```

## Context Detection

The context detector finds the nearest entity document by walking up from the current directory.

### Working directory: `/my-ops-workspace/decisions/adopt-zero-trust-model/`

```yaml
detected_context:
  current_entity:
    entity_type: "semops.core/decision"
    entity_id: "DEC-adopt-zero-trust-model"
    namespace: "semops.core"
    slug: "adopt-zero-trust-model"

  relationships:
    - type: "semops.core/made_in"
      to: "MTG-2026-02-15-governance-review"
    - type: "semops.core/part_of"
      to: "DOM-cloud-governance"
    - type: "semops.core/affects"
      to: "DOM-cloud-governance"

  available_operations:
    - "semops decision analyze"
    - "semops decision analyze --prompt extract_rationale"
    - "semops decision relate"
    - "semops decision list --related-to MTG-2026-02-15-governance-review"
```

### Working directory: `/my-ops-workspace/meetings/2026-02-15-governance-review/`

```yaml
detected_context:
  current_entity:
    entity_type: "semops.core/meeting"
    entity_id: "MTG-2026-02-15-governance-review"
    namespace: "semops.core"
    slug: "2026-02-15-governance-review"

  available_operations:
    - "semops meeting analyze"
    - "semops meeting analyze --prompt extract_decisions"
    - "semops meeting analyze --prompt extract_actions"
    - "semops decision list --related-to MTG-2026-02-15-governance-review"
```

## CLI Command Examples

```bash
# List all decisions
semops decision list

# List decisions that belong to a domain
semops decision list --related-to DOM-cloud-governance --relationship part_of

# List decisions made in a specific meeting
semops decision list --related-to MTG-2026-02-15-governance-review --relationship made_in

# Create a new decision (uses decision.md.j2 create template)
semops decision create --name "Adopt Zero Trust Model"

# Run a named prompt from the decision template bundle
semops decision analyze --id DEC-adopt-zero-trust-model --prompt extract_rationale

# Show what relationship types are available
semops config relationship-types list

# Show all entity types and their namespaces
semops config entity-types list
```

## Third-Party Entity Types

Third-party entity types install alongside built-ins with their own namespace. The directory structure is identical:

```
my-ops-workspace/
├── domain/                              # semops.core/domain (built-in)
├── decisions/                           # semops.core/decision (built-in)
└── governance-reviews/                  # com.acme.governance/governance-review (third-party)
    └── q1-2026-review/
        └── governance-review.md
```

```yaml
# governance-review.md
---
entity_type: "com.acme.governance/governance-review"
entity_id: "GRV-q1-2026-review"
namespace: "com.acme.governance"
...
---
```

The `ConfigManager` keeps `semops.core/decision` and `com.acme.governance/governance-review` in separate namespace entries — no collision regardless of prefix overlap.
