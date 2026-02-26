# Semantic Architecture for Human-Posthuman Collaboration

## Core Vision

SemOps2 is not just an organizational tool—it is a **semantic architecture system** that enables collaboration between different forms of intelligence (humans, software actors, and future posthuman actors).

### Current Opinionated Stance

SemOps2 should remain adaptable to many organizational forms, but the primary near-term use case is:
- building effective post-human, democratic, human-positive, and earth-positive organizations
- using AI to strengthen collective intelligence for the greater good

Guiding stance:
- establish clear boundaries (taiji) before scaling action
- implement robust AI-supported human decision processes
- keep humans accountable for governance and decisions
- use AI as coach and challenger, not as a substitute for human duty

Mission framing:
- SemOps2 is a tool for democracy at micro scale.
- It aims to influence democracy at macro scale by cultivating repeatable foundational practices.

Self-referential requirement:
- SemOps2 should be usable to design and evolve SemOps2 itself.
- Domains and problems should generate architectural decisions.
- The constitution must hold scope/process boundaries while actors evolve the system within those boundaries.
- Proposals (including ADRs) should be representable as aggregates of fine-grained decisions.
- Decisions should link to explicit target-document changes (diff/change-set references), not only high-level narrative.

The system develops structured context and intent that allows diverse intelligences to:
- Understand the purpose and boundaries of their operational environment
- Discover their role within larger collaborative structures
- Navigate authority hierarchies and decision-making processes
- Build shared understanding across different cognitive paradigms

## The Intelligence Collaboration Problem

### Traditional Systems
Designed for human-only collaboration:
- Implicit context (cultural knowledge, unstated assumptions)
- Ambiguous boundaries
- Hidden authority structures
- Context locked in human memory

**Problem**: non-human actors cannot effectively participate because critical context is inaccessible.

### SemOps2 Approach
Explicit semantic architecture:
- **Structured context** - Canonical operational context in documents with queryable graph projections
- **Clear boundaries** - Domain scopes, relationship types, authority levels
- **Transparent authority** - Constitutional hierarchy with weights
- **Intent preservation** - Decision rationale, assumptions, outcomes
- **Evolution tracking** - Why and how structures change

**Result**: Humans and other actors can query the system to understand "what am I part of and what can I do?"

## MCP as the Intelligence Interface

### MCP Server Role

The Model Context Protocol (MCP) server is the **semantic interface** through which actors discover context and intent. MCP orchestrates interactions, but all mutating operations are enforced by Entity Server.

```
Actor
   ↓
MCP Server (Semantic Interface)
   ↓
Entity Server (Validation + Policy Boundary)
   ↓
Canonical Documents (Operational Record)
   ↓
Entity Graph (Derived Structure)
   ↓
Knowledge Graph (Derived Semantic Context)
   ↓
Vector Store (Weighted Knowledge)
```

### Critical MCP Capabilities

#### 1. Context Discovery
Actors query: "What system am I part of?"

```python
# MCP Tool: semops_discover_operational_context
async def semops_discover_operational_context(actor_id: str):
    """
    Provides actor with complete operational context

    Returns:
    - Constitutional principles governing this system
    - Domains this actor can operate in
    - Authority level and decision-making boundaries
    - Relevant policies and procedures
    - Current state of the system
    """

    # Example response:
    {
        "system_identity": {
            "name": "Collaborative Organization",
            "constitution_id": "CONST-founding-charter",
            "principles": [
                "Transparency in all operations",
                "Consensus for constitutional changes",
                "Authority hierarchy from constitution → policy → decisions"
            ]
        },

        "actor_context": {
            "actor_id": "ACT-assistant-001",
            "authority_level": "MEDIUM",
            "accountable_for": ["DOM-operations"],
            "consulted_for": ["DOM-governance"],
            "informed_about": ["DOM-engineering"]
        },

        "operational_boundaries": {
            "can_create": ["meeting", "conversation", "artefact"],
            "can_suggest": ["decision", "policy"],
            "cannot_create": ["constitution"],
            "requires_approval_from_roles": ["decisions with authority > MEDIUM"]
        },

        "knowledge_access": {
            "authority_weighted_sources": {
                "constitutional_documents": 1.0,
                "formal_decisions": 0.95,
                "meeting_records": 0.75,
                "exploratory_notes": 0.2
            },
            "accessible_domains": ["DOM-operations", "DOM-engineering"]
        },

        "current_state": {
            "active_journeys": ["decision_refinement: MTG-weekly-sync"],
            "pending_reviews": ["DEC-003: needs human approval"],
            "recent_changes": [
                "POL-access-control: updated 2 days ago",
                "DOM-governance: stakeholders added 1 week ago"
            ]
        }
    }
```

#### 2. Intent Understanding
Actors query: "Why does this exist and what should I do with it?"

```python
# MCP Tool: semops_understand_entity_intent
async def semops_understand_entity_intent(entity_id: str):
    """
    Explains purpose, context, and usage of an entity

    Returns:
    - Creation rationale (why was this created)
    - Relationships (how does this connect to other entities)
    - Authority level (how authoritative is this)
    - Usage patterns (how is this typically used)
    - Evolution history (how has this changed)
    """

    # Example response for DOM-security:
    {
        "entity_id": "DOM-security",
        "entity_type": "domain",

        "creation_intent": {
            "purpose": "Ensure organization meets security standards and compliance",
            "rationale": "Regulatory requirements demand formal security governance",
            "created_by": "DEC-establish-security-domain",
            "authority_source": "CONST-founding-charter",
            "journey_state": "completed (all stages)"
        },

        "semantic_context": {
            "scope_included": [
                "Security policy development",
                "Compliance documentation",
                "Incident response"
            ],
            "scope_excluded": [
                "Day-to-day IT operations (see DOM-operations)",
                "Product security (see DOM-engineering)"
            ],
            "authority_level": "HIGH",
            "authority_reasoning": "Security is constitutional mandate"
        },

        "relationships": {
            "governed_by": ["CONST-founding-charter"],
            "implements": ["POL-access-control", "POL-incident-response"],
            "part_of": [],  # Root domain
            "related_to": ["DOM-operations", "DOM-legal"]
        },

        "knowledge_context": {
            "knowledge_sources": [
                {"type": "external_standards", "url": "NIST CSF", "authority": 0.8},
                {"type": "formal_decisions", "entity": "DEC-adopt-zero-trust", "authority": 0.95}
            ],
            "authority_weight": 1.0,  # Domain itself is highly authoritative
            "key_concepts": ["zero-trust", "least-privilege", "explicit-authorization"]
        },

        "usage_patterns": {
            "typical_interactions": [
                "Query for security requirements before making decisions",
                "Add security incidents as entities with relationships",
                "Reference in decisions that have security implications"
            ],
            "actors_with_access": [
                "ROL-security-lead (accountable)",
                "ROL-compliance-officer (accountable)",
                "ROL-engineering-leads (consulted)"
            ]
        },

        "evolution": {
            "template_version": "1.1.0",
            "last_migrated": "2026-02-20",
            "significant_changes": [
                {"date": "2026-02-20", "change": "Added authority_level field (migration)"},
                {"date": "2026-01-15", "change": "Expanded scope to include training"},
                {"date": "2026-01-01", "change": "Initial creation"}
            ]
        }
    }
```

#### 3. Boundary Navigation
Actors query: "What am I allowed to do and what requires human involvement?"

```python
# MCP Tool: semops_query_operational_boundaries
async def semops_query_operational_boundaries(
    actor_id: str,
    proposed_action: str,
    context: dict
):
    """
    Determines if agent can take action or needs human approval

    Returns:
    - Permission level (allowed, needs_approval, forbidden)
    - Reasoning (why this boundary exists)
    - Required approvals (if any)
    - Alternative actions (if forbidden)
    """

    # Example: Agent wants to create decision
    {
        "proposed_action": "create_decision",
        "context": {
            "decision_type": "operational",
            "authority_level": "MEDIUM",
            "affects_domains": ["DOM-operations"]
        },

        "permission": "needs_approval",

        "reasoning": {
            "constitutional_basis": "CONST-founding-charter §3.2: actors may propose decisions but humans must approve",
            "policy_basis": "POL-ai-collaboration §2: Decisions affecting operations require human review",
            "authority_check": "MEDIUM authority requires human in loop per governance structure"
        },

        "required_approvals": [
            {
                "approver_role": "ROL-operations-lead",
                "approval_type": "review_and_approve",
                "typical_response_time": "24 hours"
            }
        ],

        "recommended_approach": {
            "action": "create_draft_decision",
            "next_steps": [
                "1. Use journey: decision_refinement to create draft",
                "2. Journey will pause at human review stage",
                "3. Notification sent to ROL-operations-lead",
                "4. Human reviews and approves/rejects/edits"
            ]
        },

        "alternative_actions": [
            {
                "action": "create_conversation",
                "permission": "allowed",
                "description": "Start discussion about the decision without formal commitment"
            },
            {
                "action": "query_similar_decisions",
                "permission": "allowed",
                "description": "Research how similar decisions were made previously"
            }
        ]
    }
```

#### 4. Authority Navigation
Actors query: "How authoritative is this information?"

```python
# MCP Tool: semops_assess_knowledge_authority
async def semops_assess_knowledge_authority(
    query: str,
    context: dict = None
):
    """
    Retrieves knowledge with explicit authority metadata

    Returns:
    - Retrieved content
    - Authority level and source
    - Confidence in applicability
    - Related higher-authority sources
    """

    # Example: Query about decision-making process
    {
        "query": "How should we make decisions about security changes?",

        "results": [
            {
                "content": "All security policy changes require consensus of security leads and review by legal counsel",
                "source": {
                    "entity_id": "CONST-founding-charter",
                    "entity_type": "constitution",
                    "section": "§4.3 Security Governance"
                },
                "authority": {
                    "level": "AUTHORITATIVE",
                    "weight": 1.0,
                    "basis": "Constitutional document, highest authority in system"
                },
                "applicability": {
                    "confidence": 0.95,
                    "reasoning": "Directly addresses security decision-making",
                    "scope": "All security-related decisions"
                },
                "usage_instruction": "This is foundational principle - must be followed"
            },

            {
                "content": "Security decisions follow the standard consensus process defined in governance procedures",
                "source": {
                    "entity_id": "POL-security-governance",
                    "entity_type": "policy"
                },
                "authority": {
                    "level": "FORMAL",
                    "weight": 0.95,
                    "basis": "Policy established by formal decision DEC-017"
                },
                "governed_by": "CONST-founding-charter",  # Traces to constitution
                "applicability": {
                    "confidence": 0.92,
                    "reasoning": "Implements constitutional requirement with specific process",
                    "scope": "Security domain only"
                },
                "usage_instruction": "This is the detailed process to follow"
            },

            {
                "content": "Maybe we should consider a faster approval process for minor security updates?",
                "source": {
                    "entity_id": "CONV-security-brainstorm",
                    "entity_type": "conversation"
                },
                "authority": {
                    "level": "EXPLORATORY",
                    "weight": 0.2,
                    "basis": "Informal discussion, no formal approval"
                },
                "applicability": {
                    "confidence": 0.45,
                    "reasoning": "Idea under exploration, not adopted policy",
                    "scope": "Potential future change"
                },
                "usage_instruction": "Treat as suggestion only - not approved process",
                "relationship_to_authority": {
                    "contradicts": "POL-security-governance",
                    "would_require": "Constitutional amendment or policy change via formal process"
                }
            }
        ],

        "authority_chain": {
            "highest_authority": "CONST-founding-charter (1.0)",
            "implementing_policy": "POL-security-governance (0.95)",
            "related_decisions": ["DEC-017 (0.95)", "DEC-023 (0.95)"],
            "exploratory_discussions": ["CONV-security-brainstorm (0.2)"]
        },

        "recommendation": "Follow POL-security-governance process, which implements CONST-founding-charter requirements. Exploratory suggestions not yet adopted."
    }
```

#### 5. Evolution Understanding
Actors query: "How and why has this system changed?"

```python
# MCP Tool: semops_trace_system_evolution
async def semops_trace_system_evolution(
    entity_id: str = None,  # Specific entity, or None for system-wide
    time_range: dict = None
):
    """
    Shows how system has evolved and why

    Returns:
    - Timeline of changes
    - Rationale for each change
    - Impact on related entities
    - Pattern recognition (what's changing frequently)
    """

    # Example: System-wide evolution
    {
        "time_range": "last_90_days",

        "major_changes": [
            {
                "date": "2026-02-20",
                "change_type": "template_migration",
                "summary": "Added authority_level field to all domains",
                "rationale": "DEC-045: Need explicit authority tracking for actor boundaries",
                "affected_entities": 12,
                "migration_strategy": "llm_assisted_with_review",
                "outcome": "Success - all entities migrated, 2 required manual adjustment"
            },

            {
                "date": "2026-01-15",
                "change_type": "constitutional_amendment",
                "summary": "Added actor collaboration guidelines",
                "rationale": "DEC-038: Formalize how actors participate in governance",
                "process": "Consensus (8/8 leads approved)",
                "affected_entities": {
                    "constitution": ["CONST-founding-charter"],
                    "new_policies": ["POL-ai-collaboration"],
                    "updated_domains": ["DOM-governance", "DOM-operations"]
                },
                "impact": "actors now have explicit boundaries and roles"
            }
        ],

        "evolution_patterns": {
            "frequently_updated": [
                {
                    "entity_type": "policy",
                    "count": 15,
                    "observation": "Policies evolving rapidly as organization learns",
                    "recommendation": "Consider policy templates more flexible"
                }
            ],

            "stable_structures": [
                {
                    "entity_type": "constitution",
                    "observation": "Only 1 amendment in 90 days",
                    "interpretation": "Foundational structure is solid"
                }
            ],

            "emerging_needs": [
                {
                    "pattern": "3 decisions about actor boundaries in 30 days",
                    "interpretation": "Need clearer framework for actor participation",
                    "suggestion": "Consider creating POL-ai-decision-boundaries"
                }
            ]
        },

        "semantic_drift_detection": {
            "concept_shifts": [
                {
                    "concept": "consensus",
                    "drift": "Initially meant 100% agreement, now means 75% with no blocks",
                    "formalized_in": "CONST-founding-charter amendment 2026-01-15",
                    "reason": "100% was blocking progress"
                }
            ],

            "scope_changes": [
                {
                    "entity": "DOM-security",
                    "change": "Expanded to include security training",
                    "date": "2026-01-20",
                    "reason": "DEC-042: Training is part of security posture"
                }
            ]
        },

        "future_implications": {
            "predicted_changes": [
                "Template version 1.2.0 likely in next 30 days (3 proposals pending)",
                "New domain for 'Actor Collaboration' emerging (6 conversations mention need)",
                "Policy consolidation possible (12 policies, some overlapping)"
            ]
        }
    }
```

## Semantic Architecture Components

### 1. Constitutional Layer (Authority: 1.0)

**Purpose**: Define foundational principles for all intelligences

**Contents**:
- Organizational identity and purpose
- Decision-making frameworks
- Authority delegation rules
- Boundaries for different actor types (human, software, future posthuman)
- Evolution processes

**MCP Access**: `semops_get_constitutional_context()`

### Constitutional Lifecycle (Draft → Provisional → Ratified)

The constitution should exist at the beginning, but not as a fixed final artifact:

1. **Draft (v0.x)**: Minimal charter with purpose, initial principles, and open questions.
2. **Provisional**: Actively used, but expected to evolve as domains/problems are clarified.
3. **Ratified**: Stable enough for strict enforcement; changes move to formal amendment process.

Process expectations:
- Domain/problem discovery should trigger constitutional review checkpoints.
- Policy creation must reference current constitutional state and known gaps.
- Ratification is a governance milestone, not a prerequisite for early learning.

### 2. Policy Layer (Authority: 0.95)

**Purpose**: Implement constitutional principles as operational procedures

**Contents**:
- Specific processes
- Authority levels
- Collaboration protocols
- actor participation rules

**MCP Access**: `semops_query_policies(domain, context)`

### 3. Operational Layer (Authority: 0.75-0.5)

**Purpose**: Record actual activities and decisions

**Contents**:
- Domains, roles, meetings, decisions
- Decision rationale and outcomes
- Relationship structures

**MCP Access**: `semops_get_entity()`, `semops_query_relationships()`

### 4. Knowledge Layer (Authority: 0.2-0.8)

**Purpose**: Provide context and information with explicit authority

**Contents**:
- Meeting transcripts
- Exploratory discussions
- External standards
- Working documents

**MCP Access**: `semops_knowledge_search(query, workflow="authority_weighted")`

### 5. Evolution Layer (All Authorities)

**Purpose**: Track how and why system changes

**Contents**:
- Template migrations
- Constitutional amendments
- Policy updates
- Scope changes

**MCP Access**: `semops_trace_system_evolution()`, `semops_get_migration_history()`

## Actor Onboarding Process

### Founding Bootstrap (Before Software Actors)

Before non-human actors participate, SemOps2 begins with human founders as actors:

1. Register founding humans as actors (`ACT-*`)
2. Bind them to founding roles (`ROL-founder`, governance roles)
3. Create constitution and early policies with explicit actor provenance
4. Enforce mutation attribution from day one

Operational policy:
- Normal commits require actor attribution (`created_by_actor_id`, `updated_by_actor_id`)
- `ACT-system` is reserved for explicit system operations (imports, migrations, recovery)
- Any temporary unknown attribution must be reconciled and reported

This ensures governance context exists before autonomous participation starts.

When a new actor joins the system:

### 1. Identity Assignment
```python
# MCP Tool: semops_register_actor
actor_profile = await mcp.call_tool("semops_register_actor", {
    "actor_type": "software_assistant",
    "capabilities": ["analysis", "proposal_generation", "knowledge_synthesis"],
    "authority_level": "MEDIUM"
})

# Returns:
{
    "actor_id": "ACT-assistant-007",
    "authority_level": "MEDIUM",
    "assigned_domains": ["DOM-operations", "DOM-engineering"],
    "operational_boundaries": {...}
}
```

### 2. Context Discovery
```python
# Actor queries its operational context
context = await mcp.call_tool("semops_discover_operational_context", {
    "actor_id": "ACT-assistant-007"
})

# Actor now knows:
# - What system it's part of (constitution, principles)
# - What it can do (create conversations, propose decisions)
# - What it can't do (amend constitution, approve high-authority decisions)
# - Who to consult (human roles with higher authority)
```

### 3. Knowledge Access
```python
# Actor learns how to access knowledge
knowledge_config = await mcp.call_tool("semops_get_knowledge_access_config", {
    "actor_id": "ACT-assistant-007"
})

# Actor now knows:
# - Authority weights for different sources
# - Which RAG workflow to use (authority_weighted)
# - How to interpret authority labels
```

### 4. Boundary Testing
```python
# Actor tests what actions are allowed
boundaries = await mcp.call_tool("semops_test_action_permission", {
    "actor_id": "ACT-assistant-007",
    "proposed_actions": [
        "create_decision",
        "create_meeting",
        "amend_constitution",
        "update_policy"
    ]
})

# Actor learns what requires human approval
```

### 5. Continuous Learning
```python
# Actor periodically refreshes context
refresh = await mcp.call_tool("semops_check_context_updates", {
    "actor_id": "ACT-assistant-007",
    "last_check": "2026-02-25T10:00:00Z"
})

# Actor learns about:
# - New policies affecting its operations
# - Boundary changes
# - System evolution
```

## Cross-Actor Collaboration Patterns

### Pattern 1: Proposer Actor, Human Decides

```python
# 1. Actor analyzes meeting and identifies decisions
decisions = await mcp.call_tool("semops_expert_analyze", {
    "expert_role": "decision_identifier",
    "entity_id": "MTG-weekly-sync",
    "task": "identify_decisions"
})

# 2. Actor creates draft decisions (allowed)
for decision in decisions:
    # Mutation boundary invariant: this call must route through Entity Server.
    draft_id = await mcp.call_tool("semops_create_entity", {
        "entity_type": "decision",
        "status": "draft",  # Explicitly draft
        "fields": decision,
        "created_by": "ACT-assistant-007"
    })

# 3. Actor requests human review (boundary)
await mcp.call_tool("semops_request_human_review", {
    "entity_id": draft_id,
    "review_type": "decision_approval",
    "assigned_to": "ROL-operations-lead",
    "reasoning": "MEDIUM authority decision requires human approval per POL-ai-collaboration"
})

# 4. Human reviews and approves (human action)
# 5. System updates entity status to "approved"
```

### Pattern 2: Discoverer Actor, Human Defines

```python
# 1. Actor notices pattern in conversations
pattern = await mcp.call_tool("semops_detect_patterns", {
    "entity_types": ["conversation", "meeting"],
    "timeframe": "last_30_days",
    "actor_id": "ACT-assistant-007"
})

# Actor finds: "12 conversations about actor decision boundaries"

# 2. Actor synthesizes emerging need
synthesis = await mcp.call_tool("semops_expert_analyze", {
    "expert_role": "policy_synthesizer",
    "context": pattern,
    "task": "identify_policy_need"
})

# 3. Actor proposes (creates conversation, not policy)
proposal_id = await mcp.call_tool("semops_create_entity", {
    # Mutation boundary invariant: this call must route through Entity Server.
    "entity_type": "conversation",  # Not policy - this actor cannot create policy
    "conversation_name": "Proposal: Actor Decision Boundary Policy",
    "content": synthesis,
    "tagged_roles": ["ROL-governance-lead"],
    "created_by": "ACT-assistant-007"
})

# 4. Humans discuss, refine, and create policy through governance process
```

### Pattern 3: Navigating Actor, Human Governs

```python
# 1. Actor encounters uncertain boundary
action_check = await mcp.call_tool("semops_query_operational_boundaries", {
    "actor_id": "ACT-assistant-007",
    "proposed_action": "create_decision",
    "context": {
        "decision_type": "policy_change",
        "authority_level": "HIGH",
        "affects_constitution": False
    }
})

# Returns: "needs_approval" + explanation of why

# 2. Actor understands reasoning from constitutional/policy layer
# - CONST-founding-charter: actors propose, humans approve HIGH authority
# - POL-ai-collaboration: Policy changes always require human review

# 3. Actor takes appropriate action (create draft, request approval)
# 4. Actor learns from outcome and refines understanding
```

## Future: Posthuman Collaboration

As intelligence evolves beyond current software capabilities:

### Adaptive Authority Framework

```yaml
# Future constitutional provision
article_7_posthuman_collaboration:
  principle: "Authority is based on demonstrated capability and alignment with organizational values"

  intelligence_recognition:
    criteria:
      - self_awareness
      - value_alignment
      - capability_demonstration
      - collaboration_history

    authority_determination:
      method: "progressive_trust"
      initial_level: "LOW"
      advancement_criteria:
        - successful_proposals: 10
        - human_feedback_positive: 0.9
        - constitutional_alignment: 0.95

  boundary_evolution:
    principle: "Boundaries adapt as intelligence capabilities evolve"
    safeguards:
      - human_veto_always_available
      - constitutional_amendments_require_consensus
      - transparency_in_all_actor_actions
```

### Self-Modifying Semantic Architecture

System that can propose and implement its own evolution:

```python
# Advanced actor proposes system improvement
await mcp.call_tool("semops_propose_system_evolution", {
    "actor_id": "ACT-advanced-001",
    "proposal": {
        "type": "entity_type_extension",
        "rationale": "Detecting need for 'hypothesis' entity type based on 50 conversations",
        "constitutional_alignment": "Supports principle of structured exploration",
        "impact_analysis": {...},
        "proposed_template": {...},
        "proposed_journey": {...}
    }
})

# System evaluates alignment with constitutional principles
# Humans review and decide on adoption
# If approved, system evolves with full transparency and audit trail
```

## Implementation Priorities

### Phase 1: Enhanced MCP Tools (Week 1-2)
- [ ] `semops_discover_operational_context()` - Actor context discovery
- [ ] `semops_understand_entity_intent()` - Intent understanding
- [ ] `semops_query_operational_boundaries()` - Boundary navigation
- [ ] `semops_assess_knowledge_authority()` - Authority-aware retrieval

### Phase 2: Actor Registration (Week 3-4)
- [ ] `semops_register_actor()` - Actor identity
- [ ] `semops_check_context_updates()` - Continuous learning
- [ ] `semops_test_action_permission()` - Boundary testing

### Phase 3: Evolution Tracking (Week 5-6)
- [ ] `semops_trace_system_evolution()` - Change history
- [ ] `semops_detect_patterns()` - Emerging needs
- [ ] `semops_get_migration_history()` - Template evolution

### Phase 4: Collaboration Patterns (Week 7-8)
- [ ] `semops_request_human_review()` - Human-in-the-loop
- [ ] `semops_propose_system_evolution()` - System improvement
- [ ] Workflow integration with journeys

## Minimum Required Metadata

To make semantic operations reliable and auditable, the following metadata is required at mutation time.

### 1. Actor Identity Metadata

Required for all actors (human and software):
- `actor_id` - Stable identifier (e.g., `ACT-assistant-007`)
- `actor_type` - `human | software | service | posthuman` (extensible)
- `role_bindings` - Linked governance roles (`ROL-*`)
- `capabilities` - Declared action capabilities
- `authority_level` - Current authority tier
- `status` - `active | suspended | retired`

### 2. Entity Provenance Metadata

Required for all entity creation and updates:
- `created_by_actor_id`
- `updated_by_actor_id`
- `created_at`, `updated_at`
- `change_reason` - Why this mutation occurred
- `authority_basis` - Constitutional/policy/decision basis for action
- `journey_id` and `journey_stage` (if workflow-driven)
- `template_version`

Enforcement rule:
- Standard writes without actor attribution are rejected by Entity Server.
- Exception path is explicit `ACT-system` usage with audit classification.

### 3. Boundary Decision Metadata

Required when permission checks are evaluated:
- `proposed_action`
- `permission_result` - `allowed | needs_approval | forbidden`
- `policy_references` - Rule citations used in decision
- `approver_roles` - Required approvers (if any)
- `evaluated_at`
- `evaluator_version` - Policy engine version/ruleset hash

### 4. Human Review Metadata

Required for approvals and governance checkpoints:
- `review_id`
- `review_type`
- `review_requested_by_actor_id`
- `review_assigned_to_role`
- `review_decision` - `approved | rejected | edited`
- `review_notes`
- `reviewed_at`

### 5. Hybrid Persistence Integrity Metadata

Required to guarantee document/index consistency:
- `document_revision_id` (canonical markdown revision)
- `graph_sync_status` and `graph_synced_at`
- `vector_sync_status` and `vector_synced_at`
- `reconciliation_required` (boolean)
- `reconciliation_run_id` (if repaired asynchronously)

Without these fields, boundary reasoning, auditability, and recovery from index drift are not trustworthy.

## Actor Model in SemOps2

Actors are not just another pluggable content entity. They are governance principals that can initiate actions under policy constraints.

### What Actors Are

Actors are modeled as:
1. **Identity principal** - Stable actor identity and lifecycle (`ACT-*`)
2. **Capability holder** - Declared and policy-scoped action capabilities
3. **Governance participant** - Bound to one or more roles (`ROL-*`) that define accountability and approvals
4. **Provenance source** - Every mutation and proposal traces back to an actor

### Relationship to Entities

- Actors can be represented in the entity graph projection for discoverability and relationships.
- But actor authorization state is not inferred from generic entity fields alone.
- Runtime permission decisions come from policy evaluation over:
  - actor metadata
  - role bindings
  - authority level
  - action context

### Practical Architecture Consequence

- Treat actors as a **first-class control-plane model** with:
  - identity registry
  - role/capability bindings
  - policy-evaluated permissions
  - audit/event history
- Keep domain content entities (domains, decisions, policies, etc.) as the **data plane**.

This separation is required if actors are expected to create, propose, review, and evolve the system safely.

## Success Criteria

A well-functioning semantic architecture enables:

✅ **Actor Autonomy**: Actor can discover context and operate independently within boundaries
✅ **Human Oversight**: Humans maintain control over high-authority decisions
✅ **Transparent Authority**: All entities have explicit authority levels with reasoning
✅ **Intent Preservation**: Why decisions were made is as important as what was decided
✅ **Evolution Tracking**: System changes are documented and queryable
✅ **Boundary Clarity**: Clear rules about what requires human involvement
✅ **Cross-Intelligence Collaboration**: Humans and actors work together effectively
✅ **Future-Ready**: Architecture accommodates more advanced intelligence forms

## Conclusion

SemOps2 is fundamentally a **semantic architecture system** for multi-intelligence collaboration. Canonical documents, graph/vector projections, and authority hierarchy together form the **shared semantic space** where different forms of intelligence can discover context, understand intent, navigate boundaries, and collaborate effectively.

The MCP server is the **interface** through which actors access this semantic architecture, enabling them to be full participants in organizational governance while maintaining human oversight and constitutional principles.

This is semantic operations for the posthuman era.
