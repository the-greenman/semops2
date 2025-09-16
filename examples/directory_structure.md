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
domain/cloud_security/
├── domain_definition.md
├── problems/
│   └── compliance_challenges.md
├── personas/
│   └── security_manager.md
├── products/
│   └── zero_trust_platform.md
├── solutions/                          # NEW: Solution approaches
│   ├── ai_threat_detection.md
│   └── features/                       # NEW: Features within solutions
│       ├── real_time_monitoring.md
│       ├── threat_correlation.md
│       └── automated_response.md
├── research/                           # NEW: Research artifacts
│   ├── market_analysis_2024.md
│   ├── user_interview_summary.md
│   └── competitive_landscape.md
├── strategies/                         # NEW: Strategic initiatives
│   ├── go_to_market_strategy.md
│   └── initiatives/                    # NEW: Specific initiatives
│       ├── partnership_program.md
│       ├── content_marketing.md
│       └── analyst_engagement.md
└── integrations/                       # NEW: Integration points
    ├── existing_siem_integration.md
    └── cloud_provider_connectors.md
```

## Alternative Hierarchy: Market Segment Focus

```
domain/enterprise_software/
├── domain_definition.md
├── segments/                           # NEW: Market segments
│   ├── small_business.md              # market_segment.filename_pattern
│   ├── mid_market.md
│   └── enterprise.md
├── problems/
│   ├── digital_transformation.md      # Problems span segments
│   └── legacy_modernization.md
└── personas/
    ├── small_business/                 # Personas organized by segment
    │   ├── small_biz_owner.md
    │   └── it_generalist.md
    ├── mid_market/
    │   ├── it_director.md
    │   └── business_analyst.md
    └── enterprise/
        ├── enterprise_architect.md
        └── procurement_manager.md
```

## Cross-Cutting Entity Types

```
domain/cloud_security/
├── domain_definition.md
├── [standard hierarchy...]
├── integrations/                       # Cross-cutting integrations
│   ├── siem_connector.md              # Links multiple products/solutions
│   ├── cloud_api_gateway.md           # Integration specifications
│   └── third_party_feeds.md
├── research/                           # Domain-level research
│   ├── threat_landscape_2024.md       # Market research
│   ├── customer_pain_points.md        # User research
│   └── technology_trends.md           # Technical research
└── strategies/                        # Strategic planning
    ├── market_penetration.md          # Business strategy
    ├── product_roadmap.md             # Product strategy
    └── partnership_strategy.md        # Go-to-market strategy
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
semops problem get PROB-ComplianceChallenges
semops persona create --name "Security Manager"

# New entity types (automatically available)
semops solution list                    # Lists solutions in current context
semops feature create --name "Real-time Monitoring"
semops research get RES-MarketAnalysis2024

# Market segments
semops market-segment list              # Auto-generated command
semops market-segment create --name "Small Business"

# Cross-cutting entities
semops integration list                 # Lists all integrations
semops strategy analyze STRAT-GoToMarket
```

## Template Variable Context

Each entity type automatically receives appropriate context variables:

### Solution Template Variables
```yaml
# Available in solution.md.j2 template:
{
  "entity_type": "solution",
  "solution_id": "SOL-AiThreatDetection",
  "solution_name": "AI Threat Detection",
  "solution_slug": "ai_threat_detection",
  "product_id": "PROD-ZeroTrustPlatform",  # Parent context
  "domain_id": "DOM-CloudSecurity",        # Ancestor context
  "template_id": "TEMPLATE-Solution",
  "template_version": "1.0.0"
}
```

### Feature Template Variables
```yaml
# Available in feature.md.j2 template:
{
  "entity_type": "feature",
  "feature_id": "FEAT-RealTimeMonitoring",
  "feature_name": "Real-time Monitoring",
  "solution_id": "SOL-AiThreatDetection",  # Parent
  "product_id": "PROD-ZeroTrustPlatform",  # Grandparent
  "domain_id": "DOM-CloudSecurity"         # Root
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