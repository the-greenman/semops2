# Collaborative Organization Architecture

This document defines the architecture for using SemOps2 to support collaborative organization governance with transparent operational records, authority-weighted knowledge, and interactive entity refinement journeys.

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Entity-Journey Framework](#entity-journey-framework)
3. [Modular Entity Packages](#modular-entity-packages)
4. [Template Evolution System](#template-evolution-system)
5. [Authority-Weighted Knowledge](#authority-weighted-knowledge)
6. [LangGraph Integration](#langgraph-integration)
7. [Example Workflows](#example-workflows)

## Core Concepts

### Design Principles

1. **Transparent Operational Records** - All organizational activities captured in canonical documents, with graph projections for traversal
2. **Human-AI Collaboration** - AI assists, humans decide at every stage
3. **Authority Hierarchy** - Different content types have different validity levels
4. **Rapid Evolution** - Templates change frequently in early use without causing chaos
5. **Modular Design** - Entity types and their journeys are self-contained packages
6. **CLI-First** - Command-line interface for all operations
7. **Protobuf-First Implementation** - Stable behavior is implemented as protobuf contracts; YAML is for planning and configuration iteration
8. **Entity Server as Mutation Boundary** - All creates/updates/deletes go through Entity Server validation and policy checks
9. **Hybrid Persistence** - Canonical human-readable documents plus graph/vector indexes for navigation and retrieval

### Opinionated Product Stance

The platform remains configurable for many organizational forms. The primary near-term use case is building post-human, democratic, human-positive, and earth-positive organizations that harness AI for the greater good.

Mission framing:
- Enable democracy at micro scale inside teams and organizations.
- Strengthen democracy at macro scale by developing transferable governance practices.

Design commitments for this use case:
- **Boundary First (Taiji)**: Define clear purpose, scope, and authority boundaries before optimization and scale.
- **Human Decision Sovereignty**: AI can analyze, propose, challenge, and coach; humans remain accountable for governance decisions.
- **Anti-Abdication by Design**: Workflow stages and boundary checks should prevent humans from silently offloading core governance duties to automation.

### Implementation Baseline

- Planning phase: journeys, templates, and package structures may evolve in YAML.
- Implementation phase: protobuf contracts become the runtime source of truth for service interfaces and validation.
- MCP is an orchestration/automation interface; it does not bypass Entity Server invariants.
- Founding bootstrap starts with human actor registration and role binding before constitution/policy drafting.
- Constitution starts as a minimal draft (`v0.x`, `constitution_state=draft|provisional`) and is iteratively refined as domains/problems become clearer.

### Architecture Invariants

These rules are mandatory for implementation and future design changes:

1. **Entity Server is the only mutation boundary**
   - All create/update/delete operations must execute through Entity Server.
   - No client (CLI, MCP, API, workflows) may write documents, graph records, or vector metadata directly.

2. **Protobuf contracts are the runtime source of truth**
   - Request/response schemas, validation, and compatibility rules are defined in protobuf.
   - YAML remains planning/configuration input, not the authoritative runtime contract.

3. **MCP is orchestration, not authority**
   - MCP may coordinate workflows, agent tools, and human-in-the-loop stages.
   - Any state mutation requested by MCP must call Entity Server APIs.

4. **Canonical human-readable documents are required**
   - Markdown + frontmatter is the canonical operational record for human browsing and audit.
   - Graph and vector stores are derived indexes over canonical documents.

5. **Hybrid persistence consistency is enforced**
   - A mutation is not complete until canonical document write and index updates are confirmed,
     or queued with guaranteed reconciliation and retry.
   - Drift between document state and graph/vector indexes must be detectable and repairable.

6. **Policy and relationship invariants are centralized**
   - Authority checks, boundary rules, and relationship constraints are enforced in Entity Server.
   - Workflow code cannot redefine or bypass these invariants.

7. **Every mutation is traceable**
   - Mutations record who/what initiated the change, when, and why (human, actor, or system).
   - Migration and workflow actions must produce auditable history.

8. **No actor attribution, no normal commit**
   - Standard operations must include `created_by_actor_id` / `updated_by_actor_id`.
   - `ACT-system` is allowed only for explicit system operations (bootstrap, imports, migrations, recovery).
   - Any temporary unknown attribution must be reconciled and reported.

### Hybrid Persistence Model

```
┌─────────────────────────────────────────────────────────┐
│ Canonical Documents (Markdown + frontmatter)            │
│ Human-browsable operational records                     │
│ - Domains, Roles, Meetings, Decisions, Policies         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ Graph Index (Neo4j)                                     │
│ Navigational and governance map over documents          │
│ - Entity relationships + semantic links                 │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ Vector Store (ChromaDB)                                 │
│ Embedding-based semantic search                         │
│ - Chunk embeddings with metadata                        │
│ - Authority weights, source types                       │
└─────────────────────────────────────────────────────────┘
```

Implications of this hybrid model:
- Human access remains first-class because documents are canonical artifacts.
- Graph and vector layers can be rebuilt from documents, reducing lock-in risk.
- Write-path consistency is critical: document and graph updates must commit atomically or with reliable reconciliation.
- Operational complexity is higher than a single-store model (indexing, sync jobs, repair tools).

### Exploration Interface (No Export Required)

Most browsing workflows should be read-only and scoped, not full-workspace export.

Explore interface requirements:
- Workspace overview (mission, constitution state, active domains, pending reviews)
- Entity listing and entity detail views
- Neighborhood traversal across relationships (depth-limited)
- Authority-weighted search
- Timeline of recent changes
- Open-question views for unresolved governance/workflow issues

Implementation approach:
- Add a read-only `ExploreService` in the IDL as the browse-optimized read model.
- Expose equivalent MCP browse tools for AI-mediated and CLI-mediated exploration.
- Keep mutation operations in Entity Server; browsing never bypasses write invariants.

### Constitutional Evolution Practice

- Create a bootstrap constitution early with minimal viable principles.
- Treat early constitution as provisional while organizational context is still being discovered.
- Use regular refinement cycles (domain/problem discoveries trigger constitutional review).
- Ratify only when principles and authority boundaries are stable enough for enforcement.
- After ratification, changes are managed as formal amendments with stronger review.
- Maintain a versioned set of constitutional process templates (ratification, amendment, review cadence).
- Accept that amendment process can itself evolve; govern this through explicit constitutional/policy decisions rather than hardcoded assumptions.
- Keep the system flexible: meta-process detail may be documented and audited even when not fully enforced as rigid runtime logic.

### Fine-Grained ADR Practice

- Treat ADRs as aggregates of small, linked decisions rather than one large decision object.
- Model a proposal as a decision bundle with cross-references among constituent decisions.
- Link each constituent decision to specific target-document changes (line-level intent via structured diff/change-set references).
- Preserve both views:
  - the aggregated ADR narrative for humans
  - the fine-grained decision/change graph for traceability and actor reasoning

## Entity-Journey Framework

### The Pattern

Traditional entity creation:
```bash
semops domain create foo --name "Foo" --purpose "Bar"
# Creates minimal entity, user fills in everything
```

Journey-based creation:
```bash
semops journey start domain-definition --name "Foo"
# Interactive multi-stage process with AI guidance
```

### Journey Structure

Every entity journey follows this pattern:

```yaml
entity_journey:
  journey_id: "entity-type-refinement"
  entity_type: "semops.core/entity_type"
  journey_type: "creation_refinement | extraction_refinement | evolution"

  stages:
    - name: "stage_name"
      type: "human.create | ai.assist | human.review | system.commit"
      agent: {...}  # For ai.assist stages
      actions: [...]  # For human.review stages
      knowledge_context: {...}  # Optional RAG integration
```

### Stage Types

1. **human.create** - User creates initial draft
2. **ai.assist** - AI analyzes and proposes enhancements
3. **human.review** - User reviews, edits, approves/rejects
4. **system.commit** - System finalizes and creates entities

### Iteration and Loops

Stages can loop back for refinement:

```yaml
- name: "review_scope"
  type: "human.review"
  actions:
    - action: "approve"
      next_stage: "resource_identification"  # Continue forward
    - action: "edit"
      next_stage: "scope_clarification"  # Loop back
    - action: "reject"
      next_stage: "draft_creation"  # Start over
```

### Journey Checkpointing

**LangGraph State**: Workflow execution state, allows pause/resume
**Entity Metadata**: Final journey state saved to entity for audit trail

Both are maintained (decision: C from audit):
```python
# LangGraph checkpoint
config = {"configurable": {"thread_id": "dom-foo"}}
workflow.update_state(config, new_state)

# Entity metadata
entity.metadata["journey_state"] = {
  "journey_id": "domain-definition",
  "completed_stages": ["draft_creation", "scope_clarification", ...],
  "final_state": {...}
}
```

### Workflow Ownership and Scope

To keep orchestration concerns clear:

1. **Journey definitions are per-entity and lifecycle-authoritative**
   - Defined in `entity_packages/<entity>/journey_definition.yaml`
   - Own stage sequencing, human checkpoints, and commit transitions
   - Operate over flat root collections with relationship links (not nested entity directories)

2. **Expert profiles are package-local by default**
   - Defined in `entity_packages/<entity>/experts.yaml`
   - Journey `ai.assist` stages resolve `agent.role` from package experts first
   - Optional shared baseline may exist in `.semops/config/expert_types.yaml`

3. **Analysis workflows are reusable expert pipelines**
   - Defined in `.semops/config/workflows.yaml`
   - Reused across entities through `applicable_entity_types`
   - May be invoked from journey stages or executed directly via CLI/API/MCP without a journey

4. **RAG workflows are retrieval-only**
   - Defined in `.semops/config/rag_workflows.yaml`
   - Control retrieval/ranking/context assembly
   - Do not own lifecycle transitions

## Modular Entity Packages

### Package Structure

Each entity type is a self-contained package:

```
entity_packages/domain/
├── entity_definition.yaml      # Entity type config
├── experts.yaml                # Package-local expert profiles
├── journey_definition.yaml     # Interactive refinement process
├── migration_rules.yaml        # Template evolution rules
└── templates/
    └── v1.0.0/
        ├── create.md.j2       # Creation template
        └── analyze.md.j2      # Analysis template
```

### Entity Definition

```yaml
# entity_definition.yaml
entity_type:
  type_key: "domain"
  namespace: "semops.core"
  id_prefix: "DOM"
  template_version: "1.0.0"  # Workspace-wide versioning

  required_fields:
    - "domain_name"
    - "purpose"
    - "authority_level"

  template_bundle:
    create: "create.md.j2"
    analyze: "analyze.md.j2"
```

### Journey Definition

```yaml
# journey_definition.yaml
entity_journey:
  journey_id: "domain-definition"
  entity_type: "semops.core/domain"

  stages:
    - name: "draft_creation"
      type: "human.create"

    - name: "scope_clarification"
      type: "ai.assist"
      agent:
        role: "domain_architect"
        persona: "You help define domain boundaries..."
        expertise: ["scope_definition", "boundary_setting"]
        model: "claude-3-5-sonnet"

      task: |
        Analyze this domain draft and propose clear scope,
        related domains, stakeholders, and resources.

      knowledge_context:
        query: "existing domains, organizational structure"
        workflow: "authority_weighted"
        entity_types: ["domain", "role", "constitution"]

    - name: "review_scope"
      type: "human.review"
      actions:
        - action: "approve"
        - action: "edit"  # Loops back to scope_clarification
```

### Package Distribution

**Current** (decision: C from audit): Copy examples directory
```bash
cp -r semops2/examples/entity_packages/* myorg/.semops/entity_packages/
```

**Future**: Package registry or git submodules

## Template Evolution System

### Why It's Critical

Early adoption = rapid template changes. Without template evolution:
- ❌ Entities become outdated
- ❌ Validation fails
- ❌ Chaos as templates diverge
- ❌ Manual fixes error-prone

With template evolution:
- ✅ Controlled evolution
- ✅ LLM-assisted migration
- ✅ No data loss
- ✅ Audit trail

### Template Versioning

**Workspace-wide versioning** (decision: B from audit):
```yaml
# workspace_config.yaml
template_version: "1.1.0"

# All entity packages use this version
# Migration happens together, not piecemeal
```

### Migration Rules

```yaml
# migration_rules.yaml
current_version: "1.0.0"

migrations:
  "1.0.0 → 1.1.0":
    breaking: false
    strategy: "llm_assisted"

    changes:
      added_fields:
        - field: "authority_level"
          type: "string"
          required: true
          infer_from: ["domain_name", "purpose", "scope_included"]
          prompt: |
            Based on the domain name, purpose, and scope, determine the
            authority level. Options: HIGH, MEDIUM, LOW.

            HIGH: Governance, security, compliance, constitutional
            MEDIUM: Core operational domains
            LOW: Supporting or exploratory domains

    validation:
      - check: "authority_level in ['HIGH', 'MEDIUM', 'LOW']"
        error_message: "authority_level must be HIGH, MEDIUM, or LOW"

    rollback_supported: true
    backup_retention_days: 90
```

### Migration Strategies

1. **automated** - Direct field mapping, no review
2. **llm_assisted** - AI infers new fields from context
3. **llm_assisted_with_review** - AI + human approval
4. **manual** - Complex changes need human work

### Migration Workflow

**Manual trigger** (decision: A from audit):
```bash
# Check for outdated entities
semops migrate check

# Preview migration
semops migrate preview --to-version 1.1.0

# Execute migration
semops migrate run --strategy llm_assisted_with_review

# Review each migration
semops migrate review <entity-id>

# Approve or reject
semops migrate approve <entity-id>
semops migrate reject <entity-id>

# If problems, rollback
semops migrate rollback --to-version 1.0.0
```

### Migration Actions

```
1. backup_entity → Store current state in .semops/backups/
2. load_entity_context → Get entity + relationships + knowledge sources
3. llm_infer_fields → AI analyzes context and suggests new field values
4. generate_migration_preview → Show before/after
5. human_review → User approves/rejects (if strategy requires)
6. apply_new_template → Render with v1.1.0 template
7. validate_migration → Check all required fields present
8. commit_changes → Save canonical document revision
9. update_projections → Rebuild or queue entity_graph/knowledge_graph/vector projection updates with reconciliation metadata
```

## Authority-Weighted Knowledge

### The Problem

Not all knowledge is equally authoritative:
- Constitutional documents define foundational principles
- Formal decisions establish policy
- Meeting records capture what was discussed
- Exploratory notes are just brainstorming

### The Solution

Source types with authority weights (0.0 - 1.0):

```yaml
source_types:

  constitutional_documents:
    authority_weight: 1.0  # Highest authority
    description: "Foundational governing documents"

  formal_decisions:
    authority_weight: 0.95
    description: "Ratified decisions with formal process"

  meeting_records:
    authority_weight: 0.75
    description: "Documented discussions and transcripts"

  working_documents:
    authority_weight: 0.5
    description: "Draft policies, proposals in progress"

  informal_discussions:
    authority_weight: 0.4
    description: "Slack threads, async conversations"

  exploratory_notes:
    authority_weight: 0.2  # Lowest authority
    description: "Brainstorming, early-stage thinking"

  external_standards:
    authority_weight: 0.8
    description: "Industry standards, regulatory frameworks"
```

### RAG Workflow Integration

Authority-weighted retrieval:

```yaml
rag_workflows:

  authority_weighted:
    description: "Prioritize authoritative sources in retrieval"

    retrieval_strategy: "hybrid"
    k: 10

    source_weights:
      constitutional_documents: 1.0
      formal_decisions: 0.95
      meeting_records: 0.75
      exploratory_notes: 0.2

    post_processing:
      - action: "apply_authority_weights"
        method: "multiply_similarity_score"  # score * authority_weight

      - action: "sort_by_weighted_score"

      - action: "add_authority_label"
        labels:
          "≥0.9": "AUTHORITATIVE"
          "≥0.7": "FORMAL"
          "≥0.5": "DOCUMENTED"
          "<0.5": "EXPLORATORY"
```

### Journey Integration

AI agents use authority-weighted retrieval:

```yaml
- name: "scope_clarification"
  type: "ai.assist"
  agent:
    role: "domain_architect"

  knowledge_context:
    query: "existing domains, organizational structure, governance"
    workflow: "authority_weighted"  # Uses authority weights
    entity_types: ["domain", "role", "constitution", "policy"]

  # AI receives context with authority labels:
  # [AUTHORITATIVE] Constitution: "Domains must have clear accountability..."
  # [FORMAL] Policy: "Domain leads are responsible for..."
  # [EXPLORATORY] Notes: "Maybe we should consider..."
```

## LangGraph Integration

### Architecture

```
┌─────────────────────────────────────────────────────┐
│ CLI                                                  │
│ semops journey start domain-definition --name "Foo" │
└─────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ Journey Orchestrator (LangGraph)                    │
│ • Load journey definition YAML                      │
│ • Build state graph from stages                     │
│ • Execute with checkpointing                        │
│ • Pause for human review                            │
│ • Resume with user input                            │
└─────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ SemOps2 MCP Server (Orchestration + Extensions)     │
│ • Coordinates workflows and AI/tool integrations    │
│ • Exposes controlled automation surface             │
└─────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ Entity Server (Authoritative Mutation Boundary)     │
│ • Protobuf validation + policy checks               │
│ • EntityService + relationship invariants           │
│ • Emits canonical document + graph/vector updates   │
└─────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ Core Services + Storage                             │
│ • KnowledgeService • TemplateService • Indexers     │
│ • Document Store • Graph Store • Vector Store       │
└─────────────────────────────────────────────────────┘
```

### Journey Execution

```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from semops.journeys import load_journey

# Load journey definition
journey = load_journey("domain-definition")

# Convert to LangGraph workflow
class JourneyState(TypedDict):
    actor_id: str
    draft_entity: dict
    scope_proposal: dict
    approved_scope: dict
    selected_resources: list
    approved_stakeholders: dict
    entity_id: str

def draft_creation(state: JourneyState):
    # Human input collected via CLI
    return {
        "draft_entity": user_input,
        "entity_id": allocate_draft_entity_id("semops.core/domain")
    }

async def scope_clarification(state: JourneyState):
    # AI assistance via MCP
    expert_type = resolve_expert_type(
        entity_type="semops.core/domain",
        role=journey.stages["scope_clarification"].agent.role
    )
    async with get_semops_client() as mcp:
        result = await mcp.call_tool("semops_expert_analyze", {
            "actor_id": state["actor_id"],
            "entity_id": state["entity_id"],
            "expert_type": expert_type,
            "workflow": "journey-stage-analysis",
            "parameters": {
                "content": state["draft_entity"],
                "task": journey.stages["scope_clarification"].task
            }
        })
    return {"scope_proposal": result}

def review_scope(state: JourneyState):
    # Human review via CLI
    display_proposal(state["scope_proposal"])
    action = prompt_user_action(["approve", "edit", "reject"])

    if action == "edit":
        # Loop back to scope_clarification
        return {"needs_clarification": True}
    else:
        return {"approved_scope": state["scope_proposal"]}

# Build workflow
workflow = StateGraph(JourneyState)
workflow.add_node("draft_creation", draft_creation)
workflow.add_node("scope_clarification", scope_clarification)
workflow.add_node("review_scope", review_scope)

workflow.add_edge("draft_creation", "scope_clarification")
workflow.add_conditional_edges("review_scope", check_action, {
    "approve": "resource_identification",
    "edit": "scope_clarification",  # Loop back
    "reject": "draft_creation"
})

# Compile with checkpointing
app = workflow.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["review_scope"]  # Pause for human input
)

# Execute
config = {"configurable": {"thread_id": "dom-foo"}}
result = await app.ainvoke(initial_state, config=config)
```

### CLI Interaction

```bash
$ semops journey start domain-definition --name "Security & Compliance"

🚀 Starting journey: domain-definition
📍 Stage: draft_creation

What is the purpose of this domain?
> Ensure organization meets security standards and compliance requirements

Are there any specific areas you want to include?
> Security audits, compliance documentation, incident response

✓ Draft created

📍 Stage: scope_clarification
🤖 AI is analyzing your draft...

AI Proposal:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scope Definition:

IN SCOPE:
• Security policy development and maintenance
• Compliance documentation (SOC2, ISO27001, etc.)
• Security audits and assessments
• Incident response procedures
• Vulnerability management
• Access control standards

OUT OF SCOPE:
• Day-to-day IT operations (separate "IT Operations" domain)
• Product security features (part of "Engineering" domain)
• Physical security (part of "Facilities" domain)

Related Domains:
• IT Operations (handles implementation of security controls)
• Engineering (implements product security)
• Legal (handles regulatory interpretation)

Suggested Stakeholders:
• Security Lead (accountability)
• Compliance Officer (accountability)
• Engineering Leads (consulted)
• Legal Counsel (consulted)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Actions:
  [1] Accept AI proposal
  [2] Edit and refine
  [3] Start over

Your choice: 1
✓ Scope approved

📍 Stage: resource_identification
🤖 AI is searching for relevant resources...

[... continues through remaining stages ...]

✅ Domain created: DOM-security-compliance

Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Entity ID: DOM-security-compliance
Name: Security & Compliance
Scope: Security policy, compliance, audits, training
Resources: 4 entities, 2 external sources
Stakeholders: 2 accountable, 2 consulted
Authority: HIGH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next steps:
  • Add vulnerability management procedure (identified gap)
  • Create security training materials
  • Schedule quarterly domain review

View domain: semops domain get DOM-security-compliance
```

## Example Workflows

### Workflow 1: Establishing a Collaborative Organization

**Starting point**: New organization needs foundational governance

```bash
# 1. Initialize workspace with collaborative org config
semops init --config examples/config/collaborative_org_config_v2.yaml

# 2. Register founding humans as actors
semops actor register --actor-type human --name "Founder A" --actor-id ACT-founder-a
semops actor register --actor-type human --name "Founder B" --actor-id ACT-founder-b

# 3. Bind founding governance roles
semops relationship add holds_role ACT-founder-a ROLE-founder
semops relationship add holds_role ACT-founder-b ROLE-founder

# 4. Create bootstrap constitution through ratification journey
semops journey start constitution-ratification --name "Founding Charter"
# Interactive process with:
# - Bootstrap v0.x draft (minimal principles, open questions)
# - Context integration from domain/problem discovery (AI-assisted)
# - Iterative review/refinement
# - Provisional or ratified vote
# - Commit with constitution_state + amendment log

# Created: CONST-founding-charter (authority_weight: 1.0)
# Provenance: created_by_actor_id=ACT-founder-a (or ACT-founder-b)

# 5. Create initial domains
semops journey start domain-definition --name "Governance"
# Interactive process with:
# - Scope clarification (AI-assisted)
# - Resource identification (AI finds related entities)
# - Stakeholder mapping (AI suggests roles)
# - Finalization

# Created: DOM-governance
# Authority: HIGH (governance domain)

semops journey start domain-definition --name "Operations"
# Created: DOM-operations
# Authority: MEDIUM (operational domain)

# 6. Hold founding meeting
semops meeting create founding-meeting \
  --name "Founding Meeting" \
  --part-of DOM-governance \
  --add-transcription transcription.md

# Created: MTG-founding-meeting

# 7. Extract decisions from meeting
semops journey start decision-refinement MTG-founding-meeting
# Interactive process with:
# - AI identifies potential decisions in transcription
# - Human reviews, confirms, merges, splits
# - For each decision:
#   - AI clarifies statement and scope
#   - Human reviews
#   - AI explores options
#   - Human selects
#   - AI identifies stakeholders
#   - Human approves
#   - System creates decision entity

# Created: DEC-001, DEC-002, DEC-003, ...
# Each decision linked to MTG-founding-meeting

# 8. One decision establishes a policy
semops journey start policy-development --name "Access Control Policy"
# Interactive process similar to domain-definition

# Created: POL-access-control

# Establish relationship
semops relationship add establishes DEC-002 POL-access-control

# 9. Verify authority hierarchy
semops knowledge search "access control requirements" \
  --workflow authority_weighted

# Results prioritized:
# [AUTHORITATIVE] CONST-founding-charter: "Access must be..."
# [FORMAL] POL-access-control: "Access control policy..."
# [FORMAL] DEC-002: "Decision to adopt access control..."
# [DOCUMENTED] MTG-founding-meeting: "Discussion of access..."
```

### Workflow 2: Template Evolution in Action

**Context**: Organization adds "authority_level" field to domain entities after 3 months of use

```bash
# 1. Update template version in workspace
# Edit workspace_config.yaml:
#   template_version: "1.0.0" → "1.1.0"

# Update entity_packages/domain/entity_definition.yaml:
#   template_version: "1.1.0"
#   required_fields:
#     - "domain_name"
#     - "purpose"
#     - "authority_level"  # NEW FIELD

# Update entity_packages/domain/templates/v1.1.0/create.md.j2
# (add authority_level to template)

# 2. Add migration rule
# Edit entity_packages/domain/migration_rules.yaml:
migrations:
  "1.0.0 → 1.1.0":
    strategy: "llm_assisted_with_review"
    changes:
      added_fields:
        - field: "authority_level"
          infer_from: ["domain_name", "purpose", "scope_included"]
          prompt: "Determine authority level: HIGH, MEDIUM, or LOW"

# 3. Check which entities need migration
$ semops migrate check

Found 5 domain entities using template v1.0.0:
  • DOM-governance (created 3 months ago)
  • DOM-operations (created 3 months ago)
  • DOM-engineering (created 2 months ago)
  • DOM-marketing (created 1 month ago)
  • DOM-exploration (created 1 week ago)

Migration required to v1.1.0 (adds authority_level field)

# 4. Preview migration
$ semops migrate preview --entity-type domain

Previewing migration for DOM-governance:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current (v1.0.0):
  domain_name: "Governance"
  purpose: "Organizational governance and decision-making"
  scope_included: ["constitutional matters", "policy development"]

Proposed (v1.1.0):
  domain_name: "Governance"
  purpose: "Organizational governance and decision-making"
  scope_included: ["constitutional matters", "policy development"]
  authority_level: "HIGH"  ← AI inferred from governance scope

Confidence: 95%
Reasoning: Domain handles constitutional matters and policy,
           which are high-authority activities.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Similar previews for other 4 domains]

# 5. Run migration with review
$ semops migrate run --strategy llm_assisted_with_review

Migrating 5 domain entities from v1.0.0 → v1.1.0...

[1/5] DOM-governance
  ✓ Backed up to .semops/backups/migrations/20260226/DOM-governance
  ✓ Loaded context (entity + 8 relationships + 3 knowledge sources)
  ✓ LLM inferred authority_level: "HIGH" (confidence: 95%)

  Review:
    [1] Approve
    [2] Edit value
    [3] Skip this entity

  Your choice: 1
  ✓ Applied template v1.1.0
  ✓ Validated migration
  ✓ Committed changes
  ✓ Restored relationships

[2/5] DOM-operations
  ✓ Backed up
  ✓ LLM inferred authority_level: "MEDIUM" (confidence: 90%)

  Review:
    [1] Approve
    [2] Edit value
    [3] Skip this entity

  Your choice: 1
  ✓ Migration completed

[3/5] DOM-engineering
  ✓ Backed up
  ✓ LLM inferred authority_level: "MEDIUM" (confidence: 85%)

  Review:
    [1] Approve
    [2] Edit value
    [3] Skip this entity

  Your choice: 2

  Current value: "MEDIUM"
  Enter new value: LOW
  ✓ Value updated to "LOW"
  ✓ Migration completed

[4/5] DOM-marketing
  ✓ Backed up
  ✓ LLM inferred authority_level: "LOW" (confidence: 92%)

  Review: ...
  Your choice: 1
  ✓ Migration completed

[5/5] DOM-exploration
  ✓ Backed up
  ✓ LLM inferred authority_level: "LOW" (confidence: 98%)

  Review: ...
  Your choice: 1
  ✓ Migration completed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Migration Summary:
  • Migrated: 5/5 entities
  • Approved as-is: 4
  • Edited: 1 (DOM-engineering)
  • Skipped: 0
  • Failed: 0
  • Backup location: .semops/backups/migrations/20260226/
  • Retention: 90 days
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All domain entities now use template v1.1.0.

# 6. If something went wrong, rollback
$ semops migrate rollback --to-version 1.0.0

# (Restores all 5 entities from backup)
```

### Workflow 3: Authority-Weighted Decision Making

**Context**: Making a decision about security policy, need to reference authoritative sources

```bash
# 1. Start decision journey from security meeting
$ semops journey start decision-refinement MTG-security-review-q1

# 2. AI identifies potential decision
📍 Stage: identify_decisions
🤖 Found 1 potential decision:

  "Adopt Zero Trust security architecture"
  Context: Team discussed moving to Zero Trust model
  Clarity: Unclear (needs definition of scope)

# 3. Human confirms
Your choice: Confirm

# 4. AI clarifies with authority-weighted context
📍 Stage: clarify_decision
🤖 Analyzing decision with knowledge context...

AI retrieved authoritative sources:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[AUTHORITATIVE 1.0] CONST-founding-charter
  "Security architecture must align with principle of least privilege"

[FORMAL 0.95] POL-access-control
  "All access decisions must be explicitly authorized"

[FORMAL 0.8] External: NIST Zero Trust Architecture
  "Zero Trust assumes no implicit trust..."

[DOCUMENTED 0.75] MTG-security-review-q1
  "Discussion of Zero Trust implementation"

[EXPLORATORY 0.2] Notes from security-brainstorm
  "Maybe we should consider Zero Trust?"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AI Proposal (informed by authoritative sources):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Decision Statement:
  "Adopt Zero Trust security architecture for all system access,
   implementing explicit authorization and least privilege principles
   as defined in our access control policy"

Scope Included:
  • Network access controls
  • Application authentication
  • API authorization
  • User access management

Scope Excluded:
  • Physical security (separate domain)
  • Existing legacy systems (phased approach)

Desired Outcome:
  "All access decisions explicitly authorized, reducing attack surface
   and aligning with constitutional principle of least privilege"

Assumptions:
  • Phased rollout over 6 months
  • Budget approved for ZTNA solution
  • Engineering capacity available

Authority Alignment:
  ✓ Aligns with CONST-founding-charter (least privilege)
  ✓ Implements POL-access-control (explicit authorization)
  ✓ Follows NIST standards (external authority)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Actions:
  [1] Approve
  [2] Edit
  [3] Reject

Your choice: 1
✓ Statement approved

# Journey continues through options, stakeholders, readiness...

✅ Decision created: DEC-adopt-zero-trust

# 5. Verify authority hierarchy respected
$ semops decision get DEC-adopt-zero-trust

Decision: Adopt Zero Trust Security Architecture
Authority Source: CONST-founding-charter (authority: 1.0)
Implements: POL-access-control (authority: 0.95)
Status: ready

# Decision has highest authority backing (constitution)
```

### Workflow 4: Self-Referential System Design (SemOps Designing SemOps)

**Context**: The organization uses SemOps to evolve SemOps architecture and governance.

```bash
# 1. Create a domain for SemOps architecture stewardship
semops journey start domain-definition --name "SemOps Architecture"
# Created: DOM-semops-architecture

# 2. Create a problem that captures current system tension
semops problem create sync-complexity \
  --name "Hybrid Source-of-Truth Complexity" \
  --part-of DOM-semops-architecture
# Created: PROB-sync-complexity

# 3. Gather evidence as artefacts/conversations
semops conversation create arch-review-2026-q1 \
  --name "Architecture Review: Source of Truth" \
  --part-of DOM-semops-architecture

semops artefact create decision-record-hybrid-options \
  --name "ADR: Hybrid vs Canonical Runtime Model" \
  --part-of DOM-semops-architecture

# 4. Run decision refinement based on meeting/conversation evidence
semops journey start decision-refinement CONV-arch-review-2026-q1
# Created: DEC-* set (small scoped decisions)
# Example:
#   DEC-canonical-runtime-source
#   DEC-enable-projection-read-model
#   DEC-defer-roundtrip-import

# 4b. Aggregate small decisions into one ADR view
semops adr create ADR-hybrid-architecture-q1 \
  --decisions DEC-canonical-runtime-source,DEC-enable-projection-read-model,DEC-defer-roundtrip-import
# Created: ADR-hybrid-architecture-q1 (decision bundle)

# 5. Link decision to constitutional and policy updates
semops relationship add references ADR-hybrid-architecture-q1 CONST-founding-charter
semops journey start policy-development --name "System Evolution Policy"
# Created: POL-system-evolution
semops relationship add establishes DEC-canonical-runtime-source POL-system-evolution

# 6. If scope/process changed, run constitutional amendment workflow
semops journey start constitution-ratification --name "Founding Charter Amendment 2026-Q1"
# Constitution state transitions: provisional -> ratified (with amendment log)

# 6b. Link specific decisions to specific constitutional/policy diffs
semops change link \
  --decision-id DEC-canonical-runtime-source \
  --target CONST-founding-charter \
  --change-ref CHG-const-2026-q1-001
semops change link \
  --decision-id DEC-enable-projection-read-model \
  --target POL-system-evolution \
  --change-ref CHG-pol-2026-q1-004

# 7. Verify actor boundary compliance for automation proposals
semops actor permission-check \
  --actor-id ACT-assistant-007 \
  --action create_decision \
  --context authority_level=HIGH,affects_constitution=true
# Expected: needs_approval or forbidden, with policy references
```

Expected outcome:
- Domains and problems produce traceable architectural decisions.
- Constitution remains the boundary and process authority.
- Actors can propose and analyze, but system evolution remains governance-bounded.
- ADR proposals are traceable bundles of small decisions with explicit document-change links.

### Self-Referential Validation Checklist

Use this checklist to validate that the architecture can safely design itself:

1. **Constitutional Grounding**
   - Every architectural decision references constitutional principles or approved amendment path.
2. **Problem-to-Decision Traceability**
   - Each major architecture decision links back to at least one explicit problem entity.
3. **Actor Attribution Completeness**
   - All mutations in system-design workflows carry valid actor attribution.
4. **Boundary Enforcement**
   - High-authority or constitutional-impact actions from software actors require human approvals.
5. **Policy Materialization**
   - Approved architectural decisions produce policy/process updates, not only discussion artefacts.
6. **Evolution Transparency**
   - Timeline/audit view can reconstruct who changed system structure, when, and why.
7. **Reversibility**
   - System-level changes have rollback/migration strategy and tested recovery path.
8. **Comprehensibility Across Actor Types**
   - Human and non-human actors can discover current goals, boundaries, and allowed actions via Explore + MCP interfaces.

## Summary

This architecture provides:

1. **Entity-Journey Framework** - Interactive AI-assisted entity creation
2. **Modular Packages** - Self-contained entity type definitions
3. **Template Evolution** - Controlled, LLM-assisted migration without chaos
4. **Authority Hierarchy** - Different sources have different validity
5. **LangGraph Orchestration** - Human-in-the-loop workflows with checkpointing
6. **CLI-First** - Command-line interface for all operations

The result: A collaborative organization can establish transparent governance, make informed decisions backed by authoritative sources, and evolve their templates as they learn - all with AI assistance but human control at every step.

## Next Steps

1. Review entity packages in `/workspace/examples/entity_packages/`
2. See [TEMPLATE_EVOLUTION_GUIDE.md](../examples/TEMPLATE_EVOLUTION_GUIDE.md) for migration details
3. See [COLLABORATIVE_ORG_QUICKSTART.md](../examples/COLLABORATIVE_ORG_QUICKSTART.md) for getting started
4. Explore journey definitions for each entity type
5. Customize for your organization's needs
