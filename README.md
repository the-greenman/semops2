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

## Benefits Over SemOps v1

- **Unlimited Entity Types** - Add new types through configuration, not code
- **Single Service Class** - No more entity-specific service duplication
- **Consistent CLI** - Same command patterns across all entity types
- **Easier Maintenance** - Less code, more configuration
- **Rapid Prototyping** - Quick experimentation with new entity structures

## Architecture Approach

SemOps2 uses a **protobuf-first approach** to eliminate interface drift and ensure perfect consistency across all access methods (CLI, REST API, GraphQL, MCP).

- **Core Principles**
  - All interfaces and data structures generated from authoritative protobuf schemas
  - Single source of truth eliminates interface maintenance and drift
  - Type-safe clients auto-generated for Python, TypeScript, Go
  - Consistent ID formats enforced everywhere via protobuf validation
  - Breaking change detection in CI/CD pipeline prevents contract violations

- **Technology Stack**
  - Interface Definition: Protobuf schemas with buf toolchain
  - Code Generation: Python gRPC, OpenAPI, GraphQL, MCP tools
  - Validation: Generated protobuf validators (no manual Pydantic)
  - CLI: Auto-generated from protobuf service definitions
  - Templates: Jinja2 with generated message type injection
  - Storage: Local filesystem for entities; pluggable backends for knowledge

## Current Status

📋 **Planning Phase Complete** - Architecture design and protobuf-first approach validated.

🚧 **No Implementation Yet** - Ready to begin Sprint 0 foundation setup.

See [TODO.md](TODO.md) for detailed implementation roadmap and [ARCHITECTURE.md](ARCHITECTURE.md) for complete design specifications.

## Next Steps

1. **Sprint 0**: Set up project structure, protobuf toolchain, and development environment
2. **Sprint 1**: Define protobuf schemas and generate all Python types and service stubs
3. **Sprint 2**: Implement generic EntityService using generated contracts
4. **Sprint 3**: Build dynamic CLI system and template engine
5. **Sprint 4+**: Expert system integration and knowledge repository

---

*This is an architectural planning repository. No implementation code exists yet.*