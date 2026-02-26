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

1. **Transparent Operational Records** - All organizational activities captured in entity graph
2. **Human-AI Collaboration** - AI assists, humans decide at every stage
3. **Authority Hierarchy** - Different content types have different validity levels
4. **Rapid Evolution** - Templates change frequently in early use without causing chaos
5. **Modular Design** - Entity types and their journeys are self-contained packages
6. **CLI-First** - Command-line interface for all operations

### The Three Graphs

```
┌─────────────────────────────────────────────────────────┐
│ Entity Graph (Neo4j)                                    │
│ Operational entities and relationships                  │
│ - Domains, Roles, Meetings, Decisions, Policies        │
│ - part_of, accountable_for, establishes, ratifies      │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ Knowledge Graph (Neo4j)                                 │
│ Semantic content and concepts                          │
│ - Documents, Chunks, Concepts, Citations                │
│ - mentions, relates_to, derives_from                    │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ Vector Store (ChromaDB)                                 │
│ Embedding-based semantic search                         │
│ - Chunk embeddings with metadata                        │
│ - Authority weights, source types                       │
└─────────────────────────────────────────────────────────┘
```

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
  journey_id: "entity_type_refinement"
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
  "journey_id": "domain_definition",
  "completed_stages": ["draft_creation", "scope_clarification", ...],
  "final_state": {...}
}
```

## Modular Entity Packages

### Package Structure

Each entity type is a self-contained package:

```
entity_packages/domain/
├── entity_definition.yaml      # Entity type config
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
  journey_id: "domain_definition"
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
8. commit_changes → Save to entity graph
9. restore_relationships → Re-establish graph connections
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

  authority_weighted_search:
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
│ SemOps2 MCP Server (Tools)                          │
│ • semops_create_entity                              │
│ • semops_get_entity                                 │
│ • semops_expert_analyze                             │
│ • semops_add_relationship                           │
│ • semops_knowledge_search                           │
└─────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ SemOps2 Core Services                               │
│ • EntityService                                     │
│ • ExpertService                                     │
│ • KnowledgeService                                  │
│ • TemplateService                                   │
└─────────────────────────────────────────────────────┘
```

### Journey Execution

```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from semops.journeys import load_journey

# Load journey definition
journey = load_journey("domain_definition")

# Convert to LangGraph workflow
class JourneyState(TypedDict):
    draft_entity: dict
    scope_proposal: dict
    approved_scope: dict
    selected_resources: list
    approved_stakeholders: dict
    entity_id: str

def draft_creation(state: JourneyState):
    # Human input collected via CLI
    return {"draft_entity": user_input}

async def scope_clarification(state: JourneyState):
    # AI assistance via MCP
    async with get_semops_client() as mcp:
        result = await mcp.call_tool("semops_expert_analyze", {
            "expert_role": "domain_architect",
            "content": state["draft_entity"],
            "task": journey.stages["scope_clarification"].task
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

🚀 Starting journey: domain_definition
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
semops init --config examples/entity_packages

# 2. Create constitution through ratification journey
semops journey start constitution-ratification --name "Founding Charter"
# Interactive process with:
# - Draft principles
# - Stakeholder consultation (AI-assisted)
# - Review and refinement
# - Formal voting process
# - Ratification

# Created: CONST-founding-charter (authority_weight: 1.0)

# 3. Create initial domains
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

# 4. Hold founding meeting
semops meeting create founding-meeting \
  --name "Founding Meeting" \
  --part-of DOM-governance \
  --add-transcription transcription.md

# Created: MTG-founding-meeting

# 5. Extract decisions from meeting
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

# 6. One decision establishes a policy
semops journey start policy-development --name "Access Control Policy"
# Interactive process similar to domain-definition

# Created: POL-access-control

# Establish relationship
semops relationship add establishes DEC-002 POL-access-control

# 7. Verify authority hierarchy
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
