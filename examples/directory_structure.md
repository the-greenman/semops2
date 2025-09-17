# SemOps2 Directory Structure Examples

This document shows how the generic entity configuration maps to actual directory structures, demonstrating the flexibility of the new architecture.

## Standard Nested Hierarchy Example

```
domain/cloud-security/                   # Root domain directory
├── domain.md                            # Type-based filename for context detection
├── sources/                             # Domain-level sources (unchanged)
│   ├── sources.md
│   ├── raw/
│   └── notes/
├── internal/                            # Internal sources (unchanged)
│   ├── raw/
│   └── notes/
├── working/                             # Working files (unchanged)
│   ├── domain_analysis_generated.md
│   └── domain_guidance.md
├── problems/                            # Problem entity directory
│   ├── compliance-challenges/           # Problem slug directory
│   │   ├── problem.md                   # Type-based filename
│   │   ├── sources/                     # Problem-specific sources
│   │   ├── working/                     # Problem analysis files
│   │   └── personas/                    # Personas FOR THIS PROBLEM
│   │       ├── security-manager/
│   │       │   ├── persona.md           # Type-based filename
│   │       │   └── working/
│   │       └── compliance-officer/
│   │           ├── persona.md
│   │           └── working/
│   └── cost-optimization/               # Different problem
│       ├── problem.md
│       ├── sources/
│       ├── working/
│       └── personas/                    # Different persona instances
│           └── budget-controller/
│               ├── persona.md
│               └── working/
└── solutions/                           # Solution entity directory (NEW)
    └── zero-trust-platform/            # Solution slug directory
        ├── solution.md                  # Type-based filename
        ├── sources/                     # Solution-specific sources
        ├── working/                     # Solution analysis files
        └── features/                    # Features FOR THIS SOLUTION
            ├── threat-detection/
            │   ├── feature.md           # Type-based filename
            │   └── working/
            └── compliance-dashboard/
                ├── feature.md
                └── working/
```

## Extended Hierarchy with New Entity Types

```
domain/cloud-security/                  # Consistent kebab-case
├── domain.md                           # Type-based filename for context detection
├── problems/
│   └── compliance-challenges/          # Directory per entity instance
│       └── problem.md                  # Type-based filename
├── personas/
│   └── security-manager/               # Directory per entity instance
│       └── persona.md                  # Type-based filename
├── products/
│   └── zero-trust-platform/           # Directory per entity instance
│       └── product.md                  # Type-based filename
├── solutions/                          # NEW: Solution approaches
│   └── ai-threat-detection/            # Kebab-case directory
│       ├── solution.md                 # Type-based filename
│       └── features/                   # NEW: Features within solutions
│           ├── real-time-monitoring/   # Kebab-case directories
│           │   └── feature.md          # Type-based filename
│           ├── threat-correlation/
│           │   └── feature.md
│           └── automated-response/
│               └── feature.md
├── research/                           # NEW: Research artifacts
│   ├── market-analysis-2024/
│   │   └── research.md                 # Type-based filename
│   ├── user-interview-summary/
│   │   └── research.md
│   └── competitive-landscape/
│       └── research.md
├── strategies/                         # NEW: Strategic initiatives
│   └── go-to-market-strategy/
│       ├── strategy.md                 # Type-based filename
│       └── initiatives/                # NEW: Specific initiatives
│           ├── partnership-program/
│           │   └── initiative.md       # Type-based filename
│           ├── content-marketing/
│           │   └── initiative.md
│           └── analyst-engagement/
│               └── initiative.md
└── integrations/                       # NEW: Integration points
    ├── existing-siem-integration/
    │   └── integration.md              # Type-based filename
    └── cloud-provider-connectors/
        └── integration.md
```

## Alternative Hierarchy: Market Segment Focus

```
domain/enterprise-software/
├── domain.md                           # Type-based filename
├── segments/                           # NEW: Market segments
│   ├── small-business/                 # Kebab-case directory
│   │   └── segment.md                  # Type-based filename
│   ├── mid-market/
│   │   └── segment.md
│   └── enterprise/
│       └── segment.md
├── problems/
│   ├── digital-transformation/         # Kebab-case directories
│   │   └── problem.md                  # Type-based filename
│   └── legacy-modernization/
│       └── problem.md
└── personas/
    ├── small-business/                 # Personas organized by segment
    │   ├── small-biz-owner/            # Kebab-case directories
    │   │   └── persona.md              # Type-based filename
    │   └── it-generalist/
    │       └── persona.md
    ├── mid-market/
    │   ├── it-director/
    │   │   └── persona.md
    │   └── business-analyst/
    │       └── persona.md
    └── enterprise/
        ├── enterprise-architect/
        │   └── persona.md
        └── procurement-manager/
            └── persona.md
```

## Cross-Cutting Entity Types

```
domain/cloud-security/
├── domain.md                           # Type-based filename
├── [standard hierarchy...]
├── integrations/                       # Cross-cutting integrations
│   ├── siem-connector/                 # Kebab-case directories
│   │   └── integration.md              # Type-based filename
│   ├── cloud-api-gateway/              # Integration specifications
│   │   └── integration.md
│   └── third-party-feeds/
│       └── integration.md
├── research/                           # Domain-level research
│   ├── threat-landscape-2024/          # Kebab-case directories
│   │   └── research.md                 # Type-based filename
│   ├── customer-pain-points/           # User research
│   │   └── research.md
│   └── technology-trends/              # Technical research
│       └── research.md
└── strategies/                         # Strategic planning
    ├── market-penetration/             # Kebab-case directories
    │   └── strategy.md                 # Type-based filename
    ├── product-roadmap/                # Product strategy
    │   └── strategy.md
    └── partnership-strategy/           # Go-to-market strategy
        └── strategy.md
```

## Context Detection Examples

The generic context detector understands entity relationships from directory structure:

### Working Directory: `/domain/cloud-security/problems/compliance-challenges/personas/security-manager/`
```yaml
detected_context:
  current_entity:
    entity_type: "persona"
    entity_id: "PERS-security-manager"
    slug: "security-manager"
    nesting_level: 3

  hierarchy:
    domain:
      entity_id: "DOM-cloud-security"
      slug: "cloud-security"
      path: "/domain/cloud-security"
      file: "domain.md"
    problem:
      entity_id: "PROB-compliance-challenges"
      slug: "compliance-challenges"
      path: "/domain/cloud-security/problems/compliance-challenges"
      file: "problem.md"
      parent_id: "DOM-cloud-security"
    persona:
      entity_id: "PERS-security-manager"
      slug: "security-manager"
      path: "/domain/cloud-security/problems/compliance-challenges/personas/security-manager"
      file: "persona.md"
      parent_id: "PROB-compliance-challenges"

  scoped_relationships:
    - "Persona scoped to compliance-challenges problem"
    - "Problem scoped to cloud-security domain"
```

### Working Directory: `/domain/cloud-security/solutions/zero-trust-platform/features/threat-detection/`
```yaml
detected_context:
  current_entity:
    entity_type: "feature"
    entity_id: "FEAT-threat-detection"
    slug: "threat-detection"
    nesting_level: 3

  hierarchy:
    domain:
      entity_id: "DOM-cloud-security"
      slug: "cloud-security"
      path: "/domain/cloud-security"
      file: "domain.md"
    solution:
      entity_id: "SOL-zero-trust-platform"
      slug: "zero-trust-platform"
      path: "/domain/cloud-security/solutions/zero-trust-platform"
      file: "solution.md"
      parent_id: "DOM-cloud-security"
    feature:
      entity_id: "FEAT-threat-detection"
      slug: "threat-detection"
      path: "/domain/cloud-security/solutions/zero-trust-platform/features/threat-detection"
      file: "feature.md"
      parent_id: "SOL-zero-trust-platform"

  scoped_relationships:
    - "Feature scoped to zero-trust-platform solution"
    - "Solution scoped to cloud-security domain"
```

## CLI Command Examples

Generic commands work with any entity type defined in configuration:

```bash
# Standard entity types (unchanged from v1)
semops domain list
semops problem get PROB-compliance-challenges
semops persona create --name "Security Manager"

# New entity types (automatically available)
semops solution list                    # Lists solutions in current context
semops feature create --name "Real-time Monitoring"
semops research get RES-market-analysis-2024

# Market segments
semops market-segment list              # Auto-generated command
semops market-segment create --name "Small Business"

# Cross-cutting entities
semops integration list                 # Lists all integrations
semops strategy analyze STRAT-go-to-market
```

## Template Variable Context

Each entity type automatically receives appropriate context variables:

### Solution Template Variables
```yaml
# Available in solution.md.j2 template:
{
  "entity_type": "solution",
  "solution_id": "SOL-ai-threat-detection",
  "solution_name": "AI Threat Detection",
  "solution_slug": "ai-threat-detection",
  "product_id": "PROD-zero-trust-platform",  # Parent context
  "domain_id": "DOM-cloud-security",         # Ancestor context
  "template_id": "TEMPLATE-solution",
  "template_version": "1.0.0"
}
```

### Feature Template Variables
```yaml
# Available in feature.md.j2 template:
{
  "entity_type": "feature",
  "feature_id": "FEAT-real-time-monitoring",
  "feature_name": "Real-time Monitoring",
  "solution_id": "SOL-ai-threat-detection",  # Parent
  "product_id": "PROD-zero-trust-platform",  # Grandparent
  "domain_id": "DOM-cloud-security"          # Root
}
```

## Benefits of Generic Structure

### For File Organization
- **Predictable Layouts**: Same patterns across all entity types
- **Scalable Hierarchies**: Support for deep nesting and complex relationships
- **Flexible Grouping**: Multiple organizational approaches (segment-based, problem-based)
- **Cross-Cutting Concerns**: Integration points and research artifacts

### For Context Detection
- **Automatic Resolution**: Context detected from directory structure
- **Hierarchical Awareness**: Understanding of parent-child relationships
- **Multiple Ancestors**: Access to full entity hierarchy
- **Flexible Navigation**: Works with any entity type configuration

### For CLI Operations
- **Consistent Patterns**: Same commands work for all entity types
- **Context-Aware Defaults**: Auto-detection of IDs and relationships
- **Extensible Commands**: New entity types get full CLI support automatically
- **Hierarchical Operations**: Commands understand entity relationships

This generic approach maintains all the organizational benefits of the current system while providing unlimited extensibility for new entity types and relationship patterns.