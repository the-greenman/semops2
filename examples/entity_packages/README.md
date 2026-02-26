# Entity Packages

Entity packages are modular, self-contained units that define entity types, their expert profiles, and interactive refinement journeys.

## Package Structure

Each package contains:

```
entity_package_name/
├── entity_definition.yaml      # Entity type configuration
├── experts.yaml                # Package-local expert profiles (default resolution source)
├── journey_definition.yaml     # Interactive refinement journey
├── migration_rules.yaml        # Template evolution rules
└── templates/
    └── v1.0.0/                 # Versioned templates
        ├── create.md.j2        # Creation template
        └── analyze.md.j2       # Analysis template
```

## Available Packages

### [domain/](domain/)
**Purpose**: Define operational domains with clear boundaries and stakeholders

**Journey Stages**:
1. Draft creation (human)
2. Scope clarification (AI-assisted)
3. Review scope (human)
4. Resource identification (AI-assisted)
5. Review resources (human)
6. Stakeholder mapping (AI-assisted)
7. Review stakeholders (human)
8. Finalize domain (system)

**Use Case**: Create governance, operations, engineering, or other organizational domains

### [decision/](decision/)
**Purpose**: Extract and refine decisions from meeting or conversation content

**Journey Stages**:
1. Load source content (system)
2. Identify decisions (AI-assisted)
3. Review identified decisions (human)
4. Clarify each decision (AI-assisted, iterative)
5. Review clarified statement (human)
6. Explore options (AI-assisted)
7. Review options (human)
8. Identify stakeholders (AI-assisted)
9. Review stakeholders (human)
10. Assess readiness (human)
11. Create decision entity (system)

**Use Case**: Turn meeting discussions into formal decision records

### [policy/](policy/)
**Purpose**: Develop organizational policies with AI assistance

**Scope**: Optional collaborative-org extension package (not a required `semops.core` default)

**Journey Stages**:
1. Draft policy (human)
2. AI enrichment (AI-assisted)
3. Review policy (human)
4. Finalize policy (system)

**Use Case**: Create access control, security, operational policies

### [constitution/](constitution/)
**Purpose**: Create foundational governing documents

**Scope**: Optional collaborative-org extension package (not a required `semops.core` default)

**Journey Stages**:
1. Draft constitution (human)
2. Stakeholder consultation (AI-assisted)
3. Review draft (human)
4. Voting process (human)
5. Finalize constitution (system)

**Use Case**: Establish organizational charter, foundational principles

## Using Entity Packages

### Installation

```bash
# Copy packages to your workspace
cp -r /path/to/semops2/examples/entity_packages .semops/entity_packages/

# Packages are referenced in config
# collaborative_org_config_v2.yaml:
#   entity_packages_path: "../entity_packages"
#   entity_packages:
#     - package: "domain"
#       journey_enabled: true
```

### Starting a Journey

```bash
# General syntax
semops journey start <journey-id> [options]

# Examples
semops journey start domain-definition --name "Engineering"
semops journey start decision-refinement MTG-weekly-sync
semops journey start policy-development --name "Access Control"
semops journey start constitution-ratification --name "Charter"
```

### Journey Commands

```bash
# Check journey status
semops journey status <thread-id>

# Resume paused journey
semops journey resume <thread-id>

# List available journeys
semops journey list

# Describe journey stages
semops journey describe domain-definition
```

## Journey Stage Types

### human.create
User creates initial draft with required/optional fields

**Example**:
```yaml
- name: "draft_creation"
  type: "human.create"
  required_fields: ["domain_name"]
  optional_fields: ["description", "purpose"]
```

### ai.assist
AI analyzes context and proposes enhancements

**Example**:
```yaml
- name: "scope_clarification"
  type: "ai.assist"
  agent:
    role: "domain_architect"
    persona: "You help define domain boundaries..."
    expertise: ["scope_definition", "boundary_setting"]
    model: "claude-3-5-sonnet"
  task: |
    Analyze this domain draft and propose:
    1. Clear scope definition
    2. Related domains
    3. Key stakeholders
  knowledge_context:
    query: "existing domains, organizational structure"
    workflow: "authority_weighted"
    entity_types: ["domain", "role", "constitution"]
```

### human.review
User reviews AI proposal and takes action

**Example**:
```yaml
- name: "review_scope"
  type: "human.review"
  show:
    - label: "AI Proposal"
      content: "{outputs.scope_proposal}"
  actions:
    - action: "approve"
      label: "Accept AI proposal"
      next_stage: "resource_identification"
    - action: "edit"
      label: "Edit and refine"
      allow_edit: true
      next_stage: "scope_clarification"  # Loop back
    - action: "reject"
      label: "Start over"
      next_stage: "draft_creation"
```

### system.commit
System finalizes and creates entities

**Example**:
```yaml
- name: "finalize_domain"
  type: "system.commit"
  actions:
    - action: "create_entity"
      entity_type: "domain"
      template_version: "1.0.0"
      fields:
        domain_name: "{outputs.approved_scope.domain_name}"
        purpose: "{outputs.approved_scope.purpose}"
        # ...
    - action: "add_relationships"
      relationships:
        - type: "part_of"
          from: "{outputs.selected_resources.entities}"
          to: "{entity_id}"
    - action: "save_journey_state"
      journey_id: "{journey_id}"
      entity_id: "{entity_id}"
```

## Iterative Refinement

Journeys support loops for refinement:

```yaml
- name: "review_scope"
  type: "human.review"
  actions:
    - action: "approve"
      next_stage: "resource_identification"  # Continue forward
    - action: "edit"
      next_stage: "scope_clarification"  # Loop back for refinement
```

**Flow**:
1. AI proposes scope
2. Human reviews
3. If edit: loop back to AI with feedback
4. AI refines based on feedback
5. Human reviews again
6. Repeat until approved

## Knowledge Context Integration

AI agents can query the knowledge repository:

```yaml
knowledge_context:
  query: "existing domains, organizational structure, governance"
  workflow: "authority_weighted"  # Use authority-weighted retrieval
  entity_types: ["domain", "role", "constitution", "policy"]
```

**Authority-weighted results**:
```
[AUTHORITATIVE 1.0] Constitution: "Domains must have clear accountability..."
[FORMAL 0.95] Policy: "Domain leads are responsible for..."
[DOCUMENTED 0.75] Meeting: "Discussion of domain structure..."
[EXPLORATORY 0.2] Notes: "Maybe we should consider..."
```

## Template Evolution

When templates change, entities are migrated:

```yaml
# migration_rules.yaml
migrations:
  "1.0.0 → 1.1.0":
    strategy: "llm_assisted_with_review"
    changes:
      added_fields:
        - field: "authority_level"
          infer_from: ["domain_name", "purpose", "scope_included"]
          prompt: "Determine authority level: HIGH, MEDIUM, or LOW"
```

**Migration workflow**:
```bash
# Check for outdated entities
semops migrate check

# Preview migration
semops migrate preview --entity-type domain

# Run migration
semops migrate run --entity-type domain --strategy llm_assisted_with_review

# Rollback if needed
semops migrate rollback --migration-id <id>
```

See [TEMPLATE_EVOLUTION_GUIDE.md](../TEMPLATE_EVOLUTION_GUIDE.md) for details.

## Creating Custom Packages

### 1. Create Package Directory

```bash
mkdir -p .semops/entity_packages/my_entity/{templates/v1.0.0,prompts}
```

### 2. Define Entity Type

```yaml
# entity_definition.yaml
entity_type:
  type_key: "my_entity"
  namespace: "org.myorg"
  id_prefix: "ME"
  name_field: "entity_name"
  template_version: "1.0.0"
  required_fields: ["entity_name", "purpose"]
  template_bundle:
    create: "create.md.j2"
```

### 3. Define Journey

```yaml
# journey_definition.yaml
entity_journey:
  journey_id: "my-entity-creation"
  entity_type: "org.myorg/my_entity"
  stages:
    - name: "draft_creation"
      type: "human.create"
    - name: "ai_enrich"
      type: "ai.assist"
      agent:
        role: "my_entity_specialist"
        persona: "..."
    - name: "review"
      type: "human.review"
    - name: "finalize"
      type: "system.commit"
```

### 4. Define Package Experts

```yaml
# experts.yaml
expert_types:
  my_entity_specialist:
    name: "My Entity Specialist"
    persona:
      role: "Specialist for my_entity refinement"
    expertise: ["context_mapping", "stakeholder_alignment"]
```

### 5. Create Templates

```jinja2
# templates/v1.0.0/create.md.j2
# {{entity_name}}

**Entity Type**: My Entity
**ID**: {{entity_id}}

## Purpose
{{purpose}}

## Metadata
- **Created**: {{created_date}}
- **Template Version**: {{template_version}}
```

### 6. Define Migration Rules

```yaml
# migration_rules.yaml
current_version: "1.0.0"
migrations: {}
strategies:
  llm_assisted:
    requires_approval: false
rollback:
  enabled: true
  retention_policy: "90_days"
```

### 7. Reference in Config

```yaml
# .semops/config.yaml
entity_packages:
  - package: "my_entity"
    namespace: "org.myorg"
    journey_enabled: true
```

## Package Distribution

### Current: Copy Directory
```bash
cp -r entity_packages/* .semops/entity_packages/
```

### Future: Package Registry
```bash
# Not yet implemented
semops package install domain@1.0.0
semops package install org/custom-entity
```

## Best Practices

### 1. Keep Journeys Focused
Each journey should have a clear purpose. Don't try to do too much in one journey.

### 2. Provide Clear Agent Personas
Well-defined personas help LLM generate better proposals:
```yaml
persona: |
  You are an organizational architect who helps define clear boundaries
  and purposes for operational domains. You understand how to avoid
  overlaps, identify interfaces between domains, and ensure each domain
  has a coherent scope.
```

### 3. Use Knowledge Context
Let AI agents query existing knowledge:
```yaml
knowledge_context:
  query: "relevant existing entities and patterns"
  workflow: "authority_weighted"
```

### 4. Enable Iterative Loops
Allow users to refine AI proposals:
```yaml
actions:
  - action: "edit"
    next_stage: "previous_stage"  # Loop back
```

### 5. Version Templates Carefully
Follow semantic versioning:
- MAJOR: Breaking changes
- MINOR: Added fields (non-breaking)
- PATCH: Bug fixes, typos

## Troubleshooting

### "Journey not found"
```bash
# Check package loaded
semops config show entity_packages

# Verify journey_definition.yaml and experts.yaml exist
ls .semops/entity_packages/domain/journey_definition.yaml
ls .semops/entity_packages/domain/experts.yaml
```

### "Template not found"
```bash
# Check template version matches
semops config show workspace.template_version

# Verify template exists
ls .semops/entity_packages/domain/templates/v1.0.0/
```

### "Agent fails to generate proposal"
```bash
# Check logs
tail -f .semops/logs/semops.log

# Verify LLM configuration
semops config show expert.default_model
```

## Further Reading

- [COLLABORATIVE_ORG_ARCHITECTURE.md](../../docs/COLLABORATIVE_ORG_ARCHITECTURE.md) - Full architecture
- [COLLABORATIVE_ORG_QUICKSTART.md](../COLLABORATIVE_ORG_QUICKSTART.md) - Getting started
- [TEMPLATE_EVOLUTION_GUIDE.md](../TEMPLATE_EVOLUTION_GUIDE.md) - Migration guide

## Contributing

Share your custom entity packages with the community:
1. Create package following structure above
2. Test thoroughly
3. Document use cases
4. Submit to package registry (future)
5. Share on Discord/GitHub

---

Entity packages make SemOps2 extensible and adaptable to your organization's specific needs. Start with the provided packages and create your own as patterns emerge.
