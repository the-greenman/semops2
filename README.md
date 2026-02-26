# SemOps2 - Generic Semantic Operations Platform

SemOps2 is a configuration-driven semantic operations platform. Any entity type — and the prompts, templates, and relationships that go with it — can be defined through YAML configuration without code changes.

## Vision

A single `EntityService` handles all entity types. Entity types, their templates and prompt bundles, and the typed relationships between them are all defined in configuration. Third-party contributions are namespaced to prevent collisions.

The initial built-in entity set is designed for **operations**: domains, roles, meetings, decisions, conversations, and artefacts.

## Key Design Decisions

### Namespaced Entity Types
Every entity type belongs to a namespace (reverse-DNS). This allows multiple contributors to define a `decision` type without collision:

```yaml
entity_types:
  decision:
    namespace: "semops.core"       # built-in
    id_prefix: "DEC"
    ...

  decision:
    namespace: "com.acme.governance"   # third-party, no collision
    id_prefix: "DEC"
    ...
```

The fully-qualified type key `semops.core/decision` is unambiguous everywhere.

### Template Bundles per Entity Type
Each entity type declares a bundle of templates and prompts — not just one template:

```yaml
decision:
  namespace: "semops.core"
  template_bundle:
    create: "decision.md.j2"
    analyze: "decision-analysis.md.j2"
    prompts:
      summarize: "prompts/decision-summarize.txt"
      extract_rationale: "prompts/decision-rationale.txt"
```

### Typed Relationships Between Entities
Relationships are graph edges, not directory nesting. The config declares which types can relate and how:

```yaml
relationship_types:
  made_in:
    namespace: "semops.core"
    from_types: ["semops.core/decision"]
    to_types: ["semops.core/meeting"]
    cardinality: many_to_one
```

### Generic Service Layer
One `EntityService` handles all types:

```python
service.list_entities("semops.core/decision")
service.create_entity("semops.core/meeting", name="Governance Review 2026-02-15")
service.get_entity_relationships("DEC-adopt-zero-trust", relationship_type="semops.core/made_in")
```

### Dynamic CLI
Commands are auto-generated from configuration:

```bash
semops decision list
semops decision create --name "Adopt Zero Trust Model"
semops meeting analyze --workflow extract_decisions
semops role list --related-to DOM-cloud-governance
```

## Architecture Approach

Protobuf-first: all service contracts, message types, and validation rules are defined in `.proto` schemas and generated via `buf`. Hand-written code implements the contracts; it never defines its own types.

```
schema/semops/v1/     # Source of truth — proto schemas
buf generate          # Produces Python gRPC, OpenAPI, docs
src/                  # Hand-written implementations of generated contracts
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for full design and [docs/IDL_ARCHITECTURE.md](docs/IDL_ARCHITECTURE.md) for the protobuf-first interface design.

## Current Status

**Sprint 0 complete.** Protobuf schemas are defined and generating Python/gRPC/OpenAPI artifacts. gRPC server scaffold exists. No business logic implemented yet.

See [TODO.md](TODO.md) for the implementation roadmap.

## Next Steps

1. Update `core.proto` — add `namespace` and `prefix` fields to `EntityID`
2. Implement `ConfigManager` with namespace validation and type registry
3. Implement `EntityService` CRUD backed by filesystem
4. Write ops entity templates and prompt bundles
5. Activate contract tests