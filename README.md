# SemOps2 - Next-Generation Generic Semantic Operations

SemOps2 is a complete architectural reimagining of the semantic operations platform, built around generic, configuration-driven entity management instead of hardcoded entity-specific services.

## Vision

Replace the rigid `DomainService`, `ProblemService`, `PersonaService` architecture with a flexible system where any entity type can be defined through configuration files and templates, without requiring code changes.

## Key Innovations

### 🔧 Configuration-Driven Entity Types
Define unlimited entity types through YAML configuration:
```yaml
entity_types:
  solution:
    id_prefix: "SOL"
    template: "solution.md.j2"
    parent_entity: "product"
    # ... configuration defines everything
```

### 🚀 Generic Service Layer
Single `EntityService` handles all entity types:
```python
service = EntityService()
service.list_entities("solution")  # Works for any entity type
service.create_entity("solution", name="AI Assistant")
```

### 🎯 Dynamic CLI Generation
Commands auto-generated from configuration:
```bash
# Same patterns work for any configured entity type
semops solution list
semops solution create --name "New Solution"
semops solution analyze
```

### 📋 Template-First Design
All entities use Jinja2 templates with consistent patterns:
- YAML frontmatter for metadata
- Standardized variable substitution
- Extensible field definitions

## Architecture Overview

```
semops2/
├── src/core/           # Generic entity operations
├── models/             # Entity type and context models
├── cli/                # Dynamic command generation
├── config/             # Entity type definitions and templates
└── tests/              # Comprehensive test suite
```

## Current Status

📋 **Planning Phase** - Architecture design and validation

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design specifications.

## Benefits Over SemOps v1

- **Unlimited Entity Types** - Add new types through configuration, not code
- **Single Service Class** - No more entity-specific service duplication
- **Consistent CLI** - Same command patterns across all entity types
- **Easier Maintenance** - Less code, more configuration
- **Rapid Prototyping** - Quick experimentation with new entity structures

## MVP Scope

The initial MVP focuses on a configuration-driven core with deterministic behavior and defers advanced integrations until contracts stabilize.

- Scope (included)
  - YAML-configured entity types with Pydantic-validated models
  - Dynamic CLI for `list`, `get`, `create` based on configuration
  - Jinja2 templates with YAML frontmatter; file emission via filesystem utilities
  - Deterministic ID and slug generation (`python-slugify`)
  - Basic context detection by walking directories and parsing frontmatter
- Out of scope (deferred)
  - Protobuf-first APIs and codegen (Buf/OpenAPI/GraphQL)
  - Expert system workflows and analysis commands
  - Knowledge repository, vector/graph stores, multimodal search

## Technology Choices (MVP)

- Models and validation: Pydantic v2 (with JSON Schema generation)
- CLI: Typer
- Templates: Jinja2
- Frontmatter: PyYAML (safe loader)
- Slugging: python-slugify
- Storage: Local filesystem for entities; optional Chroma for vector store in a later phase

## Current Status

📋 Planning complete with actionable MVP scope and technology decisions. Implementation to start with configuration loading, models, and dynamic CLI for domain/problem/persona/product.

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design and context detection algorithm.

## Next Steps

1. Implement `ConfigManager`, `EntityType`, `Entity`, and `Context` models with Pydantic validation.
2. Build `TemplateEngine`, `Frontmatter` utilities, and `FileUtils` for file emission.
3. Implement `EntityService` with `list/get/create` and deterministic ID/slug/path generation.
4. Implement basic `ContextDetector` and wire into CLI defaults.
5. Add unit tests for each module and CLI happy paths.

---

*This is an architectural planning repository. No implementation code exists yet.*