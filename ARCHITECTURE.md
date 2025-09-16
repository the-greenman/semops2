# SemOps2 - Generic Architecture Plan

## Overview

SemOps2 reimagines the semantic operations platform with a generic, configuration-driven architecture that eliminates the need for entity-specific service classes. Instead of hardcoded domains, problems, personas, and products, the system uses a flexible entity type configuration system that can handle unlimited entity types through templates and configuration.

## Current Problems with SemOps v1

1. **Entity-Specific Services** - Separate `DomainService`, `ProblemService`, `PersonaService` classes that duplicate logic
2. **Hardcoded Entity Types** - New entity types require new service classes, CLI commands, and templates
3. **Coupling** - Tight coupling between entity types and implementation code
4. **Duplication** - Same patterns repeated across different entity services
5. **Scalability** - Adding new entity types requires significant code changes

## SemOps2 Core Principles

### 1. Protobuf-First Interface Definition (Service Contracts)
All interfaces and data structures generated from authoritative protobuf schemas that establish **strict contracts between services**:
- **Service Contracts**: Protobuf schemas define the exact interface between EntityService, ExpertService, KnowledgeService, CLI, and MCP
- **Single source of truth** eliminates interface drift across all access methods
- **Type-safe clients** auto-generated for Python, TypeScript, Go from same schema
- **Consistent ID formats** enforced everywhere via protobuf validation rules
- **Breaking change detection** in CI/CD pipeline prevents contract violations
- **Cross-service compatibility** guaranteed through shared protobuf message types

### 2. Configuration-Driven Entity Types
All entity types defined in configuration files, not code:
- Entity metadata (prefixes, templates, directory structures)
- Hierarchical relationships between entity types
- Context detection rules
- Validation rules and constraints

### 3. Generic Service Layer (Contract-Based)
Single `EntityService` that handles all entity types through **protobuf-defined contracts**:
- **Service contracts** defined in `services.proto` specify exact method signatures
- **Request/response types** generated from protobuf ensure type safety across all interfaces
- **Unified CRUD operations** use same protobuf messages for CLI, API, and MCP access
- **Cross-service communication** guaranteed through shared message types

### 4. Template-First Design

All entity types use Jinja2 templates with:
- Standardized variable substitution
- YAML frontmatter for metadata
- Consistent document structure
- Extensible field definitions

### 5. Managed Template Lifecycle via TemplateService

To ensure long-term consistency as templates evolve, a dedicated `TemplateService` manages the entire template lifecycle.

1.  **Layered Loading**: The service loads templates using the override system (Project > Built-in), ensuring project-specific templates are used when present.
2.  **Version Manifest**: It reads a manifest (e.g., `.semops/templates.yaml`) that defines the canonical version for each template.
3.  **Status Checking**: It compares an entity's `template_version` from its frontmatter against the manifest to detect out-of-date files.
4.  **Migration Workflow**: It provides a `migrate` method that orchestrates the re-rendering of old entities with new templates, using AI to help map old fields to new ones where possible.

This is exposed to the user via the `semops templates status` and `semops templates migrate` commands.

### 6. Dynamic CLI Generation
CLI commands generated from entity type configurations:
- Automatic command registration
- Context-aware parameter resolution
- Consistent output formatting
- Extensible without code changes

## Configuration Management

To decouple the `semops2` tool from the knowledge bases it manages, configuration is loaded in a layered manner.

1.  **Project Root Discovery**: The tool searches upwards from the current directory for a marker file (e.g., `.semops-project`) to identify the root of the knowledge base project.
2.  **Layered Loading**: The `ConfigManager` loads configuration in the following order, with later layers overriding earlier ones:
    *   **Built-in Defaults**: A default set of configurations is bundled with the `semops2` application.
    *   **Project Configuration**: Configurations are loaded from a designated directory (e.g., `.semops/`) within the project root. This same override logic applies to assets like Jinja2 templates, allowing a project to use its own versions in place of the defaults.
    *   **Explicit Path**: A CLI flag (`--config-path`) can be used to provide a path to a configuration directory, which takes the highest precedence.

This allows `semops2` to be a portable tool while giving each knowledge base full control over its own configuration.

## Testing Strategy

SemOps2 employs a multi-layered testing approach to ensure correctness and reliability.

1.  **Behavior-Driven Development (BDD)**: High-level features and user-facing behaviors are defined as Gherkin scenarios in the documentation (`docs/ENTITY_CONFIGURATION.md`). These serve as the primary acceptance criteria.

2.  **Unit and Integration Testing**: Lower-level testing is conducted using `pytest`.
    *   **Framework**: `pytest` is the standard framework for all unit and integration tests.
    *   **Directory Structure**: A top-level `tests/` directory mirrors the `src/` package structure. For example, tests for `src/core/entity_service.py` reside in `tests/core/test_entity_service.py`.
    *   **Mocking**: The `pytest-mock` plugin is used to isolate components. This is essential for testing services without interacting with the live file system, external APIs, or LLM endpoints.
    *   **Fixtures**: `pytest` fixtures are used to provide consistent and reusable test setups, such as creating temporary configuration files on disk (`tmp_path`) or providing mock service objects.

## Logging and Auditing Strategy

To provide observability, traceability, and security, SemOps2 implements a three-tiered logging strategy.

1.  **Application Logging**: Standard developer-focused logs (INFO, DEBUG, ERROR) for monitoring application health. Logs are structured as JSON for easy aggregation and analysis by external systems.

2.  **Audit Logging**: A critical, immutable record of all state-changing operations (`create`, `update`, `delete`). Each audit log entry is structured to capture:
    *   `timestamp`
    *   `actor_id` (e.g., `user:john.doe` or `agent:triage-ai`)
    *   `action` (e.g., `entity.create`)
    *   `target_entity_id`
    *   A diff or summary of the changes made.
    This is handled by the `EntityService` and `WorkflowEngine` to ensure all mutations are tracked.

3.  **AI Interaction Logging**: A detailed trace of every interaction with the LLM for debugging, evaluation, and cost management. This includes the full prompt, the raw response, token counts, and latency, and is handled by a dedicated wrapper around the LLM client.

## Architecture Components

### Core Components (Contract-Based Architecture)

semops2/
├── schema/                   # **SERVICE CONTRACTS** - Protobuf schemas defining all interfaces
│   └── v1/
│       ├── core.proto        # Base types: EntityID, Entity, validation rules
│       ├── entities.proto    # Domain, Problem, Persona, Product definitions
│       ├── experts.proto     # Expert system service contracts
│       ├── knowledge.proto   # Knowledge repository service contracts
│       └── services.proto    # Main service interfaces: EntityService, ExpertService
├── src/                      # Source code implementing the contracts
│   ├── core/
│   │   ├── generated/        # **GENERATED FROM CONTRACTS** - Auto-generated from protobuf
│   │   │   ├── services_pb2.py        # Service interface implementations
│   │   │   ├── entities_pb2.py        # Entity message types
│   │   │   └── *_pb2_grpc.py          # gRPC service stubs
│   │   ├── entity_service.py # Implements protobuf-defined EntityService contract
│   │   ├── template_service.py # Manages template loading, versioning, and migration
│   │   ├── expert_service.py # Implements protobuf-defined ExpertService contract
│   │   ├── knowledge_service.py # Implements protobuf-defined KnowledgeService contract
│   │   ├── template_engine.py # Jinja2 template processing using generated types
│   │   ├── context_detector.py # Working directory context detection
│   │   └── config_manager.py  # Configuration loading and validation
│   ├── models/
│   │   ├── entity_type.py     # Entity type definition model
│   │   ├── entity.py          # Individual entity model
│   │   ├── expert_type.py     # Expert persona definition model
│   │   ├── expert.py          # Expert instance model
│   │   ├── source_type.py     # Source type definition model
│   │   ├── storage_backend.py # Storage backend configuration model
│   │   └── context.py         # Context information model
│   ├── experts/
│   │   ├── prompt_generator.py # Dynamic expert prompt generation
│   │   ├── workflow_engine.py # Multi-expert workflow execution
│   │   └── synthesis_engine.py # Expert analysis synthesis
│   ├── knowledge/
│   │   ├── extractors/        # Source content extractors
│   │   ├── processors/        # Content processing pipeline
│   │   ├── chunkers/          # Content chunking strategies
│   │   ├── enrichers/         # Metadata and relationship enrichment
│   │   ├── stores/            # Storage backend implementations
│   │   └── retrievers/        # RAG retrieval strategies
│   ├── cli/
│   │   ├── dynamic_commands.py # Auto-generated CLI commands
│   │   └── formatters.py      # Output formatting utilities
│   └── utils/
│       ├── frontmatter.py     # YAML frontmatter utilities
│       ├── file_utils.py      # File system operations
│       └── slug_utils.py      # Slug generation utilities
├── schema/                   # Protobuf schema definitions
├── generated/                # **CONTRACT IMPLEMENTATIONS** - Auto-generated from protobuf
│   ├── python/               # Generated Python gRPC clients and types
│   ├── typescript/           # Generated TypeScript clients for web UI
│   ├── go/                   # Generated Go clients for performance services
│   ├── mcp/                  # Generated MCP tool definitions and handlers
│   └── api/
│       ├── openapi/          # Generated OpenAPI specifications
│       ├── graphql/          # Generated GraphQL schemas
│       └── jsonschema/       # Generated JSON Schema validation
└── tests/                    # Tests using generated contracts and message builders

knowledge-base-project/
├── .semops-project           # Marker file indicating the project root
├── .semops/                  # Project-specific configuration
│   ├── entity_types.yaml
│   ├── workflows.yaml
│   └── templates/
│       ├── domain.md.j2
│       └── problem.md.j2
└── domain/                   # The actual knowledge base content
    └── my-first-domain/
        └── domain.md

## Entity Type Configuration Schema

```yaml
# config/entity_types.yaml
entity_types:
  domain:
    # Identity
    id_prefix: "DOM"
    name_field: "domain_name"
    slug_field: "domain_slug"

    # Template & Structure
    template: "domain.md.j2"
    directory_name: "domain"
    filename_pattern: "{entity_type}.md"    # → domain.md for context detection

    # Hierarchy & Nesting
    parent_entity: null
    child_entities: ["problem", "solution"]
    nesting_strategy: "root"                # Root entity
    scoped_to_parent: false
    context_level: 1

    # Validation
    required_fields: ["domain_name", "brief_description"]
    unique_fields: ["domain_name", "domain_slug"]

    # CLI Configuration
    list_command: true
    get_command: true
    create_command: true
    analyze_command: true

  problem:
    id_prefix: "PROB"
    name_field: "problem_name"
    slug_field: "problem_slug"
    template: "problem.md.j2"
    directory_name: "problems"
    filename_pattern: "{entity_type}.md"    # → problem.md for context detection

    # Hierarchy & Nesting
    parent_entity: "domain"
    child_entities: ["persona"]
    nesting_strategy: "nested_directories"  # Creates problems/{slug}/problem.md
    scoped_to_parent: true                  # Must exist within specific domain
    context_level: 2
    required_fields: ["problem_name", "domain_id"]

  persona:
    id_prefix: "PERS"
    name_field: "persona_name"
    slug_field: "persona_slug"
    template: "persona.md.j2"
    directory_name: "personas"
    filename_pattern: "{entity_type}.md"    # → persona.md for context detection

    # Hierarchy & Nesting
    parent_entity: "problem"
    child_entities: []
    nesting_strategy: "nested_directories"  # Creates personas/{slug}/persona.md
    scoped_to_parent: true                  # Persona for specific problem
    context_level: 3
    required_fields: ["persona_name", "problem_id"]

  # New generic entity types with nested structure
  solution:
    id_prefix: "SOL"
    name_field: "solution_name"
    slug_field: "solution_slug"
    template: "solution.md.j2"
    directory_name: "solutions"
    filename_pattern: "{entity_type}.md"    # → solution.md

    # Hierarchy & Nesting
    parent_entity: "domain"
    child_entities: ["feature"]
    nesting_strategy: "nested_directories"  # solutions/{slug}/solution.md
    scoped_to_parent: true                  # Solution for specific domain
    context_level: 2
    required_fields: ["solution_name", "domain_id"]

  feature:
    id_prefix: "FEAT"
    name_field: "feature_name"
    slug_field: "feature_slug"
    template: "feature.md.j2"
    directory_name: "features"
    filename_pattern: "{entity_type}.md"    # → feature.md

    # Hierarchy & Nesting
    parent_entity: "solution"
    child_entities: []
    nesting_strategy: "nested_directories"  # features/{slug}/feature.md
    scoped_to_parent: true                  # Feature for specific solution
    context_level: 3
    required_fields: ["feature_name", "solution_id"]
```

## Key Architectural Patterns

### Protobuf Service Contracts - Foundation Architecture

All services in SemOps2 communicate through **strictly-defined protobuf contracts** that eliminate interface drift and ensure type safety:

```protobuf
// schema/v1/services.proto - SERVICE CONTRACTS
service EntityService {
  // Contract defines exact interface between CLI, API, MCP, and service
  rpc CreateEntity(CreateEntityRequest) returns (CreateEntityResponse);
  rpc GetEntity(GetEntityRequest) returns (GetEntityResponse);
  rpc ListEntities(ListEntitiesRequest) returns (ListEntitiesResponse);
}

// schema/v1/core.proto - SHARED TYPES
message EntityID {
  string id = 1 [(validate.rules).string.pattern = "^[A-Z]{2,5}-[a-z0-9-]+$"];
  string entity_type = 2;
  string slug = 3 [(validate.rules).string.pattern = "^[a-z0-9-]+$"];
}
```

**Contract Benefits:**
- **CLI, API, MCP use identical types** - Same `EntityID` message everywhere
- **Breaking changes prevented** - `buf breaking` detects interface violations
- **Type safety guaranteed** - Generated validators prevent runtime errors
- **Cross-language compatibility** - Python, TypeScript, Go clients from same schema
- **Zero interface maintenance** - All access methods stay synchronized automatically

**Contract Enforcement:**
```bash
# Contract validation in CI/CD
buf breaking --against '.git#branch=main'  # Prevents breaking changes
buf generate                                # Regenerates all clients from contracts
```

### 1. Contract-Based Generic Entity Service

EntityService implements the **protobuf-defined service contract**, ensuring identical behavior across CLI, API, and MCP:

```python
# Implementation follows protobuf contract exactly
class EntityService(services_pb2_grpc.EntityServiceServicer):
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.template_engine = TemplateEngine()
        self.context_detector = ContextDetector()

    # Contract method: uses generated request/response types
    def ListEntities(self, request: services_pb2.ListEntitiesRequest,
                    context) -> services_pb2.ListEntitiesResponse:
        """Implementation of protobuf-defined ListEntities contract."""
        entities = self._load_entities_by_type(request.entity_type, request.parent_id)
        return services_pb2.ListEntitiesResponse(entities=entities)

    def GetEntity(self, request: services_pb2.GetEntityRequest,
                 context) -> services_pb2.GetEntityResponse:
        """Implementation of protobuf-defined GetEntity contract."""
        entity = self._load_entity(request.entity_id)
        return services_pb2.GetEntityResponse(entity=entity)

    def CreateEntity(self, request: services_pb2.CreateEntityRequest,
                    context) -> services_pb2.CreateEntityResponse:
        """Implementation of protobuf-defined CreateEntity contract."""
        # Uses generated types - no manual validation needed
        entity = self._create_from_template(request.entity_type, request.variables)
        return services_pb2.CreateEntityResponse(entity=entity)
```

**Contract Guarantees:**
- **CLI calls same methods as API** - Both use generated gRPC clients
- **MCP tools auto-generated** - Tool schemas derived from service contract
- **Type validation automatic** - Protobuf validates all inputs/outputs
- **Breaking changes impossible** - Contract changes require explicit schema evolution

### 2. Multi-Agent Expert System Integration

```python
### 7. Multi-Expert Workflow Engine

To orchestrate complex methodologies that require multiple specialized AI agents, the system uses a `WorkflowEngine`.

1.  **Specialized Experts**: First, individual experts are defined in `config/experts.yaml`, each with a unique persona and skill.

    ```yaml
    # in config/experts.yaml
    experts:
      boundary_definer:
        persona: "You are a business strategist specializing in market segmentation..."
      tension_analyzer:
        persona: "You are a systems thinker who identifies underlying conflicts..."
    ```

2.  **Configurable Workflows**: Next, a multi-step workflow is defined in `config/workflows.yaml`. Each step specifies an expert, a task, and how its output should be handled.

    ```yaml
    # in config/workflows.yaml
    workflows:
      define_domain_strategy:
        name: "Define Domain Strategy"
        description: "A two-step process for defining domain boundaries and tensions."
        applicable_entity_types: ["domain"] # Restricts this workflow to 'domain' entities
        steps:
          - name: "Define Boundaries"
            expert: "boundary_definer"
            task: "Define clear, justifiable boundaries for the domain."
            model: "claude-3-opus" # Optional: Specify a powerful model for this critical step
            output_field: "domain_boundaries"
            validation: # Optional: Defines a validation check for the step's output
              expert: "quality_analyst"
              criteria: "Ensure the boundaries are specific, measurable, and do not overlap with existing domains."
              on_failure: "stop" # Action to take if validation fails
            inputs:
              - name: "human_feedback" # Declares a required input named 'human_feedback'.
                description: "Corrections and instructions from a human expert."
                required: true
          - name: "Analyze Tensions"
            expert: "tension_analyzer"
            task: "Analyze the domain for foundational tensions."
            model: "gpt-4-turbo" # Optional: Use a different model for another step
            input_from: "previous_step"
            output_field: "foundational_tensions"
    ```

3.  **Workflow Execution**: The user invokes the entire workflow with a single command. The `WorkflowEngine` then executes each step in sequence, using the `EntityService` to update the target file at each stage.

    ```bash
    semops domain analyze --id DOM-cloud-governance --workflow define_domain_strategy

4.  **Workflow Discovery**: Workflows are discoverable via the CLI. The `semops workflow list` command shows all available workflows, and when run inside an entity context, it highlights those applicable to the current entity type.
    ```

This architecture transforms implicit methodologies into explicit, version-controllable assets that can be executed consistently by both humans and AI agents.
    def __init__(self, config_manager: ConfigManager):
        self.experts = config_manager.get_expert_types()
        self.mappings = config_manager.get_entity_expert_mappings()
        self.prompt_generator = ExpertPromptGenerator()
        self.workflow_engine = WorkflowEngine()

    def get_expert_analysis(self, entity_type: str, entity_data: Dict,
                          expert_type: Optional[str] = None) -> Dict:
        """Generate expert analysis using specialized AI agents."""
        # Get appropriate expert for entity type
        expert = expert_type or self.mappings.get_primary_expert(entity_type)

        # Generate expert-specific prompt
        prompt = self.prompt_generator.generate_expert_prompt(expert, entity_type, entity_data)

        # Execute analysis with expert specialization
        return self._execute_expert_analysis(expert, prompt, entity_data)

    def run_multi_expert_workflow(self, workflow_name: str, entity_data: Dict) -> Dict:
        """Execute multi-expert analysis workflow with synthesis."""
        workflow = self.workflow_engine.get_workflow(workflow_name)

        results = {}
        for phase in workflow.phases:
            if phase.synthesis:
                # Synthesis phase combines multiple expert analyses
                results[phase.name] = self._synthesize_expert_analyses(
                    [results[dep] for dep in phase.depends_on]
                )
            else:
                # Individual expert analysis phase
                results[phase.name] = self.get_expert_analysis(
                    entity_type=entity_data['entity_type'],
                    entity_data=entity_data,
                    expert_type=phase.expert
                )

        return results

class ExpertPromptGenerator:
    def generate_expert_prompt(self, expert_type: str, entity_type: str, context: Dict) -> str:
        """Generate dynamic expert-specific prompts."""
        expert_config = self.experts[expert_type]

        # Load expert header template
        header_template = self.load_template(expert_config.templates.header)

        # Generate expert context
        expert_context = {
            'expert_name': expert_config.name,
            'expert_role': expert_config.persona.role,
            'specialization': expert_config.persona.specialization,
            'expertise_areas': expert_config.expertise,
            'methodology': expert_config.analysis_approach.methodology,
            'entity_type': entity_type,
            'entity_context': context
        }

        return header_template.render(expert_context)
```

### 3. Generic Knowledge Repository Integration

```python
class KnowledgeService:
    """Generic knowledge repository supporting multiple source types and storage backends."""

    def __init__(self, config_manager: ConfigManager, domain_path: Path):
        self.config = config_manager
        self.domain_path = domain_path
        self.source_types = config_manager.get_source_types()
        self.storage_backends = config_manager.get_storage_backends()
        self.rag_workflows = config_manager.get_rag_workflows()

        # Initialize pluggable components
        self.extractors = self._load_extractors()
        self.processors = self._load_processors()
        self.stores = self._initialize_stores()
        self.retrievers = self._initialize_retrievers()

    def add_knowledge_source(self, source_type: str, source_config: Dict) -> str:
        """Add and process knowledge source using configured pipeline."""
        source_type_config = self.source_types[source_type]

        # Execute processing pipeline
        raw_content = self.extractors[source_type].extract(source_config)
        processed_content = self.processors[source_type].process(raw_content)
        chunks = self._chunk_content(processed_content, source_type_config)
        enriched_chunks = self._enrich_content(chunks, source_type_config)

        # Store in configured backends
        source_id = self._store_knowledge(enriched_chunks, source_type_config.storage)
        return source_id

    def retrieve_context(self, query: str, expert_type: str = None,
                        workflow: str = "basic_semantic") -> RAGContext:
        """Retrieve relevant context using specified RAG workflow."""

        # Select appropriate workflow
        if expert_type:
            workflow = self.rag_workflows.get_workflow_for_expert(expert_type) or workflow

        rag_workflow = self.rag_workflows[workflow]
        retriever = self.retrievers[workflow]

        # Execute retrieval workflow
        context = retriever.retrieve(query, rag_workflow.steps)

        return RAGContext(
            content=context.content,
            sources=context.sources,
            confidence_scores=context.scores,
            retrieval_method=workflow
        )

### 5. Source Weighting and Authority

To differentiate between authoritative sources (e.g., official documentation) and conversational ones (e.g., meeting notes), the system supports source weighting.

1.  **Configuration**: A `weight` attribute (e.g., 0.0 to 1.0) is added to each source type in `config/source_types.yaml` to represent its authority.

    ```yaml
    # config/source_types.yaml
    source_types:
      official_documentation:
        weight: 1.0
      meeting_notes:
        weight: 0.5
    ```

2.  **Metadata Enrichment**: During the `enrich` phase of the knowledge processing pipeline, this `weight` is embedded as metadata into every chunk derived from a source (e.g., `"source_weight": 0.5`).

3.  **Weighted Retrieval**: The `retrievers` in the `KnowledgeService` use this metadata to re-rank search results. A chunk's final score is a combination of its semantic relevance and its source's authority, ensuring that more trustworthy information is prioritized.

class MultiModalKnowledgeRepository(KnowledgeService):
    """Extended repository with multi-modal capabilities."""

    def search_multimodal(self, query: Union[str, Path],
                         modalities: List[str] = ["text", "image"]) -> List[MultiModalResult]:
        """Search across text and media content."""

        results = []

        if "text" in modalities:
            text_results = self.retrieve_context(query, workflow="hybrid_search")
            results.extend(text_results.sources)

        if "image" in modalities:
            if isinstance(query, str):
                # Text-to-image search using CLIP
                image_results = self._clip_search(query)
            else:
                # Image-to-image similarity
                image_results = self._image_similarity_search(query)
            results.extend(image_results)

        return self._rank_multimodal_results(results)
```

### 4. Dynamic CLI Command Generation

```python
# CLI commands auto-generated from entity type configuration
def generate_cli_commands(config_manager: ConfigManager) -> typer.Typer:
    app = typer.Typer()

    for entity_type, config in config_manager.get_entity_types().items():
        entity_app = typer.Typer(help=f"{entity_type.title()} operations")

        if config.list_command:
            add_list_command(entity_app, entity_type, config)
        if config.get_command:
            add_get_command(entity_app, entity_type, config)
        if config.create_command:
            add_create_command(entity_app, entity_type, config)
        if config.analyze_command:
            add_analyze_command(entity_app, entity_type, config)

        app.add_typer(entity_app, name=entity_type)

    return app
```

### 5. MCP Server Integration

```python
# Auto-generated MCP server from protobuf services
class MCPServerIntegration:
    """MCP server that exposes SemOps services as MCP tools."""

    def __init__(self, entity_service: EntityService, expert_service: ExpertService,
                 knowledge_service: KnowledgeService):
        self.entity_service = entity_service
        self.expert_service = expert_service
        self.knowledge_service = knowledge_service
        self.mcp_server = SemOpsMCPServer()

    async def start_server(self):
        """Start the MCP server with auto-generated tools."""
        # Initialize server with services
        self.mcp_server.initialize_services(
            self.entity_service,
            self.expert_service,
            self.knowledge_service
        )

        # Register additional custom tools if needed
        await self._register_custom_tools()

        # Start stdio server
        await self.mcp_server.run()

    async def _register_custom_tools(self):
        """Register any domain-specific custom tools."""
        # Custom tools can be added here for specialized workflows
        pass

class MCPToolGenerator:
    """Generates MCP tool definitions from protobuf service definitions."""

    def generate_tools_from_protobuf(self, service_definitions: Dict) -> List[Tool]:
        """Auto-generate MCP tools from protobuf service definitions."""
        tools = []

        for service_name, service_def in service_definitions.items():
            for method_name, method_def in service_def.methods.items():
                tool = Tool(
                    name=f"semops_{method_name.lower()}",
                    description=method_def.description or f"{method_name} operation",
                    inputSchema=self._protobuf_to_json_schema(method_def.input_type)
                )
                tools.append(tool)

        return tools

    def _protobuf_to_json_schema(self, protobuf_message) -> Dict:
        """Convert protobuf message definition to JSON schema."""
        schema = {"type": "object", "properties": {}, "required": []}

        for field in protobuf_message.fields:
            field_schema = self._field_to_schema(field)
            schema["properties"][field.name] = field_schema

            if field.label == "LABEL_REQUIRED":
                schema["required"].append(field.name)

        return schema

    def _field_to_schema(self, field) -> Dict:
        """Convert protobuf field to JSON schema property."""
        type_mapping = {
            "TYPE_STRING": {"type": "string"},
            "TYPE_INT32": {"type": "integer"},
            "TYPE_BOOL": {"type": "boolean"},
            "TYPE_MESSAGE": {"type": "object"}
        }

        base_schema = type_mapping.get(field.type, {"type": "string"})

        # Add validation rules if present
        if hasattr(field, 'validate_rules'):
            if field.validate_rules.string.pattern:
                base_schema["pattern"] = field.validate_rules.string.pattern
            if field.validate_rules.string.in_:
                base_schema["enum"] = list(field.validate_rules.string.in_)

        return base_schema
```

### 6. Context-Aware Operations with Nested Hierarchy

```python
class ContextDetector:
    def detect_context(self) -> Optional[Context]:
        """Detect current semantic context from nested directory structure."""
        path = Path.cwd()
        context = Context()

        # Walk up directory tree looking for entity type files
        current_path = path
        while current_path.parent != current_path:
            for entity_type, config in self.config.get_entity_types().items():
                # Look for type-based filename (domain.md, problem.md, persona.md)
                entity_file = current_path / config.filename_pattern.format(entity_type=entity_type)

                if entity_file.exists():
                    # Extract entity info from directory structure
                    entity_info = self._extract_entity_info(current_path, entity_type, config)
                    context.add_entity_level(entity_type, entity_info)

            current_path = current_path.parent

        # Build hierarchical context from discovered entities
        return context.build_hierarchy() if context.has_entities() else None

    def _extract_entity_info(self, path: Path, entity_type: str, config: EntityConfig) -> Dict:
        """Extract entity information from directory path and file."""
        if config.nesting_strategy == "root":
            # Root entity: domain/cloud-security/ → slug = cloud-security
            slug = path.name
        else:
            # Nested entity: problems/compliance-challenges/ → slug = compliance-challenges
            slug = path.name

        entity_id = f"{config.id_prefix}-{slug}"

        return {
            'entity_type': entity_type,
            'entity_id': entity_id,
            'slug': slug,
            'path': path,
            'file_path': path / config.filename_pattern.format(entity_type=entity_type),
            'parent_path': self._get_parent_path(path, config),
            'nesting_level': config.context_level
        }

    def auto_resolve_entity_id(self, entity_type: str) -> Optional[str]:
        """Auto-resolve entity ID from hierarchical context."""
        context = self.detect_context()
        if context and context.has_entity_type(entity_type):
            return context.get_entity_id(entity_type)
        return None

    def get_context_hierarchy(self) -> Dict[str, Any]:
        """Get full hierarchical context from nested structure."""
        context = self.detect_context()
        if not context:
            return {}

        return {
            'current_context': context.get_current_entity(),
            'hierarchy': context.get_full_hierarchy(),
            'available_operations': context.get_available_operations(),
            'parent_entities': context.get_ancestors(),
            'child_entity_types': context.get_possible_children()
        }

class Context:
    def __init__(self):
        self.entities = {}  # entity_type -> entity_info

    def add_entity_level(self, entity_type: str, entity_info: Dict):
        """Add discovered entity to context."""
        self.entities[entity_type] = entity_info

    def build_hierarchy(self) -> 'Context':
        """Build parent-child relationships from nested structure."""
        # Sort by nesting level (domain=1, problem=2, persona=3, etc.)
        sorted_entities = sorted(
            self.entities.items(),
            key=lambda x: x[1]['nesting_level']
        )

        # Build parent relationships
        for i, (entity_type, entity_info) in enumerate(sorted_entities):
            if i > 0:  # Not root entity
                parent_type, parent_info = sorted_entities[i-1]
                entity_info['parent_id'] = parent_info['entity_id']
                entity_info['parent_type'] = parent_type

        return self

    def get_current_entity(self) -> Dict:
        """Get the deepest/most specific entity in current context."""
        if not self.entities:
            return {}

        # Return entity with highest nesting level
        return max(self.entities.values(), key=lambda x: x['nesting_level'])

    def get_entity_id(self, entity_type: str) -> Optional[str]:
        """Get entity ID for specific type in current context."""
        return self.entities.get(entity_type, {}).get('entity_id')
```

### 7. Directory Structure Examples

**Nested Generic Structure:**
```
domain/cloud-security/                   # Root domain directory
├── domain.md                            # Type-based filename for context
├── sources/                             # Domain-level sources
├── working/                             # Domain analysis files
├── problems/                            # Problem entity directory
│   ├── compliance-challenges/           # Problem slug directory
│   │   ├── problem.md                   # Type-based filename
│   │   ├── sources/                     # Problem-specific sources
│   │   ├── working/
│   │   └── personas/                    # Personas FOR THIS PROBLEM
│   │       ├── security-manager/
│   │       │   ├── persona.md           # Persona for this problem
│   │       │   └── working/
│   │       └── compliance-officer/
│   │           ├── persona.md
│   │           └── working/
│   └── cost-optimization/               # Different problem
│       ├── problem.md
│       └── personas/                    # Different personas/instances
│           └── budget-controller/
│               └── persona.md
├── solutions/                           # NEW: Solution entity directory
│   └── zero-trust-platform/            # Solution slug directory
│       ├── solution.md                  # Type-based filename
│       ├── sources/
│       ├── working/
│       └── features/                    # Features FOR THIS SOLUTION
│           ├── threat-detection/
│           │   ├── feature.md
│           │   └── working/
│           └── compliance-dashboard/
│               ├── feature.md
│               └── working/
└── research/                            # NEW: Research entity directory
    └── market-analysis-2024/
        ├── research.md
        └── working/
```

**Context Detection Examples:**

Working Directory: `/domain/cloud-security/problems/compliance-challenges/personas/security-manager/`

Detected Context:
```yaml
context:
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
    - "This persona exists FOR compliance-challenges problem"
    - "This persona exists WITHIN cloud-security domain"
    - "Persona is scoped to specific problem context"
```

### 6. Source Management Model (Across Entities)

SemOps2 treats knowledge sources as first-class, configurable resources that can be associated at any entity level (domain, problem, persona, product, or any future type). The model supports inheritance, overrides, and cross-domain relationships while preserving a clear and deterministic resolution algorithm.

#### Concepts

- Source Types
  - Defined in `config/source_types.yaml` with extractor/processor/chunker pipelines
  - Examples: `web_page`, `pdf`, `markdown_note`, `repo`, `api`, `dataset`
- Source Instance
  - A concrete source item with metadata and a stable `source_id` (URL-hash-based)
- Association
  - Explicit links between a source instance and one or more entities
  - Scope can be `attached` (direct) or `inherited` (via ancestors)

#### Configuration

- Root entity types are configurable (default: `domain`). Multiple roots are supported.
- Per source type, define which entity types it can attach to and default scope behavior.

```yaml
# config/source_types.yaml
source_types:
  web_page:
    extractor: web
    processor: readability_html
    chunker: semantic_text
    enrichers: [relationships, tags]
    attach_to: ["domain", "problem", "persona", "product"]
    default_scope: "inherit"  # inherit to descendants unless overridden

settings:
  roots: ["domain"]  # root entity types in the hierarchy
```

#### Source Association (Frontmatter)

Entity documents can declare direct associations and overrides via YAML frontmatter. Associations should also be stored in a separate index for fast resolution.

```yaml
# Example: domain/foo.md frontmatter
sources:
  attach:  # direct attachments at this entity
    - src_id: SRC-PatternsPainsMigrating-5fdbec50
      type: web_page
      title: "Patterns, Pains, and Migrating"
      tags: [vmware, migration]
  exclude:  # block specific sources from inheritance to children
    - SRC-OldBlog-12345678
```

```yaml
# Example: problem/cost-shock.md frontmatter
sources:
  attach:
    - src_id: SRC-Broadcom-PriceChange-9abc0123
  exclude:
    - SRC-PatternsPainsMigrating-5fdbec50  # stop inheritance for this subtree
```

#### Resolution Algorithm (Deterministic)

Given an `entity_context` (resolved by `ContextDetector`), compute `effective_sources(entity)`:

1. Collect direct `attach` at the entity.
2. Walk ancestors to the nearest root (`settings.roots`) and union their `attach` marked as inheritable (`default_scope: inherit` or per-association scope) while respecting any `exclude` at intermediate levels.
3. If the entity participates in cross-domain relationships, union sources from linked entities only if the relationship permits source sharing (see Relationships section).
4. Apply deduplication by `source_id`. Maintain provenance with fields: `origin_entity_id`, `scope` (`attached` or `inherited`), `depth`.
5. Apply final filters (e.g., by `source_type`, tags, security classification) as requested by the caller.

Always display a summary of resolved context and effective source counts before write operations that depend on them.

#### IDs and Metadata

- Source IDs must be stable and deterministic (URL-hash-based or content-hash-based) to avoid drift between runs.
- Minimum metadata stored alongside content chunks:
  - `source_id`, `source_type`, `title`, `url` (if applicable), `origin_entity_ids` (one or many), `tags`, `created_at`, `updated_at`.
- Chunk metadata mirrors `source_id` and includes `entity_lineage` for fast scoping.

#### Storage and Retrieval

- Storage backends (vector/graph) are pluggable via `config/storage_backends.yaml`. MVP can defer vector store to Phase 2.
- `KnowledgeService` API additions:

```python
class KnowledgeService:
    def attach_source(self, entity_id: str, source: Dict, inherit: bool = True) -> str:
        """Attach a source to an entity and process/store it. Returns source_id."""

    def detach_source(self, entity_id: str, source_id: str) -> None:
        """Remove association (and optionally unpublish from scope)."""

    def list_sources(self, entity_id: str, include_inherited: bool = True) -> List[Dict]:
        """List effective sources for an entity using the resolution algorithm."""

    def reindex_sources(self, entity_id: Optional[str] = None, force: bool = False) -> Dict:
        """Rebuild vector/graph indexes for sources attached to an entity or the whole tree."""
```

#### Relationships and Cross-Domain Source Sharing

To support domains that relate to other domains (graph vs strict tree), introduce typed relationships with explicit source-sharing policies.

```yaml
# config/entity_types.yaml (excerpt)
relationships:
  - name: "depends_on"
    from: "domain"
    to: "domain"
    share_sources: true          # include sources from target in resolution
    max_depth: 1                 # prevent runaway unions
  - name: "informs"
    from: "problem"
    to: "problem"
    share_sources: false         # metadata-only, no source union
```

Resolution step (3) uses `share_sources` to decide whether to include sources from related entities and respects `max_depth`.

#### Root Definition

- Roots define where inheritance begins. Default is `domain`, but additional roots can be defined if a different topology is desired.
- If multiple root types exist, the `ContextDetector` captures the nearest root instance for lineage calculation.

This model preserves today’s domain-root behavior while enabling fine-grained attachments, inheritance control, and cross-domain knowledge graphs when needed.

## Migration Strategy from SemOps v1

### Phase 1: Configuration and Models
1. Create entity type configuration system
2. Implement entity models and validation
3. Build template engine with Jinja2
4. Create configuration loader and validator

### Phase 2: Generic Services
1. Implement generic EntityService
2. Add context detection and auto-resolution
3. Build template-based document generation
4. Add file system utilities and frontmatter handling

### Phase 3: Dynamic CLI
1. Create dynamic command generation
2. Add output formatters and table functions
3. Implement context-aware parameter resolution
4. Add error handling with helpful hints

### Phase 4: Testing and Migration
1. Comprehensive unit tests for all components
2. Integration tests with real templates and data
3. Performance testing with large entity sets
4. Migration scripts from SemOps v1 data structures

### Phase 5: Extension and Enhancement
1. Add new entity types through configuration
2. Enhanced template features and validation
3. Advanced context detection and relationship mapping
4. API layer for external integrations

## Benefits of Generic Architecture

### For Developers
- **Single Service Class** - No more entity-specific services
- **Configuration-Driven** - New entity types without code changes
- **Consistent Patterns** - Same operations across all entity types
- **Easier Testing** - Test one service, works for all entity types
- **Reduced Complexity** - Fewer classes and less code to maintain

### For Users
- **Consistent CLI** - Same command patterns across all entity types
- **Predictable Behavior** - Context detection works the same way
- **Extensibility** - Easy to add custom entity types
- **Familiar Interface** - Same operations available for all entities

### For System Evolution
- **Flexible Hierarchies** - Support any entity relationship structure
- **Template Evolution** - Easy to update document templates
- **Validation Rules** - Configurable validation without code changes
- **Rapid Prototyping** - Quick addition of new entity types for experimentation

## Next Steps

1. **Validate Approach** - Review architecture with stakeholders
2. **Create Detailed Design** - Expand each component with implementation details
3. **Build Prototype** - Implement core components with basic functionality
4. **Test with Existing Data** - Validate against current SemOps domains and problems
5. **Plan Migration** - Define strategy for moving from v1 to v2

This generic architecture maintains all the power and flexibility of the current SemOps system while eliminating the rigid entity-specific structure that limits extensibility and creates maintenance overhead.