# SemOps2 Interface Contract

This document defines the protobuf-first contract shared across SemOps2 subsystems. It enumerates the generated packages, versioning rules, and collaboration guidelines so multiple agents can contribute without breaking each other.

## Purpose

- Establish a single source of truth for all public SemOps2 interfaces.
- Describe how generated artifacts are organized in the repository.
- Provide consumption and compatibility guidance for every subsystem (server, CLI, MCP, external clients).

## Generated Packages

Code generation runs via `buf generate` and writes artifacts into the repository. Generated modules are read-only for contributors—always regenerate instead of hand-editing.

| Package | Location | Contents | Consumers |
| ------- | -------- | -------- | --------- |
| `semops.generated.core_pb2` | `src/semops/generated/core_pb2.py` | Core shared messages (IDs, metadata, context) | All Python subsystems |
| `semops.generated.entities_pb2` | `src/semops/generated/entities_pb2.py` | Entity definitions and validation annotations | Core services, template engine |
| `semops.generated.services_pb2` | `src/semops/generated/services_pb2.py` | Request/response messages for gRPC services | Server, CLI, MCP adapters |
| `semops.generated.services_pb2_grpc` | `src/semops/generated/services_pb2_grpc.py` | gRPC service/base classes and client stubs | Server implementation, client integrations |
| `semops.generated.validators` | `src/semops/generated/validators/` | protoc-gen-validate helpers and JSON schema | Config loader, validation tests |

Additional language targets (OpenAPI, MCP schema, etc.) live under `generated/` peers and follow the same "do not edit" rule.

## Versioning Policy

- Protobuf package versioning is controlled by directory (`schema/v1/`). Breaking changes trigger a new package directory (`schema/v2/`).
- Generated Python packages follow semantic versioning via `pyproject.toml` once packaging is introduced. Until then, rely on git history and tags.
- All generated files include `// @generated` comments; CI enforces freshness with `buf lint`, `buf breaking`, and `buf generate --template buf.gen.yaml`.
- Consumers may not vendor generated files—import from the shared packages only.

## Consumption Guidelines

### Server Implementation

- `src/server/entity_service_server.py` implements `EntityServiceServicer` from `services_pb2_grpc`.
- Business logic lives in `src/core/` modules and must convert to/from generated messages only.
- Contract tests in `tests/contracts/test_entity_service_server.py` instantiate the server through gRPC channels and assert on protobuf messages.

### CLI

- CLI modules (`src/cli/`) depend exclusively on generated clients from `services_pb2_grpc`.
- Service discovery (local vs. remote) is configured via environment variables or config files; no CLI code imports server internals.
- CLI integration tests (`tests/cli/test_entity_service_integration.py`) use shipped stubs or fixtures that speak gRPC.

### External Integrations

- MCP adapters, REST gateways, and other agents must consume the protobuf contract instead of duplicating data models.
- Generated JSON schemas and OpenAPI specs (future deliverables) inherit from the same protobuf source to guarantee parity.

## Regeneration Workflow

```bash
# Update or add .proto files in schema/v1/
buf lint

# Recreate generated artifacts
buf generate

# Run contract and integration tests
pytest tests/contracts tests/cli
```

After regeneration, inspect diffs for the generated directories. Do not edit generated files when fixing review feedback—update the `.proto` files and regenerate instead.

## Multi-Agent Collaboration Rules

- Treat `schema/` and `docs/` as shared planning space; coordinate schema changes through PRs and ADR updates.
- Agents implementing business logic or CLI features must not alter generated modules.
- Contract-breaking changes (removing fields, renaming services) require a version bump and explicit ADR/change note in docs.
- Use contract tests as the first signal when subsystems drift from the protobuf definitions.

## Open Questions

- Packaging strategy for publishing `semops.generated` to an internal registry.
- Automation for distributing non-Python targets (e.g., TypeScript clients).
- Additional enforcement tooling (pre-commit, CI targets) still to be implemented.

Document owner: Architecture team. Update this file whenever the contract surface or regeneration workflow changes.
