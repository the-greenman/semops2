# Interface Definition Language Architecture - Protobuf-First Design

## Overview

SemOps2 uses a protobuf-first approach to eliminate interface drift and ensure perfect consistency across all access methods (CLI, REST API, GraphQL, MCP). All interfaces, data structures, and validation rules are generated from authoritative protobuf schemas, creating a single source of truth for the entire system.

Scope note: this document defines the SemOps2 IDL target architecture. SemOps v1 references are historical rationale only and are not in-scope runtime behavior.

## Legacy Problem Context: Interface Drift in SemOps v1

### Historical Issues
```python
# Different ID formats across interfaces
cli_id = "DOM-vmware-modernisation"     # CLI inconsistent kebab-case
api_id = "DOM-VmwareModernisation"      # API uses PascalCase
mcp_id = "vmware-modernisation"         # MCP uses kebab-case
file_id = "domain/vmware_modernisation" # File system uses underscores
```

### Inconsistent Data Structures
- CLI returns dict with snake_case keys
- REST API returns camelCase JSON
- MCP tools use different field names
- GraphQL has its own naming conventions

### Manual Interface Maintenance
- Multiple interface definitions to keep in sync
- Breaking changes not detected until runtime
- Client libraries manually maintained
- Validation rules duplicated across systems

## SemOps2 Solution: Protobuf-First IDL

### Single Source of Truth Architecture

```
┌─────────────────────────────────┐
│        Master Protobuf         │
│         Schemas (.proto)        │
│                                 │
│  ┌─────────────────────────┐   │
│  │     core.proto          │   │
│  │   - EntityID format     │   │
│  │   - Base entity types   │   │
│  │   - Common enums        │   │
│  └─────────────────────────┘   │
│                                 │
│  ┌─────────────────────────┐   │
│  │   services.proto        │   │
│  │   - All service APIs    │   │
│  │   - Request/Response    │   │
│  │   - Error definitions   │   │
│  └─────────────────────────┘   │
└─────────────────────────────────┘
                 │
                 ▼
         ┌───────────────┐
         │  buf generate │
         └───────────────┘
                 │
    ┌────────────┼────────────┐
    ▼            ▼            ▼
┌────────┐  ┌─────────┐  ┌────────┐
│ Python │  │OpenAPI  │  │GraphQL │
│ gRPC   │  │ Specs   │  │Schema  │
│        │  │         │  │        │
│CLI     │  │REST API │  │Web UI  │
│Internal│  │MCP Tools│  │Queries │
└────────┘  └─────────┘  └────────┘
```

## Core Schema Design

### Master Entity ID Definition

The `EntityID` message uses a **namespace model** to support third-party entity type contributions without ID collisions. Two different packages can both define a `decision` type because each lives under a distinct namespace.

```protobuf
// schema/semops/v1/core.proto
syntax = "proto3";
package semops.v1;

import "buf/validate/validate.proto";
import "google/protobuf/timestamp.proto";
import "google/protobuf/struct.proto";

// Standardized EntityID - enforces format everywhere
message EntityID {
  // Reverse-DNS namespace owning this type, e.g. "semops.core" or "com.acme"
  string namespace = 1;

  // Short prefix, unique within the namespace, e.g. "DEC"
  string prefix = 2 [(buf.validate.field).string.pattern = "^[A-Z]{2,6}$"];

  // Fully-qualified type key: "{namespace}/{type_key}", e.g. "semops.core/decision"
  // NOT a closed enum — valid values are determined by the loaded configuration.
  string entity_type = 3 [(buf.validate.field).string.min_len = 1];

  // URL-safe slug for file system and web usage (kebab-case)
  string slug = 4 [(buf.validate.field).string.pattern = "^[a-z0-9-]+$"];

  // Computed display ID: "{prefix}-{slug}", e.g. "DEC-budget-2026"
  // Unique within a namespace. Globally unique when combined with namespace.
  string id = 5;

  // File-system context path
  string domain_path = 6;
}

// Base entity structure
message EntityMeta {
  EntityID entity_id = 1;
  string name = 2 [(buf.validate.field).string.min_len = 1];
  string description = 3;
  google.protobuf.Struct metadata = 4;
  google.protobuf.Timestamp created_at = 5;
  google.protobuf.Timestamp updated_at = 6;
  repeated string tags = 7;
  EntityStatus status = 8;
  string template_version = 9;
  float weight = 10 [(buf.validate.field).float = {gte: 0.0, lte: 1.0}];
}

enum EntityStatus {
  ENTITY_STATUS_UNSPECIFIED = 0;
  ENTITY_STATUS_DRAFT = 1;
  ENTITY_STATUS_ACTIVE = 2;
  ENTITY_STATUS_ARCHIVED = 3;
  ENTITY_STATUS_DELETED = 4;
}
```

**Why not a closed enum for `entity_type`?** Protobuf enums are schema-level constructs that require a schema change and regeneration to add a new value. Since entity types are defined in YAML configuration and must be extensible by third parties without modifying the schema, `entity_type` carries the fully-qualified string key (`semops.core/decision`) and validation against valid types happens in the `ConfigManager` at runtime, not in the protobuf layer.

### Actor and Governance Control-Plane Schema (Planned)

Semantic operations require actor identity, boundary decisions, and mutation audit events as first-class protobuf messages. These are control-plane contracts and are not modeled as generic content frontmatter.

```protobuf
// schema/semops/v1/governance.proto (planned)
syntax = "proto3";
package semops.v1;

import "buf/validate/validate.proto";
import "google/protobuf/struct.proto";
import "google/protobuf/timestamp.proto";
import "semops/v1/core.proto";

// Actor identity used by humans, software, services, and future actor types.
message Actor {
  // Stable actor identifier, e.g. "ACT-assistant-007"
  string actor_id = 1 [(buf.validate.field).string.pattern = "^ACT-[a-z0-9-]+$"];

  // Open string for extensibility; examples: "human", "software", "service", "posthuman"
  string actor_type = 2 [(buf.validate.field).string.min_len = 1];

  // Human-readable name
  string display_name = 3 [(buf.validate.field).string.min_len = 1];

  // Role links (ROLE-*) used by policy and approval logic
  repeated string role_bindings = 4;

  // Declared capabilities, evaluated by policy engine at runtime
  repeated string capabilities = 5;

  // Organization-defined authority tier (e.g., LOW, MEDIUM, HIGH)
  string authority_level = 6;

  ActorStatus status = 7;
  google.protobuf.Timestamp created_at = 8;
  google.protobuf.Timestamp updated_at = 9;

  // Extensible metadata (identity provider refs, labels, external IDs, etc.)
  google.protobuf.Struct metadata = 10;
}

enum ActorStatus {
  ACTOR_STATUS_UNSPECIFIED = 0;
  ACTOR_STATUS_ACTIVE = 1;
  ACTOR_STATUS_SUSPENDED = 2;
  ACTOR_STATUS_RETIRED = 3;
}

// Request to evaluate whether an actor can perform an action in context.
message PermissionDecisionRequest {
  string actor_id = 1 [(buf.validate.field).string.pattern = "^ACT-[a-z0-9-]+$"];
  string proposed_action = 2 [(buf.validate.field).string.min_len = 1];
  google.protobuf.Struct action_context = 3;
}

// Policy evaluation result with traceable reasoning.
message PermissionDecision {
  string decision_id = 1;
  string actor_id = 2;
  string proposed_action = 3;
  PermissionResult result = 4;

  // Policy/constitution/decision references that justify outcome.
  repeated string policy_references = 5;
  repeated string approver_roles = 6;

  string rationale = 7;
  google.protobuf.Timestamp evaluated_at = 8;
  string evaluator_version = 9; // ruleset hash/version
}

enum PermissionResult {
  PERMISSION_RESULT_UNSPECIFIED = 0;
  PERMISSION_RESULT_ALLOWED = 1;
  PERMISSION_RESULT_NEEDS_APPROVAL = 2;
  PERMISSION_RESULT_FORBIDDEN = 3;
}

// Immutable audit event for any state mutation.
message MutationAuditEvent {
  string event_id = 1;
  string actor_id = 2;
  string mutation_type = 3; // create_entity, update_entity, add_relationship, migrate_template, etc.

  EntityID target_entity_id = 4;
  string change_reason = 5;
  string authority_basis = 6; // constitutional/policy/decision citation

  // Optional workflow traceability.
  string journey_id = 7;
  string journey_stage = 8;
  string review_id = 9;

  // Hybrid persistence integrity tracking.
  string document_revision_id = 10;
  SyncStatus graph_sync_status = 11;
  SyncStatus vector_sync_status = 12;
  string reconciliation_run_id = 13;

  google.protobuf.Timestamp occurred_at = 14;
  google.protobuf.Struct metadata = 15;
}

enum SyncStatus {
  SYNC_STATUS_UNSPECIFIED = 0;
  SYNC_STATUS_PENDING = 1;
  SYNC_STATUS_COMPLETED = 2;
  SYNC_STATUS_FAILED = 3;
}

// Aggregated proposal/ADR composed of multiple fine-grained decisions.
message DecisionBundle {
  string bundle_id = 1; // e.g. ADR-hybrid-architecture-q1
  string bundle_type = 2; // e.g. "adr", "proposal"
  string title = 3;
  repeated string decision_ids = 4; // ordered list of constituent DEC-* items
  string status = 5; // draft | approved | superseded
  string rationale_summary = 6;
  google.protobuf.Timestamp created_at = 7;
  google.protobuf.Timestamp updated_at = 8;
}

// Link between a decision and a concrete document change-set reference.
message DecisionChangeLink {
  string link_id = 1;
  string decision_id = 2; // DEC-*
  EntityID target_entity_id = 3; // CONST-*, POL-*, etc.
  string change_ref = 4; // CHG-* identifier from a diff/change-set registry
  string change_summary = 5;
  google.protobuf.Timestamp linked_at = 6;
}
```

Control-plane enforcement policy (planned):
- Normal mutating requests require actor attribution in metadata (`created_by_actor_id` / `updated_by_actor_id`).
- `ACT-system` is allowed only for explicit system-classified operations (bootstrap/import/migration/recovery).
- Unknown attribution is treated as governance debt and must be reconciled via audit workflow.

### Entity Document (File-Based View)

Rather than defining message types per entity (which would require a schema change for every new entity type), SemOps2 uses a single generic `EntityDocument` that represents the file-based view of any entity. Entity-specific fields live in `frontmatter` as a free-form `Struct`.

```protobuf
// schema/semops/v1/entities.proto
syntax = "proto3";
package semops.v1;

import "google/protobuf/struct.proto";
import "google/protobuf/timestamp.proto";
import "semops/v1/core.proto";

// Generic file-based entity representation.
// Works for any entity type (domain, decision, meeting, role, artefact, etc.)
// without requiring schema changes when new types are introduced.
message EntityDocument {
  // Fully-qualified entity ID including namespace
  EntityID entity_id = 1;

  // Parsed YAML frontmatter — entity-specific fields live here
  google.protobuf.Struct frontmatter = 2;

  // Markdown content body
  string content = 3;

  // File system metadata
  string file_path = 4;
  google.protobuf.Timestamp file_modified_at = 5;

  // Which template bundle entry was used to create this document
  string template_name = 6;
  string template_version = 7;
}
```

### Expert System Schema

Expert types are **configuration-driven**, not a closed protobuf enum. The `expert_type` field carries a string key that maps to an entry in `experts.yaml`. This follows the same extensibility principle as `entity_type`: new expert personas are added via config, not schema changes. Journey `agent.role` values are runtime aliases that must resolve to `expert_type` keys before expert calls are executed.
Normative contract decision: [ADR-0003](./decisions/ADR-0003-actor-expert-invocation-contract.md).

```protobuf
// schema/semops/v1/experts.proto (planned)
syntax = "proto3";
package semops.v1;

import "buf/validate/validate.proto";
import "google/protobuf/struct.proto";
import "google/protobuf/timestamp.proto";
import "semops/v1/core.proto";

// Expert analysis request.
// workflow is a config-defined string key, e.g. "basic_analysis" or "decision-rationale-review".
// Selector contract:
// - pass expert_type for explicit expert key execution, OR
// - pass requested_role for alias-based package-first resolution.
message ExpertAnalysisRequest {
  EntityID entity_id = 1;
  string expert_type = 2;
  string workflow = 3;
  google.protobuf.Struct parameters = 4;
  bool auto_save = 5;
  string actor_id = 6 [(buf.validate.field).string.pattern = "^ACT-[a-z0-9-]+$"];
  string requested_role = 7;
}

// Resolution metadata captured for auditability.
message ExpertResolutionMetadata {
  string requested_role = 1;       // Empty when expert_type provided directly
  string resolved_expert_type = 2; // Final config key used by runtime
  string resolution_source = 3;    // package | core | builtin
  string resolver_version = 4;     // Resolver implementation/config version
  repeated string resolution_path = 5; // Catalogs inspected in order
}

// Expert analysis response
message ExpertAnalysisResponse {
  string analysis_id = 1;
  string expert_type = 2;
  EntityID entity_id = 3;
  string analysis_content = 4;
  float confidence_score = 5;
  repeated KnowledgeSourceRef sources_used = 6;
  string workflow_used = 7;
  google.protobuf.Timestamp generated_at = 8;
  AnalysisStatus status = 9;
  ExpertResolutionMetadata resolution = 10;
  bool schema_validated = 11;
  string prompt_version = 12;
  string trace_id = 13;
  string backend_used = 14;
}

enum AnalysisStatus {
  ANALYSIS_STATUS_UNSPECIFIED = 0;
  ANALYSIS_STATUS_IN_PROGRESS = 1;
  ANALYSIS_STATUS_COMPLETED = 2;
  ANALYSIS_STATUS_FAILED = 3;
}
```

Validation semantics (service-enforced):

- `actor_id` is required.
- At least one selector must be provided: `expert_type` or `requested_role`.
- If both are provided, service either rejects the request or requires explicit policy allowing override mode.

### Knowledge Repository Schema

```protobuf
// semops/schema/v1/knowledge.proto
syntax = "proto3";
package semops.v1;

import "semops/schema/v1/core.proto";

// Knowledge source types are configuration-driven (open string keys),
// e.g. "web_content", "documents", "api_feeds".
// Valid values are resolved from runtime config, not a closed protobuf enum.

// Knowledge source definition
message KnowledgeSource {
  string source_id = 1;
  string source_type = 2;
  string name = 3;
  string url = 4;
  google.protobuf.Struct config = 5;
  EntityID domain_id = 6;
  ProcessingStatus processing_status = 7;
  google.protobuf.Timestamp created_at = 8;
  google.protobuf.Timestamp last_processed = 9;
}

enum ProcessingStatus {
  PROCESSING_STATUS_UNSPECIFIED = 0;
  PROCESSING_STATUS_PENDING = 1;
  PROCESSING_STATUS_PROCESSING = 2;
  PROCESSING_STATUS_COMPLETED = 3;
  PROCESSING_STATUS_FAILED = 4;
}

// RAG retrieval request
message RetrievalRequest {
  string query = 1 [(validate.rules).string.min_len = 1];
  EntityID context_entity_id = 2; // Optional context
  string expert_type = 3; // Optional expert context (config-defined key)
  string workflow = 4; // RAG workflow to use
  int32 max_results = 5 [(validate.rules).int32 = {gte: 1, lte: 100}];
  repeated string source_types = 6;
  google.protobuf.Struct parameters = 7;
}

// RAG retrieval response
message RetrievalResponse {
  repeated KnowledgeResult results = 1;
  string workflow_used = 2;
  float total_confidence = 3;
  google.protobuf.Timestamp retrieved_at = 4;
  RetrievalMetrics metrics = 5;
}

message KnowledgeResult {
  string content = 1;
  string source_id = 2;
  string source_type = 3;
  float relevance_score = 4;
  google.protobuf.Struct metadata = 5;
  string citation_format = 6; // e.g., "[[SRC-Title-hash]]"
}

// Source reference for citations
message KnowledgeSourceRef {
  string source_id = 1;
  string source_type = 2;
  string citation = 3;
  string url = 4;
}
```

### Explore Read-Model Schema (Planned)

Browsing should be first-class without requiring export. The explore schema provides read-only projections for humans and AI-mediated interfaces.

```protobuf
// schema/semops/v1/explore.proto (planned)
syntax = "proto3";
package semops.v1;

import "buf/validate/validate.proto";
import "google/protobuf/timestamp.proto";
import "semops/v1/core.proto";

message ExploreSelector {
  // Optional scope constraints
  repeated string entity_types = 1;   // e.g. "semops.core/domain"
  repeated string domain_ids = 2;     // e.g. "DOM-governance"
  repeated string statuses = 3;       // e.g. "active", "draft"
  repeated string authority_levels = 4;
}

message EntitySummary {
  EntityID entity_id = 1;
  string name = 2;
  string status = 3;
  string authority_level = 4;
  string last_change_summary = 5;
  google.protobuf.Timestamp updated_at = 6;
}

message BrowseOverviewRequest {
  string actor_id = 1 [(buf.validate.field).string.pattern = "^ACT-[a-z0-9-]+$"];
  ExploreSelector selector = 2;
  bool include_pending_reviews = 3;
  bool include_recent_changes = 4;
}

message BrowseOverviewResponse {
  string workspace_name = 1;
  string mission_summary = 2;
  EntityID constitution_id = 3;
  string constitution_state = 4;
  repeated EntitySummary active_domains = 5;
  repeated EntitySummary pending_reviews = 6;
  repeated TimelineItem recent_changes = 7;
}

message GetEntityViewRequest {
  EntityID entity_id = 1;
  string actor_id = 2 [(buf.validate.field).string.pattern = "^ACT-[a-z0-9-]+$"];
}

message EntityView {
  EntitySummary summary = 1;
  string purpose = 2;
  string rationale = 3;
  repeated string policy_references = 4;
  repeated EntityID related_entities = 5;
  string current_journey_state = 6;
}

message GetEntityViewResponse {
  EntityView entity = 1;
}

message EntityNeighborhoodRequest {
  EntityID center_entity_id = 1;
  int32 depth = 2 [(buf.validate.field).int32 = {gte: 1, lte: 3}];
  repeated string relationship_types = 3;
  int32 max_nodes = 4 [(buf.validate.field).int32 = {gte: 1, lte: 500}];
}

message RelationshipEdge {
  EntityID from_entity_id = 1;
  EntityID to_entity_id = 2;
  string relationship_type = 3;
}

message EntityNeighborhoodResponse {
  EntitySummary center = 1;
  repeated EntitySummary nodes = 2;
  repeated RelationshipEdge edges = 3;
}

message TimelineRequest {
  ExploreSelector selector = 1;
  google.protobuf.Timestamp since = 2;
  google.protobuf.Timestamp until = 3;
  int32 max_results = 4 [(buf.validate.field).int32 = {gte: 1, lte: 1000}];
}

message TimelineItem {
  string event_id = 1;
  string actor_id = 2;
  string mutation_type = 3;
  EntityID target_entity_id = 4;
  string summary = 5;
  google.protobuf.Timestamp occurred_at = 6;
}

message TimelineResponse {
  repeated TimelineItem items = 1;
}

message ListOpenQuestionsRequest {
  ExploreSelector selector = 1;
  int32 max_results = 2 [(buf.validate.field).int32 = {gte: 1, lte: 200}];
}

message OpenQuestion {
  string question_id = 1;
  string text = 2;
  EntityID source_entity_id = 3;
  string status = 4;   // open | resolved
  string priority = 5; // low | medium | high
}

message ListOpenQuestionsResponse {
  repeated OpenQuestion questions = 1;
}
```

### Service Interface Definitions

```protobuf
// semops/schema/v1/services.proto
syntax = "proto3";
package semops.v1;

import "semops/schema/v1/core.proto";
import "semops/schema/v1/entities.proto";
import "semops/schema/v1/experts.proto";
import "semops/schema/v1/explore.proto";
import "semops/schema/v1/governance.proto";
import "semops/schema/v1/knowledge.proto";

// Generic entity service - works for all entity types
service EntityService {
  // Core CRUD operations
  rpc ListEntities(ListEntitiesRequest) returns (ListEntitiesResponse);
  rpc GetEntity(GetEntityRequest) returns (GetEntityResponse);
  rpc CreateEntity(CreateEntityRequest) returns (CreateEntityResponse);
  rpc UpdateEntity(UpdateEntityRequest) returns (UpdateEntityResponse);
  rpc DeleteEntity(DeleteEntityRequest) returns (DeleteEntityResponse);

  // Analysis operations
  rpc AnalyzeEntity(AnalyzeEntityRequest) returns (AnalyzeEntityResponse);
  rpc GetEntityInfo(GetEntityInfoRequest) returns (GetEntityInfoResponse);
  rpc ValidateEntity(ValidateEntityRequest) returns (ValidateEntityResponse);

  // Context operations
  rpc DetectContext(DetectContextRequest) returns (DetectContextResponse);
  rpc GetEntityRelationships(GetRelationshipsRequest) returns (GetRelationshipsResponse);
}

// Expert analysis service
service ExpertService {
  rpc GetExpertAnalysis(ExpertAnalysisRequest) returns (ExpertAnalysisResponse);
  rpc ListAvailableExperts(ListExpertsRequest) returns (ListExpertsResponse);
  rpc RunMultiExpertWorkflow(WorkflowRequest) returns (WorkflowResponse);
  rpc GetExpertWorkflows(GetWorkflowsRequest) returns (GetWorkflowsResponse);
  rpc SynthesizeExpertAnalyses(SynthesisRequest) returns (SynthesisResponse);
}

// Knowledge repository service
service KnowledgeService {
  rpc AddKnowledgeSource(AddSourceRequest) returns (AddSourceResponse);
  rpc ProcessKnowledgeSource(ProcessSourceRequest) returns (ProcessSourceResponse);
  rpc SearchKnowledge(SearchRequest) returns (SearchResponse);
  rpc RetrieveContext(RetrievalRequest) returns (RetrievalResponse);
  rpc ListKnowledgeSources(ListSourcesRequest) returns (ListSourcesResponse);
  rpc GetSourceStatus(GetSourceStatusRequest) returns (GetSourceStatusResponse);
}

// Context detection service
service ContextService {
  rpc DetectContext(DetectContextRequest) returns (DetectContextResponse);
  rpc ValidateContext(ValidateContextRequest) returns (ValidateContextResponse);
  rpc GetContextPath(GetContextPathRequest) returns (GetContextPathResponse);
}

// Read-only exploration service for browsing without export.
service ExploreService {
  rpc BrowseOverview(BrowseOverviewRequest) returns (BrowseOverviewResponse);
  rpc GetEntityView(GetEntityViewRequest) returns (GetEntityViewResponse);
  rpc GetEntityNeighborhood(EntityNeighborhoodRequest) returns (EntityNeighborhoodResponse);
  rpc GetTimeline(TimelineRequest) returns (TimelineResponse);
  rpc ListOpenQuestions(ListOpenQuestionsRequest) returns (ListOpenQuestionsResponse);
}

// Actor and governance control-plane service
service GovernanceService {
  // Actor identity lifecycle
  rpc RegisterActor(RegisterActorRequest) returns (RegisterActorResponse);
  rpc GetActor(GetActorRequest) returns (GetActorResponse);
  rpc ListActors(ListActorsRequest) returns (ListActorsResponse);

  // Semantic context + boundary checks
  rpc DiscoverOperationalContext(DiscoverOperationalContextRequest) returns (DiscoverOperationalContextResponse);
  rpc EvaluatePermission(PermissionDecisionRequest) returns (PermissionDecision);

  // Evolution + audit
  rpc TraceSystemEvolution(TraceSystemEvolutionRequest) returns (TraceSystemEvolutionResponse);
  rpc ListMutationAuditEvents(ListMutationAuditEventsRequest) returns (ListMutationAuditEventsResponse);

  // Fine-grained ADR/proposal support
  rpc CreateDecisionBundle(CreateDecisionBundleRequest) returns (CreateDecisionBundleResponse);
  rpc GetDecisionBundle(GetDecisionBundleRequest) returns (GetDecisionBundleResponse);
  rpc LinkDecisionToChange(LinkDecisionToChangeRequest) returns (LinkDecisionToChangeResponse);
}
```

## Code Generation Pipeline

### buf.gen.yaml Configuration

```yaml
# buf.gen.yaml - Controls all code generation
version: v1
managed:
  enabled: true
  go_package_prefix:
    default: github.com/semops/semops2/gen/go

plugins:
  # Core gRPC generation
  - plugin: python
    out: src/semops/generated
    opt: grpc_python_out=src/semops/generated

  - plugin: go
    out: gen/go
    opt:
      - paths=source_relative
      - require_unimplemented_servers=false

  - plugin: ts
    out: web/src/generated
    opt: grpc_js,import_style=commonjs

  # API specifications
  - plugin: openapi
    out: api/openapi
    opt: naming=proto,depth=2

  - plugin: jsonschema
    out: api/jsonschema
    opt: disallow_additional_props,enforce_oneof

  # GraphQL schema generation
  - plugin: graphql-schema
    out: api/graphql
    opt: import_prefix=semops.v1

  # Validation generation
  - plugin: validate
    out: src/semops/generated
    opt: lang=python

  # Documentation
  - plugin: doc
    out: docs/api
    opt: html,index.html

  # MCP Server Tool Generation
  - plugin: mcp-tools
    out: src/semops/generated/mcp
    opt:
      - server_name=semops
      - async_handlers=true
      - tool_prefix=semops_
```

### Generated Outputs

**Python gRPC Client:**
```python
# Generated: src/semops/generated/services_pb2_grpc.py
from semops.generated import core_pb2, services_pb2, services_pb2_grpc

# Type-safe client with validation
client = services_pb2_grpc.EntityServiceStub(channel)

# Namespace-scoped EntityID
entity_id = core_pb2.EntityID(
    namespace="semops.core",
    prefix="DEC",
    entity_type="semops.core/decision",
    slug="adopt-zero-trust-model",
    id="DEC-adopt-zero-trust-model",
)

request = services_pb2.GetEntityRequest(entity_id=entity_id)
response = client.GetEntity(request)
```

**OpenAPI Specification:**
```yaml
# Generated: api/openapi/services.yaml
openapi: 3.1.0
info:
  title: SemOps API
  version: 1.0.0

paths:
  /api/v1/entities:
    get:
      summary: List Entities
      parameters:
        - name: entity_type
          in: query
          description: "Fully-qualified type key, e.g. 'semops.core/decision'"
          schema:
            type: string
            minLength: 1
      responses:
        '200':
          description: List of entities
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListEntitiesResponse'

components:
  schemas:
    EntityID:  # Generated from protobuf
      type: object
      required: [namespace, prefix, entity_type, slug, id]
      properties:
        namespace:
          type: string
          description: "Reverse-DNS namespace, e.g. 'semops.core' or 'com.acme'"
        prefix:
          type: string
          pattern: '^[A-Z]{2,6}$'
        entity_type:
          type: string
          description: "Fully-qualified type key: '{namespace}/{type_key}'"
          minLength: 1
        slug:
          type: string
          pattern: '^[a-z0-9-]+$'
        id:
          type: string
          description: "Display ID: '{prefix}-{slug}', e.g. 'DEC-budget-2026'"
```

**GraphQL Schema:**
```graphql
# Generated: api/graphql/schema.graphql
scalar EntityID
scalar DateTime

interface Entity {
  entityId: EntityID!
  name: String!
  description: String
  createdAt: DateTime!
  updatedAt: DateTime!
  status: EntityStatus!
}

type Domain implements Entity {
  entityId: EntityID!
  name: String!
  description: String
  createdAt: DateTime!
  updatedAt: DateTime!
  status: EntityStatus!
  focusAreas: String
  boundariesInScope: String
  boundariesOutOfScope: String
  domainTensions: [String!]!
}

type Query {
  entities(type: String, parentId: EntityID): [Entity!]!
  entity(id: EntityID!): Entity
  expertAnalysis(entityId: EntityID!, expertType: ExpertType!): ExpertAnalysisResponse
}
```

**MCP Tool Definitions:**

MCP tool schemas are generated from the protobuf service definitions. Because `entity_type` and `expert_type` are open strings (not closed enums), the generated schemas use `minLength` constraints rather than `enum` lists. Valid values come from the runtime config, exposed via `semops_list_entity_types` and `semops_list_expert_types` tools.

```python
# Generated: src/semops/generated/mcp/tools.py
SEMOPS_TOOLS = [
    Tool(
        name="semops_browse_overview",
        description="Read-only workspace overview for quick exploration",
        inputSchema={
            "type": "object",
            "properties": {
                "actor_id": {"type": "string"},
                "include_pending_reviews": {"type": "boolean"},
                "include_recent_changes": {"type": "boolean"}
            },
            "required": ["actor_id"]
        }
    ),
    Tool(
        name="semops_list_entities",
        description="List entities of a specific type with optional relationship filtering",
        inputSchema={
            "type": "object",
            "properties": {
                "entity_type": {
                    "type": "string",
                    "minLength": 1,
                    "description": "Fully-qualified type key, e.g. 'semops.core/decision'"
                },
                "related_to": {
                    "type": "string",
                    "description": "Optional: filter to entities related to this ID"
                },
                "relationship_type": {
                    "type": "string",
                    "description": "Optional: relationship type to filter by, e.g. 'semops.core/made_in'"
                }
            },
            "required": ["entity_type"]
        }
    ),
    Tool(
        name="semops_get_entity",
        description="Get a specific entity by its display ID",
        inputSchema={
            "type": "object",
            "properties": {
                "entity_id": {
                    "type": "string",
                    "description": "Display ID, e.g. 'DEC-adopt-zero-trust'"
                },
                "namespace": {
                    "type": "string",
                    "description": "Namespace to disambiguate if multiple types share the same prefix"
                }
            },
            "required": ["entity_id"]
        }
    ),
    Tool(
        name="semops_get_entity_neighborhood",
        description="Read-only graph neighborhood traversal around an entity",
        inputSchema={
            "type": "object",
            "properties": {
                "entity_id": {"type": "string"},
                "depth": {"type": "integer", "minimum": 1, "maximum": 3},
                "relationship_types": {"type": "array", "items": {"type": "string"}},
                "max_nodes": {"type": "integer", "minimum": 1, "maximum": 500}
            },
            "required": ["entity_id"]
        }
    ),
    Tool(
        name="semops_get_timeline",
        description="Read-only timeline of recent system changes",
        inputSchema={
            "type": "object",
            "properties": {
                "since": {"type": "string", "description": "ISO-8601 timestamp"},
                "until": {"type": "string", "description": "ISO-8601 timestamp"},
                "max_results": {"type": "integer", "minimum": 1, "maximum": 1000}
            }
        }
    ),
    Tool(
        name="semops_list_open_questions",
        description="Read-only list of unresolved questions across selected scope",
        inputSchema={
            "type": "object",
            "properties": {
                "entity_types": {"type": "array", "items": {"type": "string"}},
                "domain_ids": {"type": "array", "items": {"type": "string"}},
                "max_results": {"type": "integer", "minimum": 1, "maximum": 200}
            }
        }
    ),
    Tool(
        name="semops_create_entity",
        description="Create a new entity from its template bundle",
        inputSchema={
            "type": "object",
            "properties": {
                "entity_type": {
                    "type": "string",
                    "minLength": 1,
                    "description": "Fully-qualified type key, e.g. 'semops.core/meeting'"
                },
                "name": {"type": "string"},
                "variables": {
                    "type": "object",
                    "description": "Template variables for the create template"
                }
            },
            "required": ["entity_type", "name"]
        }
    ),
    Tool(
        name="semops_expert_analyze",
        description="Run an expert prompt against an entity",
        inputSchema={
            "type": "object",
            "properties": {
                "actor_id": {"type": "string"},
                "entity_id": {"type": "string"},
                "expert_type": {
                    "type": "string",
                    "description": "Config-defined expert key, e.g. 'operations-analyst'"
                },
                "requested_role": {
                    "type": "string",
                    "description": "Journey/agent role alias resolved at runtime"
                },
                "workflow": {
                    "type": "string",
                    "description": "Config-defined workflow key"
                },
                "parameters": {
                    "type": "object",
                    "description": "Optional workflow/expert parameters"
                },
            },
            "required": ["actor_id", "entity_id"],
            "oneOf": [
                {"required": ["expert_type"]},
                {"required": ["requested_role"]}
            ]
        }
    ),
    Tool(
        name="semops_list_entity_types",
        description="List all configured entity types with their namespaces and prefixes",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="semops_list_relationship_types",
        description="List all configured relationship types",
        inputSchema={"type": "object", "properties": {}}
    ),
]

# Auto-generated async handlers wrapping protobuf services
class SemOpsHandler:
    def __init__(self, entity_service: EntityService, expert_service: ExpertService,
                 knowledge_service: KnowledgeService, explore_service: ExploreService):
        self.entity_service = entity_service
        self.expert_service = expert_service
        self.knowledge_service = knowledge_service
        self.explore_service = explore_service

    async def handle_semops_browse_overview(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle browse_overview MCP tool call."""
        request = explore_pb2.BrowseOverviewRequest(
            actor_id=arguments["actor_id"],
            include_pending_reviews=arguments.get("include_pending_reviews", True),
            include_recent_changes=arguments.get("include_recent_changes", True),
        )

        response = await self.explore_service.BrowseOverview(request)

        return [TextContent(
            type="text",
            text=f"""# Workspace Overview

**Workspace**: {response.workspace_name}
**Mission**: {response.mission_summary}
**Constitution**: {response.constitution_id.id} ({response.constitution_state})
**Active Domains**: {len(response.active_domains)}
**Pending Reviews**: {len(response.pending_reviews)}
**Recent Changes**: {len(response.recent_changes)}
"""
        )]

    async def handle_semops_list_entities(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle list_entities MCP tool call."""
        request = services_pb2.ListEntitiesRequest(
            entity_type=arguments["entity_type"],
            parent_id=arguments.get("parent_id")
        )

        response = await self.entity_service.ListEntities(request)

        entities_data = []
        for entity in response.entities:
            entities_data.append({
                "id": entity.entity_id.id,
                "name": entity.name,
                "type": entity.entity_id.entity_type,
                "status": entity.status,
                "created_at": entity.created_at.ToJsonString()
            })

        return [TextContent(
            type="text",
            text=f"Found {len(entities_data)} {arguments['entity_type']} entities:\n" +
                 "\n".join([f"- {e['id']}: {e['name']}" for e in entities_data])
        )]

    async def handle_semops_get_entity(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle get_entity MCP tool call."""
        entity_id = entities_pb2.EntityID(id=arguments["entity_id"])
        request = services_pb2.GetEntityRequest(entity_id=entity_id)

        response = await self.entity_service.GetEntity(request)

        if not response.entity:
            return [TextContent(type="text", text=f"Entity {arguments['entity_id']} not found")]

        entity = response.entity
        return [TextContent(
            type="text",
            text=f"""# {entity.name}

**ID**: {entity.entity_id.id}
**Type**: {entity.entity_id.entity_type}
**Status**: {entity.status}
**Created**: {entity.created_at.ToJsonString()}

## Description
{entity.description}

**Tags**: {', '.join(entity.tags)}
"""
        )]

    async def handle_semops_expert_analyze(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle expert_analyze MCP tool call."""
        entity_id = entities_pb2.EntityID(id=arguments["entity_id"])
        expert_type = arguments.get("expert_type", "")
        requested_role = arguments.get("requested_role", "")
        workflow = arguments.get("workflow", "basic_analysis")

        request = experts_pb2.ExpertAnalysisRequest(
            entity_id=entity_id,
            expert_type=expert_type,
            workflow=workflow,
            parameters=arguments.get("parameters", {}),
            actor_id=arguments["actor_id"],
            requested_role=requested_role,
            auto_save=True
        )

        response = await self.expert_service.GetExpertAnalysis(request)

        return [TextContent(
            type="text",
            text=f"""# Expert Analysis: {response.resolution.resolved_expert_type.replace('_', ' ').title()}

**Analysis ID**: {response.analysis_id}
**Entity**: {arguments['entity_id']}
**Requested Role**: {response.resolution.requested_role}
**Resolved Expert**: {response.resolution.resolved_expert_type}
**Resolution Source**: {response.resolution.resolution_source}
**Confidence**: {response.confidence_score:.2f}
**Workflow**: {response.workflow_used}
**Generated**: {response.generated_at.ToJsonString()}
**Trace ID**: {response.trace_id}

## Analysis Content

{response.analysis_content}

## Sources Used
{chr(10).join([f"- [{src.citation}]({src.url})" for src in response.sources_used])}
"""
        )]

    async def handle_semops_search_knowledge(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle search_knowledge MCP tool call."""
        context_entity_id = None
        if arguments.get("context_entity_id"):
            context_entity_id = entities_pb2.EntityID(id=arguments["context_entity_id"])

        request = knowledge_pb2.RetrievalRequest(
            query=arguments["query"],
            context_entity_id=context_entity_id,
            workflow=arguments.get("workflow", "basic_semantic"),
            max_results=arguments.get("max_results", 10)
        )

        response = await self.knowledge_service.RetrieveContext(request)

        results_text = []
        for result in response.results:
            results_text.append(f"""## {result.source_id} (Score: {result.relevance_score:.2f})
{result.content[:500]}{"..." if len(result.content) > 500 else ""}
""")

        return [TextContent(
            type="text",
            text=f"""# Knowledge Search Results

**Query**: {arguments['query']}
**Workflow**: {response.workflow_used}
**Total Results**: {len(response.results)}
**Confidence**: {response.total_confidence:.2f}

{chr(10).join(results_text)}
"""
        )]
```

**MCP Server Implementation:**
```python
# Generated: src/semops/generated/mcp/server.py
import asyncio
from typing import Any, Sequence
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool

from .tools import SEMOPS_TOOLS, SemOpsHandler
from semops.core import EntityService, ExpertService, KnowledgeService, ExploreService

class SemOpsMCPServer:
    """Auto-generated MCP server for SemOps protobuf services."""

    def __init__(self):
        self.server = Server("semops")
        self.handler = None

    def initialize_services(self, entity_service: EntityService,
                          expert_service: ExpertService,
                          knowledge_service: KnowledgeService,
                          explore_service: ExploreService):
        """Initialize with SemOps service instances."""
        self.handler = SemOpsHandler(entity_service, expert_service, knowledge_service, explore_service)
        self._register_tools()

    def _register_tools(self):
        """Register auto-generated tools and handlers."""

        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            return SEMOPS_TOOLS

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict[str, Any]) -> Sequence[Any]:
            # Route to appropriate handler method
            handler_name = f"handle_{name}"
            if hasattr(self.handler, handler_name):
                handler_method = getattr(self.handler, handler_name)
                return await handler_method(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="semops",
                    server_version="2.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    )
                )
            )

# Usage example
async def main():
    # Initialize SemOps services
    entity_service = EntityService()
    expert_service = ExpertService()
    knowledge_service = KnowledgeService()
    explore_service = ExploreService()

    # Create and run MCP server
    mcp_server = SemOpsMCPServer()
    mcp_server.initialize_services(entity_service, expert_service, knowledge_service, explore_service)

    await mcp_server.run()

if __name__ == "__main__":
    asyncio.run(main())
```

## MCP Integration Architecture

### **1. Automatic Tool Generation**
- MCP tool definitions auto-generated from protobuf service definitions
- Input schemas derived from protobuf message validation rules
- Consistent parameter names and types across all interfaces

### **2. Async Service Wrappers**
- Auto-generated async handlers wrap synchronous protobuf services
- Type-safe conversion between MCP arguments and protobuf messages
- Proper error handling and response formatting

### **3. Zero-Configuration MCP Server**
- Generic MCP server that adapts to any protobuf service definition
- Automatic tool registration and routing
- Standard MCP protocol compliance with stdio transport

### **4. Consistent Error Handling**
- Protobuf validation errors mapped to MCP error responses
- Service exceptions converted to appropriate MCP error types
- Detailed error messages with context information

### **5. Read-Only Exploration Without Export**
- ExploreService provides browse-first read models (overview, neighborhood, timeline, open questions)
- MCP browse tools support AI-mediated exploration and human CLI exploration
- Most discovery workflows operate on small scoped reads instead of full workspace export

## Interface Consistency Benefits

### **1. Perfect ID Format Consistency**
```bash
# Same EntityID structure everywhere, namespace-qualified:
semops decision get DEC-adopt-zero-trust                              # CLI
GET /api/v1/entities/DEC-adopt-zero-trust?ns=semops.core             # REST
query { entity(id: "DEC-adopt-zero-trust", ns: "semops.core") }      # GraphQL
mcp_tool("semops_get_entity", {"entity_id": "DEC-adopt-zero-trust"}) # MCP
```

### **2. Type Safety Across All Interfaces**
- Compile-time validation in Python, TypeScript, Go
- Runtime validation with generated validators
- IDE autocomplete and error detection
- Impossible type mismatches between interfaces

### **3. Automatic Breaking Change Detection**
```bash
# buf breaking detects schema changes
buf breaking --against '.git#branch=main'

# Fails CI/CD if breaking changes detected
# Forces proper schema evolution
```

### **4. Zero Interface Maintenance**
- All client libraries auto-generated from schema
- API documentation auto-generated
- Validation rules defined once, used everywhere
- Schema evolution handled automatically

This protobuf-first approach eliminates the interface drift observed in the SemOps v1 historical architecture, ensuring consistency across access methods with strong type safety and automatic code generation.
