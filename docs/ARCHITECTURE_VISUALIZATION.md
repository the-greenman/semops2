# SemOps2 Architecture Visualization

This document provides a high-level visual overview of the SemOps2 architecture using Mermaid diagrams. It illustrates the interaction between the core components and shows the flow for key operations like entity creation and AI-driven analysis.

## Component Overview

This diagram shows the main architectural components and their primary relationships.

```mermaid
graph TD
    subgraph User/Agent Interface
        CLI
    end

    subgraph CoreServices [Core Services]
        EntityService["Generic EntityService"]
        ContextDetector["ContextDetector"]
        ConfigManager["ConfigManager"]
        TemplateEngine["TemplateEngine"]
    end

    subgraph AISubsystem [AI Subsystem]
        WorkflowEngine["WorkflowEngine"]
        ExpertPromptGenerator["ExpertPromptGenerator"]
        LLM["LLM API"]
    end

    subgraph KnowledgeSubsystem [Knowledge Subsystem]
        KnowledgeService["KnowledgeService"]
        VectorStore["Vector Store (ChromaDB)"]
        FileSystem["File System (Markdown Files)"]
    end

    subgraph Configuration
        direction LR
        EntityTypeConfig["entity_types.yaml"]
        ExpertConfig["experts.yaml"]
        WorkflowConfig["workflows.yaml"]
        Templates["*.md.j2 Templates"]
    end

    %% High-Level Connections
    CLI --> EntityService

    EntityService --> ConfigManager
    EntityService --> ContextDetector
    EntityService --> TemplateEngine
    EntityService --> WorkflowEngine
    EntityService --> KnowledgeService
    EntityService --> FileSystem

    ConfigManager --> EntityTypeConfig
    ConfigManager --> ExpertConfig
    ConfigManager --> WorkflowConfig

    TemplateEngine --> Templates
    ContextDetector --> FileSystem

    WorkflowEngine --> ExpertPromptGenerator
    ExpertPromptGenerator --> LLM
    ExpertPromptGenerator --> KnowledgeService

    KnowledgeService --> VectorStore
    KnowledgeService --> FileSystem
```

## Operational Flows

These diagrams illustrate the sequence of interactions for specific commands.

### Flow 1: `semops domain create`

This shows a simple entity creation workflow without AI-driven content generation.

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant EntityService
    participant ConfigManager
    participant TemplateEngine
    participant FileSystem

    User->>CLI: semops domain create --name "New Domain"
    CLI->>EntityService: create("domain", name="New Domain")
    EntityService->>ConfigManager: get_entity_config("domain")
    ConfigManager-->>EntityService: Return domain config
    EntityService->>TemplateEngine: render("domain.md.j2", ...)
    TemplateEngine-->>EntityService: Return rendered markdown
    EntityService->>FileSystem: Write domain/new-domain/domain.md
    FileSystem-->>EntityService: Success
    EntityService-->>CLI: Return new entity path
    CLI-->>User: Display success message
```

### Flow 2: `semops domain analyze --workflow ...`

This shows the more complex, multi-expert workflow for AI-driven analysis and content generation.

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant EntityService
    participant WorkflowEngine
    participant ExpertPromptGenerator
    participant KnowledgeService
    participant LLM

    User->>CLI: semops domain analyze --workflow my_workflow
    CLI->>EntityService: analyze(workflow="my_workflow")
    EntityService->>WorkflowEngine: execute("my_workflow", context)

    loop For each step in workflow
        WorkflowEngine->>ExpertPromptGenerator: generate(expert, task, context)
        ExpertPromptGenerator->>KnowledgeService: retrieve_context(query)
        KnowledgeService-->>ExpertPromptGenerator: Return relevant sources
        ExpertPromptGenerator->>LLM: Execute prompt
        LLM-->>ExpertPromptGenerator: Return AI-generated content
        ExpertPromptGenerator-->>WorkflowEngine: Return structured result
        WorkflowEngine->>EntityService: update(entity_id, new_content)
    end

    EntityService-->>CLI: Success
    CLI-->>User: Display success message
```

### Flow 3: API/MCP `create` Request

This shows how a non-CLI client, like a REST API or MCP server, interacts with the services. Note that context is provided explicitly in the request, bypassing the filesystem `ContextDetector`.

```mermaid
sequenceDiagram
    participant Client [API/MCP Client]
    participant API [REST API / MCP Server]
    participant EntityService
    participant ConfigManager
    participant TemplateEngine
    participant FileSystem

    Client->>API: POST /domains/{domain_id}/problems (body: {name: "New Problem"})
    API->>EntityService: create("problem", name="New Problem", parent_id="domain_id")
    EntityService->>ConfigManager: get_entity_config("problem")
    ConfigManager-->>EntityService: Return problem config
    EntityService->>TemplateEngine: render("problem.md.j2", ...)
    TemplateEngine-->>EntityService: Return rendered markdown
    EntityService->>FileSystem: Write domain/{domain_slug}/problems/new-problem/problem.md
    FileSystem-->>EntityService: Success
    EntityService-->>API: Return new entity data
    API-->>Client: 201 Created (response body)
```
