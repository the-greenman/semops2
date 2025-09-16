# Interface Definition Language Architecture - Protobuf-First Design

## Overview

SemOps2 uses a protobuf-first approach to eliminate interface drift and ensure perfect consistency across all access methods (CLI, REST API, GraphQL, MCP). All interfaces, data structures, and validation rules are generated from authoritative protobuf schemas, creating a single source of truth for the entire system.

## Problem: Interface Drift in SemOps v1

### Current Issues
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

```protobuf
// semops/schema/v1/core.proto
syntax = "proto3";
package semops.v1;

import "validate/validate.proto";
import "google/protobuf/timestamp.proto";
import "google/protobuf/struct.proto";

// Standardized EntityID - enforces format everywhere
message EntityID {
  // Primary identifier with strict format validation (kebab-case)
  string id = 1 [(validate.rules).string.pattern = "^[A-Z]{2,5}-[a-z0-9-]+$"];

  // Entity type for routing and validation
  string entity_type = 2 [(validate.rules).string = {
    in: ["domain", "problem", "persona", "product", "solution", "feature", "research"]
  }];

  // URL-safe slug for file system and web usage (kebab-case)
  string slug = 3 [(validate.rules).string.pattern = "^[a-z0-9-]+$"];

  // Domain path context for file operations
  string domain_path = 4;
}

// Base entity structure - all semantic entities inherit this
message Entity {
  EntityID entity_id = 1;
  string name = 2 [(validate.rules).string.min_len = 1];
  string description = 3;
  google.protobuf.Struct metadata = 4;
  google.protobuf.Timestamp created_at = 5;
  google.protobuf.Timestamp updated_at = 6;
  EntityID parent_id = 7; // Optional parent relationship
  repeated string tags = 8;
  EntityStatus status = 9;
  string template_version = 10;
}

enum EntityStatus {
  ENTITY_STATUS_UNSPECIFIED = 0;
  ENTITY_STATUS_DRAFT = 1;
  ENTITY_STATUS_ACTIVE = 2;
  ENTITY_STATUS_ARCHIVED = 3;
}
```

### Specific Entity Definitions

```protobuf
// semops/schema/v1/entities.proto
syntax = "proto3";
package semops.v1;

import "semops/schema/v1/core.proto";

// Domain entity with specific fields
message Domain {
  Entity base = 1;
  string focus_areas = 2;
  string boundaries_in_scope = 3;
  string boundaries_out_of_scope = 4;
  repeated string domain_tensions = 5;
  string key_stakeholders = 6;
  string strategic_context = 7;
}

// Problem entity with domain relationship
message Problem {
  Entity base = 1;
  EntityID domain_id = 2; // Required parent relationship
  string core_problem_summary = 3;
  string trigger_event = 4;
  string current_state = 5;
  string contextual_stakes = 6;
  repeated ProblemPolarity polarities = 7;
  string scope_in_scope = 8;
  string scope_out_of_scope = 9;
}

message ProblemPolarity {
  string name = 1;
  string side_a = 2;
  string side_b = 3;
  string description_a = 4;
  string description_b = 5;
}

// Persona entity with problem relationship
message Persona {
  Entity base = 1;
  EntityID problem_id = 2; // Required parent relationship
  string role = 3;
  string authority_level = 4;
  string decision_influence = 5;
  repeated string pain_points = 6;
  repeated string goals = 7;
  string organizational_context = 8;
}
```

### Expert System Schema

```protobuf
// semops/schema/v1/experts.proto
syntax = "proto3";
package semops.v1;

import "semops/schema/v1/core.proto";

// Expert type definitions
enum ExpertType {
  EXPERT_TYPE_UNSPECIFIED = 0;
  EXPERT_TYPE_STRATEGIC_ANALYST = 1;
  EXPERT_TYPE_PRODUCT_STRATEGIST = 2;
  EXPERT_TYPE_UX_RESEARCHER = 3;
  EXPERT_TYPE_TECHNICAL_ARCHITECT = 4;
  EXPERT_TYPE_MARKET_RESEARCHER = 5;
  EXPERT_TYPE_BUSINESS_DEVELOPMENT = 6;
}

// Expert analysis request
message ExpertAnalysisRequest {
  EntityID entity_id = 1;
  ExpertType expert_type = 2;
  string workflow = 3 [(validate.rules).string = {
    in: ["basic_analysis", "comprehensive_analysis", "multi_expert_workflow"]
  }];
  google.protobuf.Struct parameters = 4;
  bool auto_save = 5;
}

// Expert analysis response
message ExpertAnalysisResponse {
  string analysis_id = 1;
  ExpertType expert_type = 2;
  EntityID entity_id = 3;
  string analysis_content = 4;
  float confidence_score = 5;
  repeated KnowledgeSourceRef sources_used = 6;
  string workflow_used = 7;
  google.protobuf.Timestamp generated_at = 8;
  AnalysisStatus status = 9;
}

enum AnalysisStatus {
  ANALYSIS_STATUS_UNSPECIFIED = 0;
  ANALYSIS_STATUS_IN_PROGRESS = 1;
  ANALYSIS_STATUS_COMPLETED = 2;
  ANALYSIS_STATUS_FAILED = 3;
}
```

### Knowledge Repository Schema

```protobuf
// semops/schema/v1/knowledge.proto
syntax = "proto3";
package semops.v1;

import "semops/schema/v1/core.proto";

// Knowledge source types
enum SourceType {
  SOURCE_TYPE_UNSPECIFIED = 0;
  SOURCE_TYPE_WEB_CONTENT = 1;
  SOURCE_TYPE_DOCUMENTS = 2;
  SOURCE_TYPE_API_FEEDS = 3;
  SOURCE_TYPE_CODE_REPOS = 4;
  SOURCE_TYPE_MEDIA_CONTENT = 5;
  SOURCE_TYPE_INTERNAL_KNOWLEDGE = 6;
  SOURCE_TYPE_REALTIME_FEEDS = 7;
  SOURCE_TYPE_ENTERPRISE_SYSTEMS = 8;
}

// Knowledge source definition
message KnowledgeSource {
  string source_id = 1;
  SourceType source_type = 2;
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
  ExpertType expert_type = 3; // Optional expert context
  string workflow = 4; // RAG workflow to use
  int32 max_results = 5 [(validate.rules).int32 = {gte: 1, lte: 100}];
  repeated SourceType source_types = 6;
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
  SourceType source_type = 3;
  float relevance_score = 4;
  google.protobuf.Struct metadata = 5;
  string citation_format = 6; // e.g., "[[SRC-Title-hash]]"
}

// Source reference for citations
message KnowledgeSourceRef {
  string source_id = 1;
  SourceType source_type = 2;
  string citation = 3;
  string url = 4;
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
from semops.generated import entities_pb2, services_pb2_grpc

# Type-safe client with validation
client = services_pb2_grpc.EntityServiceStub(channel)

# Consistent ID format enforced
entity_id = entities_pb2.EntityID(
    id="DOM-cloud-security",  # Regex validated
    entity_type="domain",
    slug="cloud-security"
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
          schema:
            type: string
            enum: [domain, problem, persona, product]
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
      required: [id, entity_type, slug]
      properties:
        id:
          type: string
          pattern: '^[A-Z]{2,5}-[a-z0-9-]+$'
        entity_type:
          type: string
          enum: [domain, problem, persona, product]
        slug:
          type: string
          pattern: '^[a-z0-9-]+$'
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
```python
# Generated: src/semops/generated/mcp/tools.py
from typing import Dict, Any, List
from mcp.server import Server
from mcp.types import Tool, TextContent
from semops.generated import entities_pb2, services_pb2_grpc

# Auto-generated MCP tools from protobuf service definitions
SEMOPS_TOOLS = [
    Tool(
        name="semops_list_entities",
        description="List entities of a specific type with optional parent filtering",
        inputSchema={
            "type": "object",
            "properties": {
                "entity_type": {
                    "type": "string",
                    "enum": ["domain", "problem", "persona", "product", "solution", "feature", "research"],
                    "description": "Type of entity to list"
                },
                "parent_id": {
                    "type": "string",
                    "pattern": "^[A-Z]{2,5}-[A-Za-z0-9]+$",
                    "description": "Optional parent entity ID to filter by"
                }
            },
            "required": ["entity_type"]
        }
    ),
    Tool(
        name="semops_get_entity",
        description="Get specific entity by ID with full content",
        inputSchema={
            "type": "object",
            "properties": {
                "entity_id": {
                    "type": "string",
                    "pattern": "^[A-Z]{2,5}-[A-Za-z0-9]+$",
                    "description": "Entity ID in format PREFIX-Name"
                }
            },
            "required": ["entity_id"]
        }
    ),
    Tool(
        name="semops_create_entity",
        description="Create new entity from template with provided variables",
        inputSchema={
            "type": "object",
            "properties": {
                "entity_type": {
                    "type": "string",
                    "enum": ["domain", "problem", "persona", "product"],
                    "description": "Type of entity to create"
                },
                "variables": {
                    "type": "object",
                    "description": "Template variables for entity creation"
                }
            },
            "required": ["entity_type", "variables"]
        }
    ),
    Tool(
        name="semops_analyze_entity",
        description="Generate expert analysis for entity using AI agents",
        inputSchema={
            "type": "object",
            "properties": {
                "entity_id": {
                    "type": "string",
                    "pattern": "^[A-Z]{2,5}-[A-Za-z0-9]+$",
                    "description": "Entity ID to analyze"
                },
                "expert_type": {
                    "type": "string",
                    "enum": ["strategic_analyst", "product_strategist", "ux_researcher", "technical_architect"],
                    "description": "Type of expert analysis to perform"
                },
                "workflow": {
                    "type": "string",
                    "enum": ["basic_analysis", "comprehensive_analysis", "multi_expert_workflow"],
                    "description": "Analysis workflow to execute"
                }
            },
            "required": ["entity_id"]
        }
    ),
    Tool(
        name="semops_search_knowledge",
        description="Search knowledge repository using RAG workflows",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "minLength": 1,
                    "description": "Search query"
                },
                "context_entity_id": {
                    "type": "string",
                    "pattern": "^[A-Z]{2,5}-[A-Za-z0-9]+$",
                    "description": "Optional context entity for scoped search"
                },
                "workflow": {
                    "type": "string",
                    "enum": ["basic_semantic", "hybrid_search", "graph_enhanced", "multimodal_search"],
                    "description": "RAG workflow to use"
                },
                "max_results": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "description": "Maximum number of results to return"
                }
            },
            "required": ["query"]
        }
    ),
    Tool(
        name="semops_add_knowledge_source",
        description="Add and process knowledge source for domain",
        inputSchema={
            "type": "object",
            "properties": {
                "source_type": {
                    "type": "string",
                    "enum": ["web_content", "documents", "api_feeds", "code_repos", "media_content"],
                    "description": "Type of knowledge source"
                },
                "source_config": {
                    "type": "object",
                    "description": "Source-specific configuration (URL, credentials, etc.)"
                },
                "domain_id": {
                    "type": "string",
                    "pattern": "^[A-Z]{2,5}-[A-Za-z0-9]+$",
                    "description": "Domain to associate source with"
                }
            },
            "required": ["source_type", "source_config", "domain_id"]
        }
    )
]

# Auto-generated async handlers wrapping protobuf services
class SemOpsHandler:
    def __init__(self, entity_service: EntityService, expert_service: ExpertService,
                 knowledge_service: KnowledgeService):
        self.entity_service = entity_service
        self.expert_service = expert_service
        self.knowledge_service = knowledge_service

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

    async def handle_semops_analyze_entity(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle analyze_entity MCP tool call."""
        entity_id = entities_pb2.EntityID(id=arguments["entity_id"])
        expert_type = arguments.get("expert_type", "strategic_analyst")
        workflow = arguments.get("workflow", "basic_analysis")

        request = experts_pb2.ExpertAnalysisRequest(
            entity_id=entity_id,
            expert_type=getattr(experts_pb2.ExpertType, f"EXPERT_TYPE_{expert_type.upper()}"),
            workflow=workflow,
            auto_save=True
        )

        response = await self.expert_service.GetExpertAnalysis(request)

        return [TextContent(
            type="text",
            text=f"""# Expert Analysis: {expert_type.replace('_', ' ').title()}

**Analysis ID**: {response.analysis_id}
**Entity**: {arguments['entity_id']}
**Confidence**: {response.confidence_score:.2f}
**Workflow**: {response.workflow_used}
**Generated**: {response.generated_at.ToJsonString()}

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
from semops.core import EntityService, ExpertService, KnowledgeService

class SemOpsMCPServer:
    """Auto-generated MCP server for SemOps protobuf services."""

    def __init__(self):
        self.server = Server("semops")
        self.handler = None

    def initialize_services(self, entity_service: EntityService,
                          expert_service: ExpertService,
                          knowledge_service: KnowledgeService):
        """Initialize with SemOps service instances."""
        self.handler = SemOpsHandler(entity_service, expert_service, knowledge_service)
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

    # Create and run MCP server
    mcp_server = SemOpsMCPServer()
    mcp_server.initialize_services(entity_service, expert_service, knowledge_service)

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

## Interface Consistency Benefits

### **1. Perfect ID Format Consistency**
```bash
# Same EntityID structure everywhere:
semops domain get DOM-cloud-security        # CLI
GET /api/v1/entities/DOM-cloud-security     # REST
query { entity(id: "DOM-cloud-security") }  # GraphQL
mcp_tool("get_entity", {"id": "DOM-cloud-security"})  # MCP
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

This protobuf-first approach completely eliminates the interface drift problem that plagued SemOps v1, ensuring perfect consistency across all access methods while providing strong type safety and automatic code generation.