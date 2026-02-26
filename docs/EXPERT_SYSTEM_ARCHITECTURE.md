# Expert System Architecture - Multi-Agent Analysis Framework

## Overview

SemOps2's expert system provides a generic, configuration-driven approach to multi-agent analysis where different AI expert personas specialize in different types of semantic analysis. Experts are package-local by default so pluggable entity contributions carry entity definitions, journeys, and expert behavior together.

Scope note: this document defines the SemOps2 target architecture. Any SemOps v1 references below are historical rationale only and are not part of the SemOps2 runtime scope.

## Legacy Constraints (SemOps v1 Historical Context)

### Hardcoded Expert Mapping
```python
# Historical SemOps v1 mapping example
expert_mapping = {
    "domain": "strategic",
    "problem": "product",
    "persona": "ux"
}
```

### Fixed Expert Types
- Only 3 expert types: strategic, product, UX
- Entity-to-expert mapping is inflexible
- Adding new experts requires code changes
- No support for multiple experts per entity type
- No cross-entity expert specialization

### Template-Based Expert Headers
- Expert headers hardcoded in prompt files
- No dynamic expert persona generation
- Limited to analysis-only expertise
- No expert customization for different domains/contexts

## SemOps2 Generic Expert System

### Expert Ownership Model

1. **Package-local experts are the default**
   - Each entity package may define `experts.yaml` alongside `entity_definition.yaml` and `journey_definition.yaml`.
   - Journey `ai.assist` stages resolve `agent.role` from package-local experts first.

2. **Core experts are a small shared baseline**
   - `.semops/config/expert_types.yaml` provides optional cross-package shared experts.
   - Core experts are fallback defaults, not the primary extension surface.

3. **Deterministic resolution order**
   - `entity_packages/<entity>/experts.yaml`
   - `.semops/config/expert_types.yaml`
   - Built-in SemOps core defaults

### Experts vs External Actors (Unified Runtime Contract)

- **Actors are control-plane principals**: humans/software/services use `ACT-*` identities, policy-scoped permissions, and audit attribution.
- **Experts are analysis personas**: `expert_type` keys resolve to package-local or core expert definitions and do not carry authority on their own.
- **Invocation contract is explicit**: external actors call expert analysis with `actor_id + expert_type + entity_id/workflow`.
- **Journey role aliases are resolved first**: `agent.role` in journey stages is translated to a concrete `expert_type` using package-first precedence before execution.
- **Mutation invariants still apply**: expert outputs can propose content, but any write must go through `EntityService` with `created_by_actor_id` / `updated_by_actor_id`.

### Expert Configuration Schema

Example expert and entity names below are illustrative configuration patterns. SemOps2 runtime defaults remain defined by the active `entity_types` configuration (for example, `semops.core/domain`, `semops.core/meeting`, `semops.core/decision`).

```yaml
# entity_packages/domain/experts.yaml
expert_types:
  # Strategic Business Expert
  strategic_analyst:
    name: "Strategic Business Analyst"
    description: "Market dynamics and business strategy expert"
    icon: "📊"

    # Expertise Areas
    expertise:
      - market_dynamics
      - competitive_analysis
      - business_strategy
      - risk_assessment
      - technology_trends

    # Analysis Approach
    analysis_approach:
      methodology: "source_driven_strategic"
      focus_areas:
        - business_impact
        - market_forces
        - strategic_implications
      evidence_requirements: "high"
      confidence_reporting: true

    # Persona Definition
    persona:
      role: "Seasoned strategic business analyst"
      specialization: "Technology market analysis and enterprise infrastructure decisions"
      background: "15+ years experience in enterprise technology strategy"

    # Prompt Components
    templates:
      header: "strategic_analyst_header.md.j2"
      analysis_guide: "strategic_analysis_methodology.md.j2"
      polarity_framework: "strategic_polarities.md.j2"

    # Entity Type Compatibility
    applicable_entities: ["domain", "market_segment", "strategy"]
    primary_entity: "domain"

  # Product Strategy Expert
  product_strategist:
    name: "Product Strategy Expert"
    description: "Customer research and problem validation specialist"
    icon: "🎯"

    expertise:
      - customer_research
      - problem_definition
      - market_validation
      - competitive_analysis
      - solution_architecture

    analysis_approach:
      methodology: "customer_centric_validation"
      focus_areas:
        - customer_problems
        - solution_fit
        - market_validation
      evidence_requirements: "medium"
      prioritization_framework: "impact_urgency_feasibility"

    persona:
      role: "Senior product strategist"
      specialization: "Enterprise technology solutions and customer problem analysis"
      background: "Product management in B2B enterprise software"

    templates:
      header: "product_strategist_header.md.j2"
      analysis_guide: "product_analysis_methodology.md.j2"
      validation_framework: "problem_validation.md.j2"

    applicable_entities: ["problem", "product", "solution"]
    primary_entity: "problem"

  # UX Research Expert
  ux_researcher:
    name: "UX Research Expert"
    description: "User behavior and organizational dynamics specialist"
    icon: "👤"

    expertise:
      - user_research
      - persona_development
      - behavioral_analysis
      - organizational_dynamics
      - decision_influence_mapping

    analysis_approach:
      methodology: "human_centered_behavioral"
      focus_areas:
        - user_behaviors
        - organizational_context
        - decision_influence
      evidence_requirements: "medium"
      persona_framework: "role_based_behavioral"

    persona:
      role: "Senior UX researcher"
      specialization: "Enterprise software adoption and organizational behavior"
      background: "User research in complex organizational environments"

    templates:
      header: "ux_researcher_header.md.j2"
      analysis_guide: "ux_analysis_methodology.md.j2"
      persona_framework: "behavioral_persona_development.md.j2"

    applicable_entities: ["persona", "feature"]
    primary_entity: "persona"

  # Technical Architecture Expert (NEW)
  technical_architect:
    name: "Technical Architecture Expert"
    description: "System design and technical solution specialist"
    icon: "🏗️"

    expertise:
      - system_architecture
      - technical_feasibility
      - integration_patterns
      - scalability_analysis
      - technology_selection

    analysis_approach:
      methodology: "architecture_driven_design"
      focus_areas:
        - system_design
        - technical_constraints
        - integration_points
      evidence_requirements: "high"
      architecture_framework: "layered_systems_thinking"

    applicable_entities: ["solution", "integration", "feature"]
    primary_entity: "solution"

  # Market Research Expert (NEW)
  market_researcher:
    name: "Market Research Expert"
    description: "Competitive intelligence and market analysis specialist"
    icon: "🔍"

    expertise:
      - competitive_intelligence
      - market_sizing
      - trend_analysis
      - customer_segmentation
      - adoption_patterns

    applicable_entities: ["market_segment", "research", "domain"]
    primary_entity: "research"
```

### Package-Level Expert Assignment Pattern

```yaml
# entity_packages/domain/journey_definition.yaml
entity_journey:
  journey_id: "domain-definition"
  entity_type: "semops.core/domain"
  stages:
    - name: "scope_clarification"
      type: "ai.assist"
      agent:
        role: "domain_architect"  # Resolved from entity_packages/domain/experts.yaml
    - name: "stakeholder_mapping"
      type: "ai.assist"
      agent:
        role: "stakeholder_analyst"

# Optional shared workflow library in .semops/config/workflows.yaml
workflows:
  domain-analysis:
    applicable_entity_types: ["semops.core/domain"]
    steps:
      - name: "strategic_assessment"
        expert: "domain_architect"
      - name: "market_validation"
        expert: "market_researcher"
```

## Generic Expert System Components

### ExpertService Architecture

```python
class ExpertService:
    """Generic expert system for multi-agent analysis."""

    def __init__(self, config_manager: ConfigManager):
        self.package_experts = config_manager.get_package_expert_types()
        self.core_experts = config_manager.get_core_expert_types()
        self.template_engine = TemplateEngine()

    def resolve_expert(self, entity_type: str, role: str) -> Optional[ExpertType]:
        """Resolve expert using package-first, core-second precedence."""

    def get_expert_analysis(self, actor_id: str, entity_type: str, entity_data: Dict,
                          expert_type: Optional[str] = None) -> Dict:
        """Generate expert analysis for entity."""

    def run_multi_expert_workflow(self, workflow_name: str,
                                entity_data: Dict) -> Dict:
        """Execute multi-expert analysis workflow."""

    def generate_expert_prompt(self, expert_type: str, entity_type: str,
                             context: Dict) -> str:
        """Generate expert-specific prompt from templates."""
```

### Dynamic Expert Prompt Generation

```python
class ExpertPromptGenerator:
    def generate_expert_header(self, expert_config: ExpertType,
                             entity_type: str, context: Dict) -> str:
        """Generate expert persona header dynamically."""
        template = self.load_template(expert_config.templates.header)

        expert_context = {
            'expert_name': expert_config.name,
            'expert_role': expert_config.persona.role,
            'specialization': expert_config.persona.specialization,
            'expertise_areas': expert_config.expertise,
            'methodology': expert_config.analysis_approach.methodology,
            'focus_areas': expert_config.analysis_approach.focus_areas,
            'entity_type': entity_type,
            'entity_context': context
        }

        return template.render(expert_context)
```

### Multi-Expert Analysis Workflows

```python
class MultiExpertWorkflow:
    def execute_domain_analysis(self, actor_id: str, domain_data: Dict) -> Dict:
        """Multi-phase domain analysis with expert specialization."""

        # Phase 1: Strategic Assessment
        strategic_analysis = self.expert_service.get_expert_analysis(
            actor_id=actor_id,
            entity_type="domain",
            entity_data=domain_data,
            expert_type="strategic_analyst"
        )

        # Phase 2: Market Research
        market_analysis = self.expert_service.get_expert_analysis(
            actor_id=actor_id,
            entity_type="domain",
            entity_data={**domain_data, "strategic_context": strategic_analysis},
            expert_type="market_researcher"
        )

        # Phase 3: Synthesis
        synthesis = self.synthesize_expert_analyses([
            strategic_analysis,
            market_analysis
        ])

        return {
            "strategic_assessment": strategic_analysis,
            "market_validation": market_analysis,
            "comprehensive_analysis": synthesis
        }
```

## Expert System Benefits

### For Analysis Quality
- **Specialized Expertise**: Each expert brings domain-specific knowledge and methodology
- **Multi-Perspective Analysis**: Complex entities analyzed from multiple expert viewpoints
- **Consistent Methodology**: Each expert follows defined analysis approaches
- **Evidence Integration**: Experts synthesize different types of evidence appropriately

### For System Extensibility
- **Configurable Experts**: Add new expert types through configuration only
- **Flexible Mappings**: Entity-expert assignments easily modified
- **Multi-Expert Workflows**: Complex analysis pipelines through configuration
- **Template-Driven Prompts**: Expert personas generated from templates

### For Entity Types
- **Expert Assignment**: New entity types automatically get appropriate expert analysis
- **Specialized Analysis**: Each entity type analyzed by most relevant experts
- **Cross-Entity Expertise**: Experts can work across multiple entity types
- **Contextual Analysis**: Expert selection based on entity context and relationships

## Expert Template Framework

### Expert Header Template
```jinja2
# {{expert_name}}

You are a {{expert_role}} specializing in {{specialization}}. Your expertise includes:

{% for area in expertise_areas %}
- **{{area|title}}**: [Context-specific description based on entity type]
{% endfor %}

## Your Analysis Approach for {{entity_type|title}} Analysis

1. **{{methodology|title}}**: [Methodology description]
{% for focus in focus_areas %}
2. **{{focus|title}}**: [Focus area description]
{% endfor %}

## Key Responsibilities for {{entity_type|title}}

{% if entity_type == "domain" %}
- Analyze market conditions and technology trends
- Identify strategic opportunities and threats
- Define domain boundaries based on business value
{% elif entity_type == "problem" %}
- Analyze customer problems and business impact
- Validate problem significance with market evidence
- Define problem scope and solution requirements
{% endif %}

[Context-specific responsibilities based on entity type and expert specialization]
```

## Implementation Strategy for Expert System

### Phase 1: Expert Configuration
- Define expert types in YAML configuration
- Define package-local expert catalogs and optional shared core fallback experts
- Build expert template framework

### Phase 2: Expert Service Implementation
- Generic ExpertService for expert management
- Dynamic expert prompt generation
- Multi-expert workflow execution

### Phase 3: Template Standardization
- Standardize expert headers as templates
- Create expert-specific analysis methodologies
- Build expert persona generation system

### Phase 4: Advanced Workflows
- Multi-expert analysis pipelines
- Expert synthesis and integration
- Context-aware expert selection

This generic expert system eliminates the rigid expert-entity mappings while providing far more flexibility for specialized analysis across any entity type configuration.
