# Entity Configuration System

## Overview

The entity configuration system is the heart of SemOps2's generic architecture. Instead of hardcoded entity types, all entities are defined through YAML configuration files that specify their structure, relationships, templates, and behavior.

## Configuration Schema

### Entity Type Definition

```yaml
entity_types:
  {entity_name}:
    # Identity Configuration
    id_prefix: "PREFIX"              # ID prefix (e.g., "DOM", "PROB")
    name_field: "{entity_name}_name" # Field containing entity name
    slug_field: "{entity_name}_slug" # Field containing URL-safe slug

    # Template Configuration
    template: "{entity_name}.md.j2"  # Jinja2 template file
    directory_name: "{plural_name}"  # Directory name for entity files
    filename_pattern: "{entity_type}.md" # Type-based filename for context detection

    # Structure Configuration
    nesting_strategy: "root"        # "root" collections only
    context_level: 1                 # Optional UI ordering, not filesystem hierarchy

    # Validation Configuration
    required_fields: ["field1"]     # Required fields for entity creation
    unique_fields: ["field1"]       # Fields that must be unique
    validation_schema: "schema.json" # JSON schema file (optional)

    # CLI Configuration
    list_command: true               # Generate 'list' command
    get_command: true                # Generate 'get' command
    create_command: true             # Generate 'create' command
    update_command: true             # Generate 'update' command
    delete_command: true             # Generate 'delete' command
    analyze_command: true            # Generate 'analyze' command

    # Display Configuration
    display_name: "{Entity Name}"    # Human-readable name for UI
    description: "Entity description" # Help text for CLI
    icon: "📋"                      # Icon for display (optional)
```

## Standard Entity Types

### Domain (Root Level)
```yaml
domain:
  id_prefix: "DOM"
  name_field: "domain_name"
  slug_field: "domain_slug"
  template: "domain.md.j2"
  directory_name: "domain"
  filename_pattern: "{entity_type}.md"    # → domain.md for context detection
  nesting_strategy: "root"                # Root entity type
  scoped_to_parent: false
  context_level: 1
  required_fields: ["domain_name", "brief_description"]
  unique_fields: ["domain_name", "domain_slug"]
  display_name: "Domain"
  description: "Strategic business areas and market segments"
  icon: "🏢"
```

### Problem (Level 2)
```yaml
problem:
  id_prefix: "PROB"
  name_field: "problem_name"
  slug_field: "problem_slug"
  template: "problem.md.j2"
  directory_name: "problems"
  filename_pattern: "{entity_type}.md"    # → problem.md for context detection
  nesting_strategy: "root"                # Flat collections
  scoped_to_parent: false                  # Link to domains via relationships
  context_level: 2
  required_fields: ["problem_name", "domain_id"]
  unique_fields: ["problem_name"]
  display_name: "Problem"
  description: "Market challenges and opportunities"
  icon: "🎯"
```

### Persona (Level 3)
```yaml
persona:
  id_prefix: "PERS"
  name_field: "persona_name"
  slug_field: "persona_slug"
  template: "persona.md.j2"
  directory_name: "personas"
  filename_pattern: "{entity_type}.md"    # → persona.md for context detection
  nesting_strategy: "root"                # Flat collections
  scoped_to_parent: false                  # Link to problems via relationships
  context_level: 3
  required_fields: ["persona_name", "problem_id"]
  unique_fields: ["persona_name"]
  display_name: "Persona"
  description: "User archetypes and target audiences"
  icon: "👤"
```

### Product (Level 4)
```yaml
product:
  id_prefix: "PROD"
  name_field: "product_name"
  slug_field: "product_slug"
  template: "product.md.j2"
  directory_name: "products"
  filename_pattern: "{entity_type}.md"    # → product.md for context detection
  nesting_strategy: "root"                # Flat collections
  scoped_to_parent: false                  # Link to personas via relationships
  context_level: 4
  required_fields: ["product_name", "persona_id"]
  unique_fields: ["product_name"]
  display_name: "Product"
  description: "Solution definitions and offerings"
  icon: "📦"
```

## Extended Entity Types

### Solution (Level 2B)
```yaml
solution:
  id_prefix: "SOL"
  name_field: "solution_name"
  slug_field: "solution_slug"
  template: "solution.md.j2"
  directory_name: "solutions"
  filename_pattern: "{entity_type}.md"    # → solution.md for context detection
  nesting_strategy: "root"                # Flat collections
  scoped_to_parent: false                  # Link to domains via relationships
  context_level: 2
  required_fields: ["solution_name", "domain_id"]
  display_name: "Solution"
  description: "Specific implementation approaches"
  icon: "💡"
```

### Feature (Level 3)
```yaml
feature:
  id_prefix: "FEAT"
  name_field: "feature_name"
  slug_field: "feature_slug"
  template: "feature.md.j2"
  directory_name: "features"
  filename_pattern: "{entity_type}.md"    # → feature.md for context detection
  nesting_strategy: "root"                # Flat collections
  scoped_to_parent: false                  # Link to solutions via relationships
  context_level: 3
  required_fields: ["feature_name", "solution_id"]
  display_name: "Feature"
  description: "Specific capabilities and functions"
  icon: "⚡"
```

## Flexible Hierarchies

The system supports alternative hierarchy patterns:

### Multiple Parents
```yaml
product:
  nesting_strategy: "root"
```

### Cross-References
```yaml
integration:
  id_prefix: "INT"
  nesting_strategy: "root"
  references: ["product", "solution"]  # References other entities
```

### Categorization
```yaml
market_segment:
  id_prefix: "SEG"
  nesting_strategy: "root"

relationship_types:
  in_segment:
    namespace: "semops.core"
    from_types: ["semops.core/persona"]
    to_types: ["semops.core/market_segment"]
    share_sources: false
```

## Directory Structure Mapping

Configuration determines file system layout using flat root collections:

```
my-workspace/
├── domain/
│   └── cloud-security/
│       ├── domain.md
│       └── working/
├── problems/                            # Optional entity type
│   └── compliance-challenges/
│       ├── problem.md
│       └── working/
├── personas/                            # Optional entity type
│   └── security-manager/
│       ├── persona.md
│       └── working/
├── solutions/                           # Optional entity type
│   └── zero-trust-platform/
│       ├── solution.md
│       └── working/
└── features/                            # Optional entity type
    └── threat-detection/
        ├── feature.md
        └── working/
```

## Configuration Validation

### Schema Validation
```yaml
# Validate entity type configuration against schema
validation:
  entity_type_schema: "entity_type.schema.json"
  template_validation: true
  hierarchy_validation: false
  uniqueness_validation: true
```

### Runtime Validation
```python
class EntityTypeValidator:
    def validate_hierarchy(self) -> List[str]:
        """Ensure hierarchy is acyclic and well-formed."""

    def validate_templates(self) -> List[str]:
        """Ensure all referenced templates exist."""

    def validate_uniqueness(self) -> List[str]:
        """Ensure unique field constraints can be enforced."""
```

## Template Integration

### Template Variables
Configuration provides template context:
```yaml
# Automatically available in templates:
{
  "entity_type": "domain",
  "id_prefix": "DOM",
  "parent_id": null,
  "template_id": "TEMPLATE-Domain",
  "template_version": "2.5.3"
}
```

### Template Validation
```yaml
template_validation:
  required_variables: ["entity_name", "brief_description"]
  frontmatter_schema: "frontmatter.schema.json"
  content_rules: "content_rules.yaml"
```

## CLI Integration

### Auto-Generated Commands
Configuration drives CLI command generation:
```python
# From configuration, generates:
@app.command()
def list_solutions():
    """List solutions for current product"""

@app.command()
def get_solution(solution_id: Optional[str] = None):
    """Get solution details"""
```

### Context Awareness
```yaml
context_detection:
  # Detection based on type-based filenames
  filename_indicators: ["{entity_type}.md"]  # domain.md, problem.md, persona.md
  nesting_strategy: "root"                   # Flat collections
  parent_resolution: "explicit"              # Relationships, flags, or frontmatter
  validation_rules: ["unique_constraints"]
```

## Benefits

### For Developers
- **No Code Changes** - New entity types require only configuration
- **Consistent Behavior** - Same patterns across all entity types
- **Validation Built-in** - Schema validation and constraint enforcement
- **Template Integration** - Seamless template variable injection

### For Users
- **Predictable CLI** - Same command patterns for all entities
- **Context Awareness** - Auto-detection works consistently
- **Flexible Hierarchies** - Support for complex entity relationships
- **Extensible** - Easy to add custom entity types

### For System Evolution
- **Configuration-Driven** - Changes through config files, not code
- **Backward Compatible** - Existing templates and data structures preserved
- **Rapid Prototyping** - Quick experimentation with new entity structures
- **Maintainable** - Centralized configuration instead of scattered code

## Behavior-Driven Development (BDD) Scenarios

The following Gherkin scenarios capture SemOps2 MVP behavior. They are designed to map to:
- `src/core/config_manager.py`
- `src/core/entity_service.py`
- `src/core/context_detector.py`
- `src/cli/dynamic_commands.py`
- `src/core/knowledge_service.py` (for source resolution)

### Feature: Configuration Loading and Validation

```gherkin
Feature: Load and validate entity type configuration
  As a developer
  I want configuration to be validated with clear errors
  So that incorrect configs are caught early with actionable hints

  Background:
    Given a workspace with "config/entity_types.yaml"

  Scenario: Load valid configuration
    Given the file "config/entity_types.yaml" contains a valid domain/problem/persona/product definition
    When I load configuration with ConfigManager
    Then the entity types are available in memory
    And JSON Schema can be generated for the configuration

  Scenario: Report invalid field with hint
    Given the file "config/entity_types.yaml" contains an unknown field "dir_name" in the domain type
    When I load configuration with ConfigManager
    Then an error is raised indicating "dir_name" is not allowed
    And the error suggests "directory_name" as a likely fix
```

### Feature: Dynamic CLI Generation

```gherkin
Feature: CLI commands are generated from configuration
  As a user
  I want consistent CLI commands for any configured entity type
  So that I can list, get, and create entities without code changes

  Background:
    Given a valid configuration with domain and problem types and a cli stanza

  Scenario: List domains
    When I run "semops domain list --format json"
    Then I see an array of domain metadata

  Scenario: Create problem with context-resolved parent
    Given my current directory is within a domain folder
    When I run "semops problem create --problem-name 'Cost Shock'"
    Then a new problem markdown file is created under the flat problems collection
    And the problem frontmatter contains the resolved domain_id
```

### Feature: Flexible Output Formatting

```gherkin
Feature: CLI commands support multiple output formats
  As a user or agent
  I want to specify the output format (e.g., json, yaml, table)
  So that I can consume the output programmatically or read it easily

  Scenario: Requesting JSON output for a list command
    Given a valid configuration with a "domain" entity type
    And several domains exist
    When I run "semops domain list --format json"
    Then the output is a valid JSON array of domain objects

  Scenario: Requesting YAML output for a get command
    Given a domain "Cloud Security" with ID "DOM-cloud-security" exists
    When I run "semops domain get --id DOM-cloud-security --format yaml"
    Then the output is a valid YAML object representing the domain
```

### Feature: Entity Creation and Deterministic IDs

```gherkin
Feature: Create entities with deterministic IDs and slugs
  As a user
  I want IDs and slugs to be deterministic
  So that links and paths remain stable

  Scenario Outline: Create entity produces stable ID, slug, and structure
    Given a clean workspace
    And configuration defines <entity_type> with id_prefix, nesting_strategy, and kebab-case slugs
    When I create a <entity_type> named "My Example Entity"
    Then the generated ID is "<id_prefix>-my-example-entity" (kebab-case)
    And the directory structure follows nesting_strategy
    And the filename is always "<entity_type>.md" for context detection

    Examples:
      | entity_type | id_prefix | structure |
      | domain      | DOM       | domain/my-example-entity/domain.md |
      | problem     | PROB      | problems/my-example-entity/problem.md |
      | persona     | PERS      | personas/my-example-entity/persona.md |
```

### Feature: Entity Lifecycle Management (Update and Delete)

```gherkin
Feature: CLI commands support updating and deleting entities
  As a user or agent
  I want to be able to update and delete entities programmatically
  So that I can manage the full lifecycle of an entity

  Scenario: Update an existing entity's field
    Given a problem "Cost Shock" with ID "PROB-cost-shock" exists
    When I run "semops problem update --id PROB-cost-shock --description 'An updated description'"
    Then the problem's markdown file frontmatter is updated with the new description

  Scenario: Delete an entity with confirmation
    Given a problem with ID "PROB-to-be-deleted" exists
    When I run "semops problem delete --id PROB-to-be-deleted"
    Then the CLI prompts for confirmation before deleting

  Scenario: Force delete an entity without a prompt
    Given a problem with ID "PROB-to-be-deleted" exists
    When I run "semops problem delete --id PROB-to-be-deleted --force"
    Then the entity file and its directory are removed
```

### Feature: Context Detection

```gherkin
Feature: Detect context from current directory
  As a user
  I want the tool to detect my current entity context
  So that commands can infer IDs without explicit flags

  Background:
    Given a domain exists on disk

  Scenario: Detect context from type-based filenames
    Given my current directory is "/domain/cloud-security/"
    And the directory contains "domain.md" file
    When I ask for the current context
    Then the context includes entity_type "domain" with ID "DOM-cloud-security"
    And all relationships are scoped correctly

  Scenario: Context detection works in deep working directories
    Given my current directory is "/features/threat-detection/working/"
    And the directory contains "feature.md" file
    When I ask for the current context
    Then the context includes entity_type "feature" with ID "FEAT-threat-detection"
    And the hierarchy includes domain "DOM-cloud-security"
```

### Feature: Source Management and Inheritance

```gherkin
Feature: Attach and resolve sources across the hierarchy
  As an analyst
  I want to attach sources to entities and inherit them to descendants
  So that effective context is complete and deduplicated

  Background:
    Given a domain with a problem exists on disk
    And a source type "web_page" is defined in .semops/config/source_types.yaml

  Scenario: Attach source at domain and inherit to problem
    Given the domain frontmatter attaches source "SRC-Example-1234"
    When I list sources for the problem including inherited
    Then the result contains "SRC-Example-1234" with scope "inherited"

  Scenario: Exclude inherited source at problem level
    Given the domain frontmatter attaches source "SRC-Example-1234"
    And the problem frontmatter excludes source "SRC-Example-1234"
    When I list sources for the problem including inherited
    Then the result does not contain "SRC-Example-1234"
```

### Feature: Source Weighting and Authority

```gherkin
Feature: Source weighting influences retrieval ranking
  As an analyst
  I want search results to prioritize more authoritative sources
  So that I get more trustworthy answers

  Background:
    Given the source type "official_documentation" has a weight of 1.0
    And the source type "meeting_notes" has a weight of 0.5
    And a document of each type contains the text "agile methodology"

  Scenario: Authoritative sources are ranked higher
    When I search for "agile methodology"
    Then the result from the "official_documentation" source appears higher in the ranked list than the result from "meeting_notes"
```

### Feature: Roots and Cross-Domain Relationships

```gherkin
Feature: Multiple roots and cross-domain source sharing
  As an architect
  I want to configure roots and relationships
  So that sources can be shared across domains when permitted

  Background:
    Given settings.roots includes "domain"
    And a relationship type "depends_on" from domain to domain with share_sources true

  Scenario: Share sources across related domains
    Given domain A attaches source "SRC-Rel-01"
    And domain B depends_on domain A
    When I list sources for domain B with inherited and related included
    Then the result contains "SRC-Rel-01" with provenance including domain A
    And the relationship depth does not exceed max_depth
```

### Feature: Multi-Expert Workflows

```gherkin
Feature: Execute multi-expert analysis workflows
  As a strategist
  I want to run a configured, multi-step analysis workflow on an entity
  So that I can apply a consistent methodology involving multiple AI experts

  Background:
    Given a workflow "define_domain_strategy" is defined in ".semops/config/workflows.yaml"
    And it has two steps using experts "boundary_definer" and "tension_analyzer"
    And a domain with ID "DOM-cloud-governance" exists

  Scenario: Run a named workflow on a domain
    When I run "semops domain analyze --id DOM-cloud-governance --workflow define_domain_strategy"
    Then the "boundary_definer" expert is executed first
    And the "tension_analyzer" expert is executed second, using the output of the first
    And the domain's markdown file is updated with sections generated by both experts

  Scenario: List available workflows for the current context
    Given my current directory is within a "domain" entity
    And the "define_domain_strategy" workflow is applicable only to "domain" entities
    When I run "semops workflow list"
    Then the output lists "define_domain_strategy" as an applicable workflow

  Scenario: Attempt to run a workflow on an inapplicable entity type
    Given my current directory is within a "problem" entity
    And the "define_domain_strategy" workflow is applicable only to "domain" entities
    When I run "semops problem analyze --workflow define_domain_strategy"
    Then the command fails with an error stating the workflow is not applicable to the "problem" entity type

  Scenario: A workflow step receives input from the calling interface
    Given a workflow is configured with a step that requires an input named "human_feedback"
    When I execute the workflow via an interface (CLI, API, or MCP) and provide "Focus on cost reduction" for the "human_feedback" input
    Then the prompt sent to the LLM for that step contains the text "Focus on cost reduction"

  Scenario: A workflow step specifies a custom model
    Given the project is configured with a default model "claude-3-haiku"
    And a workflow step is configured to use the model "claude-3-opus"
    When I execute the workflow
    Then the LLMManager is requested to provide the "claude-3-opus" model for that step, overriding the default

  Scenario: A workflow step's output can be validated by another AI expert
    Given a workflow step is configured with a validation check that requires the output to contain the word "synergy"
    And the step's AI expert produces an output that does not contain the word "synergy"
    When I execute the workflow
    Then the validation check fails
    And the workflow is halted immediately

  Scenario: A workflow step fails validation
    Given a workflow step is configured with a validation check that requires the output to contain the word "synergy"
    And the step's AI expert produces an output that does not contain the word "synergy"
    When I execute the workflow
    Then the validation check fails
    And the workflow is halted immediately
```

### Feature: Template Versioning and Migration

```gherkin
Feature: Template versioning and migration
  As an administrator
  I want to manage template versions and migrate existing content
  So that the knowledge base remains consistent over time

  Background:
    Given the template "policy.md.j2" is at version "1.0.0"
    And a policy "POL-access-control" was created using version "1.0.0"

  Scenario: Migrating an entity to a new template version
    Given the template "policy.md.j2" is updated to version "1.1.0" with a new required field "review_owner"
    When I run "semops templates migrate --template policy.md.j2"
    Then the system identifies "POL-access-control" as out-of-date
    And it prompts me to provide a value for the new "review_owner" field
    And the policy's file is updated with the new structure and its template_version is set to "1.1.0"
```

### Feature: Audit Logging for State Changes

```gherkin
Feature: Audit logging for entity lifecycle events
  As an administrator
  I want a clear, immutable audit trail for all state-changing operations
  So that I can track who (or what) changed what, and when

  Scenario: Creating an entity generates an audit log
    Given the actor is "ACT-creation-bot"
    When the actor creates a new problem with name "API Latency Spike"
    Then a structured audit log is created with:
      | field            | value                       |
      | actor_id         | "ACT-creation-bot"          |
      | action           | "entity.create"             |
      | target_entity_id | "PROB-api-latency-spike"    |

  Scenario: Updating an entity generates an audit log
    Given a problem with ID "PROB-api-latency-spike" exists
    And the actor is "ACT-human-jane-doe"
    When the actor updates the problem's description
    Then a structured audit log is created with:
      | field            | value                       |
      | actor_id         | "ACT-human-jane-doe"        |
      | action           | "entity.update"             |
      | target_entity_id | "PROB-api-latency-spike"    |
      | details          | "description field updated" |
```

### Feature: Template Override System

```gherkin
Feature: Template override system
  As a developer
  I want to use a project-specific template instead of the default
  So that I can customize the appearance and behavior of entities

  Scenario: A project-specific template overrides the default template
    Given the `semops2` tool has a default `problem.md.j2` template
    And my current project has a custom `problem.md.j2` in its `.semops/templates/` directory
    When I run "semops problem create --name 'Test Problem'"
    Then the new problem is created using the project's custom template, not the default one
```

### Feature: Core Entity Lifecycle

```gherkin
Feature: Core entity lifecycle operations
  As a user
  I want to create, read, update, and delete entities
  So that I can manage the knowledge base

  Scenario: Creating a new entity
    When I run "semops domain create --name 'Cloud Governance'"
    Then a new directory "domain/cloud-governance/" is created
    And a file "domain/cloud-governance/domain.md" is created from the "domain.md.j2" template
    And the file contains the text "Cloud Governance"

  Scenario: Updating an existing entity
    Given a domain named "Cloud Governance" exists
    When I run "semops domain update --field description --value 'A new description'"
    Then the "domain.md" file for "Cloud Governance" is updated with the new description

  Scenario: Deleting an entity
    Given a domain named "Cloud Governance" exists
    When I run "semops domain delete --name 'Cloud Governance'"
    Then the directory "domain/cloud-governance/" is removed
```

### Feature: Agent-Friendly Tooling

```gherkin
Feature: Agent-friendly tooling and output formats
  As an AI agent
  I want to receive structured data from the CLI
  So that I can programmatically use the output

  Scenario: Requesting JSON output
    Given a domain named "Cloud Governance" exists
    When I run "semops domain get --name 'Cloud Governance' --format json"
    Then the output is a valid JSON object
    And the JSON object contains the key "domain_name" with the value "Cloud Governance"
```
