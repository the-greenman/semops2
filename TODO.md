# SemOps2 Development TODO

## Architecture Planning

- [x] **Architecture Design** - Core generic architecture principles and patterns
- [x] **Entity Configuration System** - YAML-based entity type definitions
- [x] **Protobuf-First IDL** - Complete interface definition and code generation strategy
- [x] **Migration Planning** - Comprehensive strategy for v1 → v2 transition
- [x] **Directory Structure** - Examples of how configuration maps to file system
- [x] **Documentation** - Architecture docs and migration plan

## Phase 1: Schema-First Foundation

### Sprint 1 (Protobuf-First MVP)
- [ ] **Protobuf Schema Setup**: Define `core.proto`, `entities.proto`, `services.proto` in `schema/v1/`
- [ ] **Buf Toolchain**: Configure `buf.gen.yaml` for Python, gRPC, OpenAPI, MCP generation
- [ ] **Enforcement Setup**: Configure protobuf-first safeguards and file protection
  - [ ] Set up read-only permissions for generated directories
  - [ ] Add "DO NOT EDIT" headers to generated files
  - [ ] Configure git attributes for generated files
  - [ ] Create pre-commit hooks to prevent manual edits
- [ ] **Code Generation**: Run `buf generate` to create all Python types and service stubs
- [ ] **ConfigManager**: Load YAML using generated protobuf message types (no manual Pydantic)
- [ ] **Validation**: Use generated protobuf validators with actionable error messages
- [ ] **EntityService**: Implement gRPC service using generated request/response types
- [ ] **Context Detection**: Use generated `Context` and `EntityID` message types
- [ ] **Template Engine**: Inject generated message data into Jinja2 templates
- [ ] **Generated CLI**: Auto-generate CLI commands from protobuf service definitions
- [ ] **MCP Integration**: Auto-generate MCP tools from protobuf schemas
- [ ] **CLAUDE.md Updates**: Add protobuf-first workflow rules for AI agents
- [ ] Unit tests using generated message builders and service stubs

### Generated Types & Validation
- [ ] **All types from protobuf**: `EntityType`, `Entity`, `Context` auto-generated (no manual models)
- [ ] **Protobuf validation**: Generated validators with regex patterns and constraints
- [ ] **Schema evolution**: Backward compatibility built into protobuf definitions
- [ ] **JSON Schema generation**: Auto-generated from protobuf for external validation

### Schema-Driven Configuration
- [ ] **Protobuf-based YAML parsing**: Load entity_types.yaml into generated message types
- [ ] **Generated validation**: Use protobuf field validators for configuration errors
- [ ] **Type-safe config access**: All configuration through generated message accessors
- [ ] **Schema documentation**: Auto-generated config docs from protobuf comments

### Template Integration
- [ ] **Generated data injection**: Use protobuf message serialization for template context
- [ ] **Type-safe templates**: Template variables defined in protobuf schemas
- [ ] **Validation integration**: Template requirements validated against generated types
- [ ] **Generated template docs**: Auto-document template variables from schemas

### Generated Testing Framework
- [ ] **Message builders**: Generated test utilities for creating protobuf messages
- [ ] **Service mocking**: Use generated gRPC service stubs for testing
- [ ] **Schema validation tests**: Test generated validators against edge cases
- [ ] **Integration test fixtures**: Generated sample data from protobuf schemas

## Phase 2: Generic Entity Service 

### Sprint 2 (usability + migration prep)
- [ ] CLI formatting and contextual hint messages
- [ ] Template migration for v1 entities to Jinja2 (domain/problem/persona/product)
- [ ] v1→v2 mapping doc and a dry-run migration command
- [ ] Optional: stub `analyze` command (wires to placeholder expert service)
- [ ] Optional: basic Chroma-backed knowledge service (ingest + retrieve)
- [ ] Additional unit/integration tests for CLI and services

#### Source Management
- [ ] Define `config/source_types.yaml` (attachable entity types, default scope, pipelines)
- [ ] Implement `KnowledgeService.attach_source/detach_source/list_sources/reindex_sources`
- [ ] Frontmatter schema for `sources.attach` and `sources.exclude` with validation
- [ ] Resolution algorithm implementation (inheritance, excludes, dedup, provenance)
- [ ] Index for fast association lookups (entity_id→source_ids, source_id→entities)
- [ ] Unit tests covering inheritance and exclude edge cases

#### Relationships & Roots
- [ ] Configure `settings.roots` in configuration and ensure `ContextDetector` captures nearest root
- [ ] Relationship types with `share_sources` and `max_depth` semantics
- [ ] Extend resolution to include related-entity sources when allowed
- [ ] Tests for cross-domain source sharing and depth limits

### EntityService Enhancements
- [ ] Context-aware parameter resolution
- [ ] Frontmatter read/write and normalization
- [ ] File system operations for renames and ID/slug updates

### Context Detection
- [ ] Hierarchical relationship resolution
- [ ] Auto-detection of entity IDs from current location
- [ ] Context validation and error reporting

### Integration Points
- [ ] Source management integration (deferred if needed)
- [ ] Vector store integration (optional in Sprint 2)
- [ ] Analysis service integration (stubbed only)

## Phase 3: Dynamic CLI System 

### Command Generation
- [ ] Dynamic CLI command registration from configuration (extend to `analyze` later)
- [ ] Parameter generation based on entity type definitions (`cli` stanza)
- [ ] Context-aware parameter defaults
- [ ] Help text generation from entity metadata

### Output Formatting
- [ ] Generic table formatters for all entity types
- [ ] JSON/YAML output formatting
- [ ] Markdown output for documentation
- [ ] Error message formatting with hints

### CLI Integration
- [ ] Integration with existing CLI framework
- [ ] Command routing and dispatch
- [ ] Error handling and user feedback
- [ ] Comprehensive CLI testing

## Phase 4: Template Migration 

### Template Conversion
- [ ] Convert existing templates to Jinja2 format
- [ ] Migrate domain/problem/persona/product templates
- [ ] Add new entity type templates (solution, feature)
- [ ] Template compatibility testing

### Validation Framework
- [ ] Template syntax validation
- [ ] Required variable checking
- [ ] Output format validation
- [ ] Template performance optimization

## Phase 5: Testing, Migration & Interop 

### Data Compatibility & Migration
- [ ] Migration utilities for existing data (v1→v2)
- [ ] Backward compatibility testing
- [ ] Performance benchmarking
- [ ] Integration testing with real data
- [ ] v1 directory layout mapping to v2 `entity_types` config (IDs, slugs, frontmatter)

### Interoperability & Quality Gates
- [ ] Vector store reindexing with stable URL-hash IDs (fix mixed ID formats like `vmware_modernisation`)
- [ ] Generated type safety: prevent runtime errors through protobuf validation
- [ ] Async boundary guidelines: no `asyncio.run()` in running loops; provide async server APIs and sync CLI wrappers
- [ ] **Auto-generated MCP integration**: Tools and handlers generated from protobuf schemas (Phase 1, not post-MVP)

## Implementation Notes

### Key Design Decisions
- **Protobuf-First**: All interfaces, types, and validation generated from schemas
- **Zero Manual Models**: No Pydantic, manual validation, or interface maintenance
- **Schema-Driven**: Configuration, CLI, MCP tools all generated from protobuf
- **Code Generation Over Writing**: Maximize automation, minimize hand-written code
- **Type Safety Everywhere**: Same protobuf types across CLI, API, MCP, templates

### Success Criteria
- [ ] **Generated EntityService**: gRPC service implementation using generated types
- [ ] **Schema-driven entities**: New entity types require only protobuf schema changes
- [ ] **Auto-generated CLI**: Commands generated from protobuf service definitions
- [ ] **Auto-generated MCP**: Tools generated from protobuf schemas with zero maintenance
- [ ] **Drift-proof interfaces**: All APIs stay synchronized via code generation
- [ ] **Type-safe throughout**: Protobuf validation prevents runtime type errors
- [ ] **All v1 functionality preserved**: Complete feature parity with generated approach

### Risk Mitigation
- [ ] **Generated Code Protection**: Comprehensive safeguards to prevent manual edits
  - [ ] File system permissions and git hooks
  - [ ] Clear documentation and AI agent guidelines
  - [ ] CI validation that generated code matches schemas
- [ ] Comprehensive testing at each phase
- [ ] Backward compatibility validation
- [ ] Performance monitoring and optimization
- [ ] Clear rollback procedures for schema changes

## Future Enhancements (Post-Migration)

### Advanced Features
- [ ] Custom validation rules per entity type
- [ ] Multi-parent entity relationships
- [ ] Plugin system for custom entity behaviors
- [ ] Advanced template features (includes, macros)

### Integration Enhancements
- [ ] REST API auto-generation from configuration
- [ ] MCP server tool auto-generation
- [ ] GraphQL schema generation
- [ ] Event-driven entity updates

### User Experience
- [ ] Interactive entity creation wizards
- [ ] Visual entity relationship mapping
- [ ] Template customization UI
- [ ] Configuration validation tools

## Schema-First Development Workflow

### Development Pattern: Schema → Generate → Implement
```bash
# 1. Define or modify protobuf schemas
edit schema/v1/core.proto

# 2. Generate all code from schemas
buf generate

# 3. Implement business logic using generated types
# - Generated request/response messages
# - Generated validators
# - Generated CLI command definitions
# - Generated MCP tool schemas
```

### Key Protobuf-First Principles
- **Single Source of Truth**: All types, validation, and interfaces defined in .proto files
- **Zero Interface Drift**: Code generation ensures perfect synchronization across all access methods
- **Type Safety**: Generated validators prevent runtime errors and catch issues at compile time
- **Minimal Hand-Written Code**: Focus on business logic, let code generation handle infrastructure
- **AI-Friendly**: Code generators eliminate human error and model drift issues
- **Enforcement Required**: Technical and procedural safeguards prevent manual editing of generated code

### Generated Artifacts
- **Python Types**: Dataclasses with validation from protobuf messages
- **gRPC Services**: Server stubs and client implementations
- **CLI Commands**: Auto-generated from service method definitions
- **MCP Tools**: Tool schemas and async handlers from protobuf services
- **API Specs**: OpenAPI, GraphQL schemas for external integration
- **Documentation**: Auto-generated API docs from protobuf comments

### Schema Evolution Strategy
- **Backward Compatibility**: Use protobuf field numbering and optional fields
- **Breaking Change Detection**: `buf breaking` validates schema changes in CI/CD
- **Versioned Schemas**: Separate schema versions in `schema/v1/`, `schema/v2/` directories
- **Generated Migrations**: Tools to migrate data between schema versions

### Protobuf-First Enforcement Mechanisms

#### Technical Safeguards
- **Read-Only Generated Directories**: `chmod -R 444 src/semops/generated/`
- **Git Attributes**: Mark generated files as `linguist-generated=true`
- **Pre-commit Hooks**: Prevent commits that manually edit generated code
- **CI Validation**: Verify generated code is up-to-date with schemas
- **File System Protection**: Separate generated/ from editable source directories

#### Documentation Safeguards
- **Generated File Headers**: Clear "DO NOT EDIT" warnings with regeneration instructions
- **CLAUDE.md Rules**: Explicit AI agent guidelines for protobuf-first workflow
- **Development Rules**: DEVELOPMENT_RULES.md with clear do/don't lists
- **Directory Structure**: Clear separation between editable and protected files

#### Workflow Safeguards
- **Schema → Generate → Implement**: Enforce correct development pattern
- **Make Right Thing Easy**: `buf generate` simpler than manual edits
- **Git Hooks**: Block manual changes to generated files
- **Linting Rules**: Custom rules to detect generated file modifications

```bash
# Example enforcement structure
semops2/
├── schema/v1/              # ✅ AI agents can edit
├── src/semops/core/        # ✅ AI agents can edit (service implementations)
├── src/semops/generated/   # 🚫 PROTECTED - Generated code only
└── api/openapi/            # 🚫 PROTECTED - Generated specs
```

---

**Current Priority**: Complete Sprint 1 of Phase 1 using the protobuf-first approach to establish schema-driven infrastructure.