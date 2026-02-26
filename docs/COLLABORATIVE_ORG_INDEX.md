# Collaborative Organization with SemOps2

This directory contains the complete architecture and implementation plan for using SemOps2 to support collaborative organization governance.

## 🚀 Start Here

**New to this architecture?** Start with these in order:

1. **[PLANNING_COMPLETE.md](PLANNING_COMPLETE.md)** - Executive summary of what was created
2. **[examples/COLLABORATIVE_ORG_QUICKSTART.md](examples/COLLABORATIVE_ORG_QUICKSTART.md)** - Get started in 15 minutes
3. **[docs/COLLABORATIVE_ORG_ARCHITECTURE.md](docs/COLLABORATIVE_ORG_ARCHITECTURE.md)** - Complete architecture reference

## 📚 Documentation

### Core Architecture
- **[docs/COLLABORATIVE_ORG_ARCHITECTURE.md](docs/COLLABORATIVE_ORG_ARCHITECTURE.md)** (31KB)
  - Entity-Journey Framework
  - Modular entity packages
  - Template evolution system
  - Authority-weighted knowledge
  - LangGraph integration
  - 3 detailed workflow examples

### Practical Guides
- **[examples/COLLABORATIVE_ORG_QUICKSTART.md](examples/COLLABORATIVE_ORG_QUICKSTART.md)** (12KB)
  - 15-minute setup
  - First domain creation
  - Meeting recording and decision extraction
  - Common commands

- **[examples/TEMPLATE_EVOLUTION_GUIDE.md](examples/TEMPLATE_EVOLUTION_GUIDE.md)** (19KB)
  - Why template evolution is CRITICAL
  - 4 migration strategies
  - Complete CLI workflows
  - Troubleshooting

### Entity Packages
- **[examples/entity_packages/README.md](examples/entity_packages/README.md)**
  - Package structure explained
  - Using existing packages
  - Creating custom packages
  - Best practices

### Planning Documents
- **[PLANNING_COMPLETE.md](PLANNING_COMPLETE.md)** - Consolidation summary
- **[docs/PLANNING_AUDIT.md](docs/PLANNING_AUDIT.md)** - Design decisions and rationale
- **[docs/decisions/](docs/decisions/)** - Auditable architecture decision records (ADRs)

## 📦 Entity Packages

Self-contained packages with entity definitions, interactive journeys, and templates:

### [examples/entity_packages/domain/](examples/entity_packages/domain/)
Define operational domains with AI-assisted scope clarification and stakeholder mapping

**Journey**: draft → scope clarification → resource identification → stakeholder mapping → finalize

### [examples/entity_packages/decision/](examples/entity_packages/decision/)
Extract and refine decisions from meeting/conversation content

**Journey**: identify decisions → clarify each → explore options → map stakeholders → assess readiness → create entity

### [examples/entity_packages/policy/](examples/entity_packages/policy/)
Develop organizational policies with AI assistance

**Journey**: draft → AI enrichment → review → finalize

### [examples/entity_packages/constitution/](examples/entity_packages/constitution/)
Create foundational governing documents

**Journey**: draft → stakeholder consultation → review → voting → finalize

## ⚙️ Configuration

- **[examples/config/collaborative_org_config_v2.yaml](examples/config/collaborative_org_config_v2.yaml)**
  - Entity package imports
  - Relationship types
  - Source types with authority weights
  - RAG workflows
  - Storage backends
  - Migration configuration

## 🔑 Key Concepts

### Entity-Journey Framework
Interactive, multi-stage entity creation with AI assistance and human review at each stage.

**Traditional**:
```bash
semops domain create foo --name "Foo"
```

**Journey-based**:
```bash
semops journey start domain-definition --name "Foo"
# Interactive process with AI guidance
```

### Authority-Weighted Knowledge
Different sources have different validity:
- Constitutional documents: **1.0** (highest)
- Formal decisions: **0.95**
- Meeting records: **0.75**
- Working documents: **0.5**
- Informal discussions: **0.4**
- Exploratory notes: **0.2** (lowest)
- External standards: **0.8**

RAG workflows prioritize authoritative sources.

### Template Evolution
**CRITICAL for early adoption**: Templates change rapidly as organizations learn.

System provides:
- LLM-assisted field inference
- Human review checkpoints
- Automatic backups
- Rollback capability
- No data loss

### Modular Packages
Entity types and their journeys are packaged together:
```
domain/
├── entity_definition.yaml
├── journey_definition.yaml
├── migration_rules.yaml
└── templates/v1.0.0/
```

## 📊 Example Workflows

### 1. Establishing Organization
```bash
semops init --config examples/entity_packages
semops journey start constitution-ratification --name "Charter"
semops journey start domain-definition --name "Governance"
semops meeting create founding-meeting --part-of DOM-governance
semops journey start decision-refinement MTG-founding-meeting
```

### 2. Template Evolution
```bash
# Bump version to 1.1.0 (adds authority_level field)
semops migrate check
semops migrate preview --entity-type domain
semops migrate run --entity-type domain --strategy llm_assisted_with_review
# LLM infers values, you approve/edit each
```

### 3. Authority-Weighted Decisions
```bash
semops journey start decision-refinement MTG-security-review
# AI retrieves with authority weighting:
#   [AUTHORITATIVE 1.0] Constitution
#   [FORMAL 0.95] Policy
#   [EXTERNAL 0.8] Standards
#   [EXPLORATORY 0.2] Notes
# Decision informed by authoritative sources
```

## 🛠️ Implementation Status

**Planning**: ✅ Complete (this document set)

**Implementation phases**:
- [ ] Phase 1: Core entity packages (Week 1-2)
- [ ] Phase 2: Journey orchestration (Week 3-4)
- [ ] Phase 3: Template evolution (Week 5-6)
- [ ] Phase 4: Authority-weighted RAG (Week 7-8)
- [ ] Phase 5: Integration testing (Week 9-10)

See [PLANNING_COMPLETE.md](PLANNING_COMPLETE.md) for detailed roadmap.

## 🎯 Design Principles

1. **Transparent Operational Records** - All activities captured in canonical documents, with graph/vector indexes as derived projections
2. **Human-AI Collaboration** - AI assists, humans decide
3. **Authority Hierarchy** - Different sources have different validity
4. **Rapid Evolution** - Templates change without chaos
5. **Modular Design** - Self-contained entity packages
6. **CLI-First** - Command-line interface for all operations

## 🤝 Contributing

### Creating Custom Entity Packages

1. Copy package structure from existing packages
2. Define entity type, journey, migration rules
3. Create templates
4. Test thoroughly
5. Share with community

See [examples/entity_packages/README.md](examples/entity_packages/README.md) for details.

## 📞 Getting Help

- **Documentation**: This directory
- **Issues**: [GitHub Issues](https://github.com/semops/semops2/issues)
- **Community**: [Discord](https://discord.gg/semops)

## 🗺️ Navigation

```
/workspace/
├── COLLABORATIVE_ORG_INDEX.md ← YOU ARE HERE
├── PLANNING_COMPLETE.md
│
├── docs/
│   ├── COLLABORATIVE_ORG_ARCHITECTURE.md ← Core architecture
│   └── PLANNING_AUDIT.md
│
└── examples/
    ├── COLLABORATIVE_ORG_QUICKSTART.md ← Start here
    ├── TEMPLATE_EVOLUTION_GUIDE.md
    │
    ├── config/
    │   └── collaborative_org_config_v2.yaml ← Main config
    │
    └── entity_packages/ ← Modular entity definitions
        ├── README.md
        ├── domain/
        ├── decision/
        ├── policy/
        └── constitution/
```

## 📝 Quick Reference

### Common Commands
```bash
# Initialize workspace
semops init --config examples/entity_packages

# Start interactive journey
semops journey start domain-definition --name "Domain Name"
semops journey start decision-refinement MTG-meeting-id

# Check/run migrations
semops migrate check
semops migrate run --entity-type domain --strategy llm_assisted_with_review

# Query with authority weighting
semops knowledge search "query" --workflow authority_weighted

# Manage relationships
semops relationship add establishes DEC-001 POL-001
```

### File Paths
- Architecture: [docs/COLLABORATIVE_ORG_ARCHITECTURE.md](docs/COLLABORATIVE_ORG_ARCHITECTURE.md)
- Quickstart: [examples/COLLABORATIVE_ORG_QUICKSTART.md](examples/COLLABORATIVE_ORG_QUICKSTART.md)
- Entity packages: [examples/entity_packages/](examples/entity_packages/)
- Config: [examples/config/collaborative_org_config_v2.yaml](examples/config/collaborative_org_config_v2.yaml)

---

**Status**: Planning complete, ready for implementation
**Date**: 2026-02-26
**Context**: ~100K tokens of careful planning and consolidation

Ready to build transparent, authority-aware collaborative organizations with AI-assisted governance! 🚀
