# Consolidation Decisions: Collaborative Organization Architecture

This document is a historical record of the consolidation work and design decisions captured on 2026-02-26.
For active execution sequencing, use [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md).

## Current State Analysis

### Documents Created During Exploration

#### Core Configuration Files
1. **collaborative_org_config.yaml** (25K) - Custom entity types, relationships, source authority
2. **decision_types_example.yaml** (18K) - Decision type pattern examples
3. **template_evolution.yaml** (22K) - Template versioning and migration
4. **decision_refinement_workflow.yaml** (26K) - 6-stage decision process

#### Documentation Files
5. **WORKFLOW_UNIFICATION.md** (13K) - Early workflow analysis
6. **EXPERT_WORKFLOW_UNIFICATION.md** (24K) - Journey framework proposal
7. **AGENT_FRAMEWORK_INTEGRATION.md** (59K) - LangGraph integration with full code
8. **template-migration-walkthrough.md** (16K) - Template migration CLI examples
9. **COLLABORATIVE_ORG_SETUP_GUIDE.md** (21K) - Overview and quickstart

## Key Design Decisions

### 1. **Planning YAML + Protobuf-First Implementation** ✅
Use YAML to iterate quickly during planning, then formalize stable contracts in protobuf for implementation.

### 2. **Modular Entity-Journey Units** ✅
Entities and their journeys are paired units that can be brought in from different places

### 3. **CLI-First** ✅
Start with CLI interaction, document other modes as architecture

### 4. **Template Migration is CORE** ✅
Essential for early adoption - templates WILL change rapidly

### 5. **Entity Package Distribution** ✅
Answer: **C** - Start by copying examples directory

### 6. **Template Versioning Scope** ✅
Answer: **B** - Workspace-wide versioning (all entities evolve together)

### 7. **Migration Triggers** ✅
Answer: **A** - Manual migration with explicit control

### 8. **Journey Checkpoints** ✅
Answer: **C** - Both LangGraph state AND entity metadata

### 9. **Actor Bootstrap + Attribution Policy** ✅
Founding humans are registered as actors first, and all normal mutations require actor attribution. `ACT-system` is restricted to explicit system operations.

### 10. **Opinionated Democratic + Earth-Positive Stance** ✅
Primary near-term use case is post-human democratic organizations with human decision sovereignty, taiji boundary-setting, and AI used as coaching support rather than governance replacement.

### 11. **Micro-to-Macro Democracy Mission** ✅
Use micro-scale democratic practice (teams/organizations) as the development ground for practices that can improve macro-scale democracy.

### 12. **Self-Referential System Design** ✅
SemOps is used to design SemOps: architecture domains/problems produce decisions, constitution defines boundaries, and actor-driven evolution remains governance-bounded.

### 13. **Fine-Grained ADR + Decision-to-Diff Traceability** ✅
Major proposals are modeled as bundles of small decisions, and each decision can link to explicit target-document change references.

## Revised Understanding: Modular Entity-Journey Units

Each entity type is a **self-contained package**:

```
domain_entity_package/
├── entity_definition.yaml      # Entity type config
├── journey_definition.yaml     # Refinement journey
├── templates/
│   └── v1.0.0/
│       ├── create.md.j2
│       └── analyze.md.j2
└── migration_rules.yaml        # How to migrate between template versions
```

## Final Structure

```
/workspace
├── docs/
│   ├── IDL_ARCHITECTURE.md (existing - protobuf interfaces)
│   ├── INTERFACE_CONTRACT.md (existing - protobuf consumer contract)
│   └── COLLABORATIVE_ORG_ARCHITECTURE.md (NEW - consolidated collaborative-org design)
│
└── examples/
    ├── config/
    │   └── collaborative_org_config.yaml (REVISED - imports packages)
    │
    ├── entity_packages/
    │   ├── domain/
    │   │   ├── entity_definition.yaml
    │   │   ├── journey_definition.yaml
    │   │   ├── migration_rules.yaml
    │   │   └── templates/
    │   │       └── v1.0.0/
    │   │
    │   ├── decision/
    │   │   ├── entity_definition.yaml
    │   │   ├── journey_definition.yaml
    │   │   ├── migration_rules.yaml
    │   │   └── templates/
    │   │
    │   ├── policy/
    │   │   └── ...
    │   │
    │   └── constitution/
    │       └── ...
    │
    ├── COLLABORATIVE_ORG_QUICKSTART.md (NEW - practical guide)
    └── TEMPLATE_EVOLUTION_GUIDE.md (NEW - migration strategy)
```

## Action Plan

### Phase 1: Create Entity Package Structure
1. Create `/workspace/examples/entity_packages/` directory
2. Create `domain/` package
3. Create `decision/` package (convert from decision_refinement_workflow.yaml)
4. Create `policy/` and `constitution/` packages

### Phase 2: Consolidate Architecture Document
Create COLLABORATIVE_ORG_ARCHITECTURE.md with:
- Entity-journey framework concept
- Modular entity packages
- LangGraph CLI integration
- Template evolution system (CRITICAL feature)
- Authority-weighted knowledge
- Example journey flow (CLI-based)

### Phase 3: Update Main Config
Revise collaborative_org_config.yaml to:
- Import entity packages
- Define cross-entity relationships
- Configure source authority weights
- Configure RAG workflows

### Phase 4: Create Practical Guides
1. Create TEMPLATE_EVOLUTION_GUIDE.md (consolidate migration concepts)
2. Create COLLABORATIVE_ORG_QUICKSTART.md (streamlined how-to)

### Phase 5: Remove Superseded Documents
1. Delete WORKFLOW_UNIFICATION.md
2. Delete EXPERT_WORKFLOW_UNIFICATION.md
3. Delete AGENT_FRAMEWORK_INTEGRATION.md
4. Delete COLLABORATIVE_ORG_SETUP_GUIDE.md
5. Delete decision_types_example.yaml
6. Delete template-migration-walkthrough.md
7. Delete decision_refinement_workflow.yaml (converted to package)
8. Delete template_evolution.yaml (split into per-entity rules)

## Success Criteria

After cleanup:
- ✅ 4 entity packages (domain, decision, policy, constitution)
- ✅ 1 architecture document (consolidated)
- ✅ 1 main config (imports packages)
- ✅ 2 practical guides (quickstart, template evolution)
- ✅ Clear modular structure
- ✅ Template evolution as first-class feature
- ✅ Ready for rapid iteration during early use
