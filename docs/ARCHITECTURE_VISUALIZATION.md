# SemOps2 Architecture Visualization

This document provides a high-level visual overview of the SemOps2 architecture using Mermaid diagrams. It illustrates the interaction between the core components and shows the flow for key operations like entity creation and AI-driven analysis.

## Component Overview

This diagram shows the main architectural components with the enforced entity server as the central authority.

```mermaid
graph TD
    subgraph "Client Interfaces"
        CLI["CLI Client"]
        API["REST API Client"]
        MCP["MCP Client"]
        WebUI["Web UI Client"]
    end

    subgraph "Entity Server (Enforced)"
        EntityServer["🔒 Entity Server"]
        EntityValidation["Entity Validation"]
        EntityConstraints["Entity Constraints"]
        EntityMeta["Entity Metadata"]
    end

    subgraph "Core Services"
        EntityService["EntityService"]
        ContextDetector["ContextDetector"]
        ConfigManager["ConfigManager"]
        TemplateEngine["TemplateEngine"]
    end

    subgraph "AI Subsystem"
        WorkflowEngine["WorkflowEngine"]
        ExpertPromptGenerator["ExpertPromptGenerator"]
        LLM["LLM API"]
    end

    subgraph "Knowledge Subsystem"
        KnowledgeService["KnowledgeService"]
        VectorStore["Vector Store (ChromaDB)"]
        FileSystem["File System (Markdown Files)"]
    end

    subgraph "Configuration & Schema"
        ProtoSchema["Protocol Buffer Schema"]
        EntityTypeConfig["entity_types.yaml"]
        ExpertConfig["experts.yaml"]
        WorkflowConfig["workflows.yaml"]
        Templates["*.md.j2 Templates"]
    end

    %% All clients must go through Entity Server
    CLI --> EntityServer
    API --> EntityServer
    MCP --> EntityServer
    WebUI --> EntityServer

    %% Entity Server enforces validation
    EntityServer --> EntityValidation
    EntityServer --> EntityConstraints
    EntityServer --> EntityMeta
    EntityServer --> ProtoSchema

    %% Entity Server coordinates with services
    EntityServer --> EntityService
    EntityService --> ConfigManager
    EntityService --> ContextDetector
    EntityService --> TemplateEngine
    EntityService --> WorkflowEngine
    EntityService --> KnowledgeService
    EntityService --> FileSystem

    %% Configuration relationships
    ConfigManager --> EntityTypeConfig
    ConfigManager --> ExpertConfig
    ConfigManager --> WorkflowConfig
    ProtoSchema --> EntityValidation

    %% Template and context relationships
    TemplateEngine --> Templates
    ContextDetector --> FileSystem

    %% AI workflow relationships
    WorkflowEngine --> ExpertPromptGenerator
    ExpertPromptGenerator --> LLM
    ExpertPromptGenerator --> KnowledgeService

    %% Knowledge system relationships
    KnowledgeService --> VectorStore
    KnowledgeService --> FileSystem

    classDef enforced fill:#ff6b6b,stroke:#d63031,stroke-width:3px,color:#fff
    class EntityServer,EntityValidation,EntityConstraints,EntityMeta enforced
```

## Operational Flows

These diagrams illustrate the sequence of interactions for specific commands.

### Flow 1: `semops domain create` (Enforced Entity Server)

This shows entity creation through the enforced entity server with validation and constraints.

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant EntityServer
    participant EntityValidation
    participant EntityService
    participant ConfigManager
    participant TemplateEngine
    participant FileSystem

    User->>CLI: semops domain create --name "New Domain"
    CLI->>EntityServer: CreateEntity(type="domain", name="New Domain")

    Note over EntityServer: Enforcement Layer
    EntityServer->>EntityValidation: validate_entity_request(domain_create_req)
    EntityValidation->>EntityValidation: Check protobuf constraints
    EntityValidation->>EntityValidation: Validate entity metadata
    EntityValidation-->>EntityServer: Validation result

    alt Validation successful
        EntityServer->>EntityService: create("domain", validated_data)
        EntityService->>ConfigManager: get_entity_config("domain")
        ConfigManager-->>EntityService: Return domain config
        EntityService->>TemplateEngine: render("domain.md.j2", ...)
        TemplateEngine-->>EntityService: Return rendered markdown
        EntityService->>FileSystem: Write domain/new-domain/domain.md
        FileSystem-->>EntityService: Success
        EntityService-->>EntityServer: Return new entity metadata
        EntityServer-->>CLI: Return validated entity response
        CLI-->>User: Display success message
    else Validation failed
        EntityServer-->>CLI: Return validation errors
        CLI-->>User: Display validation errors
    end
```

### Flow 2: `semops domain analyze --workflow ...` (Enforced Updates)

This shows AI-driven analysis with enforced entity updates through the entity server.

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant EntityServer
    participant EntityValidation
    participant EntityService
    participant WorkflowEngine
    participant ExpertPromptGenerator
    participant KnowledgeService
    participant LLM

    User->>CLI: semops domain analyze --workflow my_workflow
    CLI->>EntityServer: AnalyzeEntity(entity_id, workflow="my_workflow")

    Note over EntityServer: Validate Analysis Request
    EntityServer->>EntityValidation: validate_analyze_request()
    EntityValidation-->>EntityServer: Request validated

    EntityServer->>EntityService: analyze(workflow="my_workflow")
    EntityService->>WorkflowEngine: execute("my_workflow", context)

    loop For each step in workflow
        WorkflowEngine->>ExpertPromptGenerator: generate(expert, task, context)
        ExpertPromptGenerator->>KnowledgeService: retrieve_context(query)
        KnowledgeService-->>ExpertPromptGenerator: Return relevant sources
        ExpertPromptGenerator->>LLM: Execute prompt
        LLM-->>ExpertPromptGenerator: Return AI-generated content
        ExpertPromptGenerator-->>WorkflowEngine: Return structured result

        Note over WorkflowEngine,EntityServer: Enforce Updates
        WorkflowEngine->>EntityServer: UpdateEntity(entity_id, new_content)
        EntityServer->>EntityValidation: validate_entity_update()
        EntityValidation-->>EntityServer: Update validated
        EntityServer->>EntityService: update(entity_id, validated_content)
        EntityService-->>EntityServer: Update success
        EntityServer-->>WorkflowEngine: Update confirmed
    end

    EntityService-->>EntityServer: Analysis complete
    EntityServer-->>CLI: Return analysis results
    CLI-->>User: Display success message
```

### Flow 3: API/MCP `create` Request (Enforced Entity Server)

This shows how external clients interact through the enforced entity server with unified validation.

```mermaid
sequenceDiagram
    participant Client [API/MCP Client]
    participant API [REST API / MCP Server]
    participant EntityServer
    participant EntityValidation
    participant EntityService
    participant ConfigManager
    participant TemplateEngine
    participant FileSystem

    Client->>API: POST /domains/{domain_id}/problems (body: {name: "New Problem"})
    API->>EntityServer: CreateEntity(gRPC: CreateProblemRequest)

    Note over EntityServer: Universal Enforcement
    EntityServer->>EntityValidation: validate_protobuf_request()
    EntityValidation->>EntityValidation: Check field constraints (buf.validate)
    EntityValidation->>EntityValidation: Validate entity hierarchy
    EntityValidation->>EntityValidation: Check business rules
    EntityValidation-->>EntityServer: Validation result

    alt Validation successful
        EntityServer->>EntityService: create("problem", validated_data)
        EntityService->>ConfigManager: get_entity_config("problem")
        ConfigManager-->>EntityService: Return problem config
        EntityService->>TemplateEngine: render("problem.md.j2", ...)
        TemplateEngine-->>EntityService: Return rendered markdown
        EntityService->>FileSystem: Write domain/{domain_slug}/problems/new-problem/problem.md
        FileSystem-->>EntityService: Success
        EntityService-->>EntityServer: Return entity metadata
        EntityServer-->>API: Return CreateProblemResponse (gRPC)
        API-->>Client: 201 Created (JSON response)
    else Validation failed
        EntityServer-->>API: Return validation errors (gRPC)
        API-->>Client: 400 Bad Request (JSON errors)
    end
```

## Enforced Entity Server Benefits

The enforced entity server architecture provides several key advantages:

### 🔒 Unified Validation
- **Protocol Buffer Schema Enforcement**: All entities must conform to protobuf definitions with buf.validate constraints
- **Business Rule Validation**: Centralized enforcement of entity relationships and constraints
- **Field-Level Validation**: Automatic validation of entity metadata, IDs, hierarchies, and custom fields

### 🚀 Multi-Client Support
- **Universal Interface**: CLI, REST API, MCP, and Web UI all use the same validation logic
- **Consistent Behavior**: Identical entity handling across all client interfaces
- **Type Safety**: Protocol buffer definitions ensure type safety across language boundaries

### 📊 Centralized Authority
- **Single Source of Truth**: All entity operations go through the entity server
- **Audit Trail**: Complete tracking of entity creation, updates, and analysis operations
- **Security Enforcement**: Centralized access control and permission validation

### 🔄 Workflow Integration
- **AI Workflow Validation**: Even AI-generated content must pass through entity validation
- **Update Consistency**: All entity updates, whether manual or AI-driven, follow the same validation rules
- **Rollback Safety**: Failed validations prevent inconsistent states

### 🛠️ Development Benefits
- **Schema Evolution**: Protocol buffer schema allows for backward-compatible changes
- **Code Generation**: Automatic client code generation for multiple languages
- **Documentation**: OpenAPI and markdown docs generated from schema
- **Testing**: Consistent validation logic enables comprehensive testing
