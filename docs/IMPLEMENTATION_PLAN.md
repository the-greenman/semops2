# SemOps Implementation Plan Scaffold

**Date:** 2026-02-26  
**Purpose:** Turn the completed planning corpus into an implementation-oriented architecture scaffold, with explicit workstreams and source-of-truth references.

## 1. Current State Review

### Planning and architecture state
- Planning is mature and consolidated, with collaborative-org architecture, ADRs, and package examples in place.
- Core decisions are now explicit and accepted:
  - File-first canonical datastore ([ADR-0001](./decisions/ADR-0001-file-first-canonical-datastore.md))
  - Canonical config layout and naming ([ADR-0002](./decisions/ADR-0002-configuration-layout-and-naming.md))
  - Actor-expert invocation contract and resolution metadata ([ADR-0003](./decisions/ADR-0003-actor-expert-invocation-contract.md))
- Collaborative-org implementation model and invariants are documented in [COLLABORATIVE_ORG_ARCHITECTURE.md](./COLLABORATIVE_ORG_ARCHITECTURE.md).

### Code implementation state
- Runtime code is still scaffolding-level:
  - gRPC server adapter stub: [`src/server/entity_service_server.py`](/workspace/src/server/entity_service_server.py)
  - No core service implementations yet in `src/semops/core/`.
  - Contract and CLI tests are placeholders and skipped:
    - [`tests/contracts/test_entity_service_server.py`](/workspace/tests/contracts/test_entity_service_server.py)
    - [`tests/cli/test_entity_service_integration.py`](/workspace/tests/cli/test_entity_service_integration.py)
- Generated protobuf artifacts exist, but current server imports do not yet align with generated package paths.

## 2. Implementation Workstreams (Architecture Scaffold)

Each workstream below identifies what must be implemented to move from planning to executable architecture.

### A. Contract Baseline and Schema Alignment
- Goal: Lock runtime contracts to protobuf and align generated module usage.
- Code-level impact:
  - Normalize generated import paths across server/CLI/core.
  - Apply immediate schema updates called out in architecture docs (e.g., `EntityID` and service surface updates).
  - Establish schema evolution and breaking-change checks as gating workflow.
- Primary references:
  - [ARCHITECTURE.md](./ARCHITECTURE.md) (Current Status and Next Steps)
  - [IDL_ARCHITECTURE.md](./IDL_ARCHITECTURE.md)
  - [INTERFACE_CONTRACT.md](./INTERFACE_CONTRACT.md)

### B. Configuration Subsystem (Canonical Discovery + Validation)
- Goal: Implement strict `.semops/config/*.yaml` loading and validation behavior.
- Code-level impact:
  - `ConfigManager` for root detection, layered loading, and strict path validation.
  - Namespace-aware entity type registry and reserved namespace rules.
  - Clear error surfaces for non-canonical paths.
- Primary references:
  - [ADR-0002](./decisions/ADR-0002-configuration-layout-and-naming.md)
  - [ARCHITECTURE.md](./ARCHITECTURE.md) (Configuration Management)
  - [ENTITY_CONFIGURATION.md](./ENTITY_CONFIGURATION.md)

### C. Entity Server and Canonical Write Path
- Goal: Implement `EntityService` as the only mutation boundary.
- Code-level impact:
  - CRUD over canonical markdown/frontmatter documents.
  - Policy, relationship, and attribution checks centralized in service layer.
  - No direct writes from CLI/MCP/workflows to graph/vector stores.
- Primary references:
  - [ADR-0001](./decisions/ADR-0001-file-first-canonical-datastore.md)
  - [COLLABORATIVE_ORG_ARCHITECTURE.md](./COLLABORATIVE_ORG_ARCHITECTURE.md) (Architecture Invariants)
  - [ARCHITECTURE.md](./ARCHITECTURE.md) (Generic Service Layer)

### D. Projection and Reconciliation Pipeline (Graph/Vector as Derived)
- Goal: Build reliable derived-index updates and repair paths.
- Code-level impact:
  - Post-write projection updates or durable outbox queue.
  - Sync-status metadata persisted per mutation.
  - Reconciliation and rebuild tooling for eventual consistency.
- Primary references:
  - [ADR-0001](./decisions/ADR-0001-file-first-canonical-datastore.md) (Required Runtime Guardrails)
  - [COLLABORATIVE_ORG_ARCHITECTURE.md](./COLLABORATIVE_ORG_ARCHITECTURE.md) (Hybrid Persistence Model)
  - [KNOWLEDGE_REPOSITORY_ARCHITECTURE.md](./KNOWLEDGE_REPOSITORY_ARCHITECTURE.md)

### E. Entity Package Runtime (Definitions + Journeys)
- Goal: Make packaged entity definitions and journey YAML executable.
- Code-level impact:
  - Package loader for `entity_definition.yaml` + `experts.yaml` + `journey_definition.yaml` + template bundle metadata.
  - Journey runtime (stage execution, loop/branch transitions, pause/resume checkpointing).
  - CLI commands to discover/start/resume/list journeys.
- Primary references:
  - [COLLABORATIVE_ORG_ARCHITECTURE.md](./COLLABORATIVE_ORG_ARCHITECTURE.md) (Entity-Journey Framework)
  - [examples/entity_packages/README.md](/workspace/examples/entity_packages/README.md)
  - [CONSOLIDATION_DECISIONS.md](./CONSOLIDATION_DECISIONS.md)

### F. Template Lifecycle and Migration Engine
- Goal: Implement template version governance as a first-class runtime subsystem.
- Code-level impact:
  - Template manifest/version resolution.
  - `migrate check/preview/run/review/rollback` flow.
  - Migration rule execution, backup retention, and audit records.
- Primary references:
  - [COLLABORATIVE_ORG_ARCHITECTURE.md](./COLLABORATIVE_ORG_ARCHITECTURE.md) (Template Evolution System)
  - [examples/TEMPLATE_EVOLUTION_GUIDE.md](/workspace/examples/TEMPLATE_EVOLUTION_GUIDE.md)
  - [examples/entity_packages/*/migration_rules.yaml](/workspace/examples/entity_packages)

### G. Authority-Weighted Knowledge and Retrieval
- Goal: Implement configurable source typing and authority-weighted retrieval for journeys and analysis.
- Code-level impact:
  - Source-type registry and authority weights.
  - RAG workflow execution (`authority_weighted`, etc.).
  - Knowledge retrieval integration with `ai.assist` journey stages.
- Primary references:
  - [COLLABORATIVE_ORG_ARCHITECTURE.md](./COLLABORATIVE_ORG_ARCHITECTURE.md) (Authority-Weighted Knowledge)
  - [KNOWLEDGE_REPOSITORY_ARCHITECTURE.md](./KNOWLEDGE_REPOSITORY_ARCHITECTURE.md)
  - [examples/config/collaborative_org_config_v2.yaml](/workspace/examples/config/collaborative_org_config_v2.yaml)

### H. Explore Read Model and Interface Surfaces
- Goal: Provide read-optimized browse/explore surfaces without bypassing mutation invariants.
- Code-level impact:
  - Add/implement explore-oriented read service in IDL/runtime.
  - Keep CLI and MCP clients contract-bound to generated interfaces.
  - Preserve strict separation: browse/read vs mutate/write.
- Primary references:
  - [COLLABORATIVE_ORG_ARCHITECTURE.md](./COLLABORATIVE_ORG_ARCHITECTURE.md) (Exploration Interface)
  - [INTERFACE_CONTRACT.md](./INTERFACE_CONTRACT.md)
  - [IDL_ARCHITECTURE.md](./IDL_ARCHITECTURE.md)

### I. Auditability, Attribution, and Test Activation
- Goal: Make architecture invariants observable and enforceable in CI/runtime.
- Code-level impact:
  - Audit logs for all mutations (actor, operation, target, diff/sync status).
  - Audit coverage for expert invocations (`actor_id`, `expert_type`, workflow, trace metadata).
  - Actor attribution enforcement (`created_by_actor_id` / `updated_by_actor_id` semantics).
  - Replace skipped tests with working contract + integration coverage.
- Primary references:
  - [COLLABORATIVE_ORG_ARCHITECTURE.md](./COLLABORATIVE_ORG_ARCHITECTURE.md) (Architecture Invariants)
  - [ARCHITECTURE.md](./ARCHITECTURE.md) (Testing Strategy, Logging and Auditing Strategy)
  - [INTERFACE_CONTRACT.md](./INTERFACE_CONTRACT.md)

### J. External Runtime Libraries and Adapters
- Goal: Introduce stable library-backed adapters without coupling core domain logic to any one framework.
- Code-level impact:
  - `LLMStructuredClient` adapter interface and implementations.
  - `RAGPipelineExecutor` adapter (Haystack-backed).
  - `PromptRegistry` plus telemetry adapter (Langfuse).
  - `ApiGatewayAdapter` (FastAPI over gRPC clients).
  - `MCPToolAdapter` (official MCP Python SDK).
  - `VectorStoreAdapter` abstraction with Chroma/Qdrant implementations.
  - `ExpertInvocationAdapter` to enforce `actor_id + expert_type` contract and package-first role resolution.
- Primary references:
  - Existing internal architecture docs already cited in section 2.
  - [External Library Baseline](#5-external-library-baseline-locked-on-2026-02-26).
  - [ADR-0003](./decisions/ADR-0003-actor-expert-invocation-contract.md).
- Required deliverables:
  1. Adapter contracts and error taxonomy.
  2. Dependency pinning policy and compatibility matrix.
  3. CI checks for structured-output compliance and prompt regressions.
  4. Backend parity tests (Chroma vs Qdrant).
  5. Actor/expert invocation conformance tests (role alias resolution + provenance).

## 3. Phase Sequence (High-Level)

1. **Phase 0: Contract + Config foundation**
   - Workstreams A-B and J foundation tasks
   - Exit criteria: schema and generated imports aligned; strict config loading validated; core adapter interfaces defined.
2. **Phase 1: Canonical mutation path**
   - Workstreams C-D
   - Exit criteria: file-first CRUD operational with projection sync/reconciliation hooks.
3. **Phase 2: Journey + templates runtime**
   - Workstreams E-F plus structured-output enforcement and prompt stack integration
   - Exit criteria: at least one end-to-end journey and one template migration path executable, with typed LLM outputs, actor-aware expert invocation, and prompt tracing in place.
4. **Phase 3: Knowledge + read interfaces**
   - Workstreams G-H plus Haystack execution and vector-backend abstraction parity
   - Exit criteria: authority-weighted retrieval integrated into journey AI stages, browse read model available, and Chroma/Qdrant parity validated.
5. **Phase 4: Hardening**
   - Workstream I plus MCP/REST parity and dependency hardening
   - Exit criteria: unskipped contract/integration suites, auditable invariant enforcement, and stable pinned dependency matrix.

## 4. Architecture-Planning Output from This Scaffold

This scaffold is intended to drive the next layer of detailed architecture artifacts:
- Per-workstream design docs (interfaces, state models, failure modes, test plans)
- Ordered implementation tickets grouped by dependency chain
- Definition of done per subsystem tied to ADR invariants
- Library decision record and lockfile strategy per subsystem.

Use this document as the implementation index; use the referenced docs as the detailed source material.

## 5. External Library Baseline (Locked on 2026-02-26)

### Core Selections
- **RAG orchestration:** Haystack-first implementation layer.
- **Structured LLM outputs:** provider JSON schema/tool-calling plus Instructor/Pydantic validation.
- **Prompt ops:** Git-managed prompts plus Langfuse tracing/versioning and promptfoo regression suites.
- **API/MCP surface:** protobuf/gRPC core plus FastAPI adapter and official MCP Python SDK.
- **Vector backend strategy:** Chroma for local development, Qdrant for production (config-selected).
- **Design rule:** All libraries stay behind SemOps adapters; framework primitives do not leak into domain services.
- **Actor/expert contract:** all expert execution paths require `actor_id`; journey `agent.role` aliases resolve to concrete `expert_type` keys package-first.

### Why This Baseline
- Preserves protobuf-first contracts and Entity Server mutation invariants while avoiding greenfield reimplementation.
- Improves testability with explicit adapter boundaries and typed outputs.
- Reduces vendor lock-in by keeping orchestration, vector stores, and prompt telemetry swappable behind internal interfaces.
- Supports near-term delivery with mature Python ecosystem components aligned to existing docs and configuration model.

### Dependency Policy
- Pin direct runtime dependencies and maintain a compatibility matrix per subsystem.
- Treat adapter interfaces as stable internal contracts; library upgrades cannot change domain-service semantics.
- Keep prompt text in-repo as source of truth; external prompt telemetry/versioning is additive.
- Require CI checks for:
  - structured-output conformance,
  - prompt regression coverage,
  - backend parity behavior,
  - interface parity across gRPC, FastAPI, and MCP.

### Upgrade and Drift Policy
- Library replacements or major behavior changes require ADR update and compatibility plan.
- Maintain scheduled dependency review cadence with explicit risk notes for LLM, MCP, and retrieval libraries.
- Do not auto-adopt pre-release or unstable major versions in production paths.
- Validate upgrade candidates against conformance, regression, and parity suites before adoption.

### Important API / Interface / Type Additions
1. `LLMStructuredClient.generate(...) -> TypedResult`
2. `PromptRegistry.resolve/render/record_usage(...)`
3. `RAGPipelineExecutor.run(workflow_id, query, context_entity_id, backend_hint)`
4. `VectorStoreAdapter` with standard operations for ingest/search/filter.
5. `ExpertAnalysisRequest` and MCP expert tools require `actor_id` and selector contract (`expert_type` or `requested_role`) with resolved expert metadata.
6. Response metadata additions for observability and testability:
   - `schema_validated`
   - `prompt_version`
   - `trace_id`
   - `backend_used`
   - `requested_role`
   - `resolved_expert_type`
   - `resolution_source`

### Test Cases and Scenarios
1. Structured-output conformance tests:
   - valid response;
   - malformed response with retry;
   - deterministic failure after retry exhaustion.
2. Prompt regression tests (promptfoo):
   - baseline fixtures for three critical journeys;
   - drift threshold checks.
3. Backend parity tests:
   - Chroma and Qdrant satisfy the same response schema and required ranking metadata.
4. Interface parity tests:
   - gRPC, FastAPI, and MCP return equivalent semantics for the same operations.
5. Non-bypass invariant tests:
   - MCP/API calls cannot bypass Entity Server mutation boundary.
6. Actor/expert contract tests:
   - journey `agent.role` resolves to package-local expert before core fallback;
   - expert analysis requests without `actor_id` are rejected.

### Assumptions and Defaults
1. Protobuf/gRPC remains the canonical contract architecture.
2. File-first canonical persistence and config-path ADRs remain unchanged.
3. Library choices are default baseline, not permanent exclusivity; replacements require ADR update.
4. Prompt files remain in-repo source of truth even when runtime telemetry/versioning is externalized.
5. Production deployments may vary by environment, but adapter interfaces remain stable.
