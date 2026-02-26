# Collaborative Organization Quickstart

Get started with SemOps2 for transparent collaborative organization governance in 15 minutes.

## What You'll Set Up

- **Entity Packages**: Domain, Decision, Policy, Constitution with interactive journeys
- **Authority-Weighted Knowledge**: Different sources have different validity levels
- **Template Evolution**: Controlled template changes with LLM-assisted migration
- **CLI Workflows**: Interactive entity creation and refinement

## Prerequisites

```bash
# Install SemOps2
pip install semops2

# Start Neo4j (for entity and knowledge graphs)
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password \
  neo4j:latest

# Set environment variable
export NEO4J_PASSWORD=your_password
```

## Step 1: Initialize Workspace

```bash
# Create workspace directory
mkdir -p ~/my-org
cd ~/my-org

# Copy entity packages
cp -r /path/to/semops2/examples/entity_packages .semops/entity_packages/

# Copy config
cp /path/to/semops2/examples/config/collaborative_org_config_v2.yaml .semops/config.yaml

# Initialize
semops init

✓ Workspace initialized
✓ Entity packages loaded: domain, decision, policy, constitution
✓ Storage backends connected
✓ Template version: 1.0.0
```

## Step 2: Create Your First Domain

### Interactive Journey

```bash
$ semops journey start domain-definition --name "Governance"

🚀 Starting journey: domain_definition
📍 Stage: draft_creation

What is the purpose of this domain?
> Establish and maintain organizational governance structures

✓ Draft created

📍 Stage: scope_clarification
🤖 AI is analyzing your draft...

AI Proposal:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IN SCOPE:
• Constitutional matters
• Policy development
• Decision-making processes

OUT OF SCOPE:
• Day-to-day operations

Related Domains:
• (None identified - this appears to be foundational)

Suggested Stakeholders:
• Governance Lead (accountable)

Authority Level: HIGH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Actions:
  [1] Accept AI proposal
  [2] Edit and refine
  [3] Start over

Your choice: 1
✓ Scope approved

📍 Stage: resource_identification
🤖 Searching for relevant resources...

No existing resources found (new workspace).

Actions:
  [1] Skip for now
  [2] Add custom resources

Your choice: 1
✓ Resources selection complete

📍 Stage: stakeholder_mapping
...

✅ Domain created: DOM-governance

View: semops domain get DOM-governance
```

## Step 3: Create Constitution

```bash
$ semops journey start constitution-ratification --name "Founding Charter"

# Interactive process to create foundational governance document
# ... (similar to domain journey)

✅ Constitution created: CONST-founding-charter
```

## Step 4: Record a Meeting

```bash
# Create meeting entity
$ semops meeting create founding-meeting \
  --name "Founding Meeting" \
  --part-of DOM-governance \
  --date "2026-02-26"

✅ Meeting created: MTG-founding-meeting

# Add transcription as knowledge source
$ semops knowledge add-source \
  --source-type meeting_records \
  --url file://./transcriptions/founding-meeting.md \
  --entity-id MTG-founding-meeting

✓ Transcription processed: 3 chunks, authority weight: 0.75
```

## Step 5: Extract Decisions from Meeting

```bash
$ semops journey start decision-refinement MTG-founding-meeting

📍 Stage: identify_decisions
🤖 Analyzing meeting transcription...

Found 3 potential decisions:
  1. "Adopt consensus-based decision making for constitutional changes"
  2. "Establish quarterly domain reviews"
  3. "Create access control policy"

📍 Stage: review_identified_decisions

Review each decision:

[1/3] "Adopt consensus-based decision making..."
  Clarity: Clear
  Actions: [Confirm] [Merge] [Split] [Reject] [Clarify]

Your choice: Confirm
✓ Decision confirmed

[2/3] "Establish quarterly domain reviews"
...

📍 Stage: clarify_decision (for each confirmed)
🤖 Creating clear decision statement...

AI Proposal:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Decision: "Adopt consensus-based decision making for all
           constitutional amendments and foundational policy changes"

Scope Included:
• Constitutional amendments
• Foundational policies (authority: HIGH)
• Core governance structures

Scope Excluded:
• Operational decisions (use separate process)
• Day-to-day policy updates

Desired Outcome:
"Ensure broad agreement on foundational changes while maintaining
 ability to make progress"

Assumptions:
• Consensus means 75% approval with no blocking objections
• Process applies to ~5-10 decisions per year
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Actions: [Approve] [Edit] [Reject]
Your choice: Approve

# ... journey continues through options, stakeholders, readiness ...

✅ Decision created: DEC-001 (status: ready)
✅ Decision created: DEC-002 (status: ready)
✅ Decision created: DEC-003 (status: draft)

Summary:
  Source: MTG-founding-meeting
  Decisions created: 3 (2 ready, 1 draft)
```

## Step 6: Create Policy from Decision

```bash
$ semops journey start policy-development --name "Access Control Policy"

# ... interactive journey ...

✅ Policy created: POL-001

# Establish relationship: decision establishes policy
$ semops relationship add establishes DEC-003 POL-001

✓ Relationship added: DEC-003 --[establishes]--> POL-001
```

## Step 7: Query with Authority Weighting

```bash
$ semops knowledge search "decision making process" \
  --workflow authority_weighted

Results (authority-weighted):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[AUTHORITATIVE 1.00] CONST-founding-charter
  "All constitutional changes require consensus-based approval..."

[FORMAL 0.95] DEC-001
  "Adopt consensus-based decision making for all constitutional
   amendments and foundational policy changes"

[FORMAL 0.95] POL-001
  "Policy decisions follow the process defined in the constitution..."

[DOCUMENTED 0.75] MTG-founding-meeting
  "Discussion of decision-making approaches, with agreement on
   consensus model for foundational changes"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Constitutional sources prioritized over meeting notes.
```

## Step 8: Template Evolution (After 3 Months)

```bash
# Check if entities need migration
$ semops migrate check

Found 5 domain entities using template v1.0.0
Workspace version: 1.1.0 (added authority_level field)
Migration recommended.

# Preview migration
$ semops migrate preview --entity-type domain

# Run migration with review
$ semops migrate run --entity-type domain --strategy llm_assisted_with_review

# LLM infers authority levels, you approve/edit each

✅ Migrated 5/5 entities to v1.1.0
```

## Common Commands

### Entity Management
```bash
# List entities
semops domain list
semops decision list --status ready
semops policy list

# Get entity details
semops domain get DOM-governance
semops decision get DEC-001

# Analyze entity
semops domain analyze DOM-governance
```

### Journey Management
```bash
# Start journey
semops journey start domain-definition --name "Engineering"
semops journey start decision-refinement MTG-weekly-sync

# Check journey status
semops journey status <thread-id>

# Resume paused journey
semops journey resume <thread-id>

# List available journeys
semops journey list
```

### Knowledge Operations
```bash
# Add knowledge source
semops knowledge add-source \
  --source-type external_standards \
  --url https://example.com/standards.pdf \
  --entity-id DOM-governance

# Search with authority weighting
semops knowledge search "query" --workflow authority_weighted

# Search without authority bias
semops knowledge search "query" --workflow semantic_search
```

### Relationship Management
```bash
# Add relationship
semops relationship add establishes DEC-001 POL-001
semops relationship add governed_by POL-001 CONST-founding-charter

# List relationships
semops relationship list --from DEC-001
semops relationship list --type establishes

# Visualize entity graph
semops graph visualize DOM-governance --depth 2
```

### Migration Operations
```bash
# Check for outdated entities
semops migrate check

# Preview migration
semops migrate preview --entity-type domain

# Run migration
semops migrate run --entity-type domain --strategy llm_assisted_with_review

# Rollback if needed
semops migrate rollback --migration-id <id>
```

## Directory Structure

After setup, your workspace looks like:

```
~/my-org/
├── .semops/
│   ├── config.yaml                    # Main configuration
│   ├── entity_packages/               # Entity type packages
│   │   ├── domain/
│   │   ├── decision/
│   │   ├── policy/
│   │   └── constitution/
│   ├── chromadb/                      # Vector store
│   ├── checkpoints/                   # Journey state
│   │   └── langgraph.db
│   ├── backups/                       # Migration backups
│   │   └── migrations/
│   └── logs/                          # System logs
│
├── domains/                           # Domain entities
│   ├── governance/
│   │   └── domain.md
│   └── operations/
│       └── domain.md
│
├── decisions/                         # Decision entities
│   ├── adopt-consensus-process/
│   │   └── decision.md
│   └── establish-quarterly-reviews/
│       └── decision.md
│
├── policies/                          # Policy entities
│   └── access-control/
│       └── policy.md
│
├── constitution/                      # Constitutional docs
│   └── founding-charter/
│       └── constitution.md
│
└── meetings/                          # Meeting records
    └── founding-meeting/
        └── meeting.md
```

## Next Steps

1. **Read the Architecture**: [COLLABORATIVE_ORG_ARCHITECTURE.md](../docs/COLLABORATIVE_ORG_ARCHITECTURE.md)
2. **Understand Template Evolution**: [TEMPLATE_EVOLUTION_GUIDE.md](TEMPLATE_EVOLUTION_GUIDE.md)
3. **Explore Entity Packages**: `/workspace/examples/entity_packages/`
4. **Customize for Your Org**: Edit config, journeys, templates
5. **Join Community**: Share your entity packages with others

## Troubleshooting

### "Entity package not found"
```bash
# Verify packages copied correctly
ls .semops/entity_packages/
# Should show: domain, decision, policy, constitution

# Re-copy if needed
cp -r /path/to/semops2/examples/entity_packages .semops/
```

### "Neo4j connection failed"
```bash
# Check Neo4j running
docker ps | grep neo4j

# Check password set
echo $NEO4J_PASSWORD

# Test connection
semops storage test
```

### "Journey fails to start"
```bash
# Check journey exists
semops journey list

# Check logs
tail -f .semops/logs/semops.log

# Validate config
semops config validate
```

## Getting Help

- **Documentation**: `/workspace/docs/`
- **Examples**: `/workspace/examples/`
- **Issues**: [GitHub Issues](https://github.com/semops/semops2/issues)
- **Community**: [Discord](https://discord.gg/semops)

## Summary

You now have:
- ✅ Interactive entity journeys with AI assistance
- ✅ Authority-weighted knowledge retrieval
- ✅ Template evolution with LLM-assisted migration
- ✅ Transparent operational records in entity graph

Start creating entities, recording meetings, making decisions, and building your collaborative organization's knowledge base!
