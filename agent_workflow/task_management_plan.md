# Task Management Plan: MVP GitHub Integration

## Goals
- Establish immediate task visibility between agents using GitHub Issues
- Implement Conway + VSM workflow with minimal complexity
- Create foundation for future automation and enhancement

## MVP Approach: GitHub Issues + Labels

### Repository Structure (Minimal)
- `contracts/ICS-###.md` – interface contracts (created as needed)
- GitHub Issues – all task tracking
- GitHub Project Board – visual workflow management
- Issue comments – handoff documentation

## Issue Format (GitHub Issues)

### Issue Title Format
```
[ICS-001] Add protovalidate schema annotations
```

### Issue Labels (Required)
```
contract:ICS-001          # Links to interface contract
agent:schema             # Responsible agent
status:ready             # Current state
priority:high            # Priority level
```

### Issue Body Template
```markdown
**Receiving Agent:** @service-agent
**Contract:** ICS-001 (Schema↔Service)

**Expected Outputs:**
- `schema/semops/v1/core.proto` with protovalidate annotations

**Tests Required:**
- `buf lint schema`
- `buf generate schema`
- `pytest tests/contracts`

**Dependencies:**
- [ ] CI pipeline setup (ICS-005)

**Handoff From:** @schema-agent
```

## State Management (Labels)

### Status Labels
```
status:idea           # New concept, needs planning
status:ready          # Ready to start work
status:in-progress    # Currently being worked on
status:review         # Completed, needs review
status:handoff        # Ready to hand off to next agent
status:done           # Completed and accepted
status:blocked        # Cannot proceed, needs help
```

### State Transitions
- **Manual:** Change labels to move between states
- **Automatic:** GitHub Project automation moves issues between columns
- **Blocked:** Requires comment explaining root cause and mention @contract-maintainer

## GitHub Project Board Setup

### Single Project Board: "SemOps Agent Workflow"
- **Columns:** Idea | Ready | In Progress | Review | Handoff | Done | Blocked
- **Automation:** Issues move between columns when status labels change
- **Views:**
  - Board view for workflow visualization
  - Table view grouped by agent or contract for workload visibility

### Required Labels
```
# Contract Labels
contract:ICS-001, contract:ICS-002, contract:ICS-003, etc.

# Agent Labels
agent:schema, agent:service, agent:cli, agent:knowledge, agent:ops

# Status Labels (see State Management section)
status:idea, status:ready, etc.

# Priority Labels
priority:critical, priority:high, priority:medium, priority:low
```

## Handoff Protocol (Comments)

### When Handing Off Work
Comment on the issue with handoff information:

```markdown
@receiving-agent This work is ready for handoff.

**Inputs Completed:**
- ✅ schema/semops/v1/core.proto updated with protovalidate annotations
- ✅ buf lint passes

**Your Next Steps:**
- [ ] Implement service validation using new annotations
- [ ] Update service tests to validate protovalidate rules
- [ ] Update documentation

**Tests to Run:**
- `buf generate && pytest tests/contracts`
- `scripts/test-runner.sh full`

**Questions/Blockers:** None
```

### Actions After Handoff Comment
1. Change label from `status:handoff` to `status:done`
2. Receiving agent changes to `status:ready` or `status:in-progress`
3. Create new issue for receiving agent's work if needed

## Governance & Reviews (Manual)

### Weekly Triage Meeting
- **Duration:** 15 minutes maximum
- **Participants:** All agents + Contract Maintainer
- **Agenda:**
  1. Review `status:idea` issues → assign agents, move to `status:ready`
  2. Check `status:blocked` issues → resolve or escalate
  3. Identify SLA violations → immediate action
  4. Quick workload balance check

### Daily Async Updates
- Agents comment on their assigned issues with progress
- Mention blockers or delays immediately
- Tag other agents when dependencies are ready

### Contract Changes
- Create GitHub issue for contract modifications
- Link to affected tasks
- Contract Maintainer approval required before implementation

## MVP Implementation Steps

### Immediate Setup (Start Today)
1. **Create GitHub Project Board**
   - Name: "SemOps Agent Workflow"
   - Add columns: Idea, Ready, In Progress, Review, Handoff, Done, Blocked
   - Enable automation to move issues based on label changes

2. **Create Required Labels**
   - Status labels: `status:idea`, `status:ready`, etc.
   - Agent labels: `agent:schema`, `agent:service`, etc.
   - Contract labels: `contract:ICS-001`, `contract:ICS-002`, etc.
   - Priority labels: `priority:critical`, `priority:high`, etc.

3. **Create Issue Template**
   - Basic template for consistent issue creation
   - Include required fields: receiving agent, contract, outputs, tests

4. **Start Creating Issues**
   - Begin with current work items
   - Use consistent title format: `[ICS-001] Task description`
   - Apply appropriate labels

### Growth Path (Add Later)
- Issue templates for different task types
- Basic GitHub Actions for label automation
- Simple metrics collection from GitHub API
- YAML task files (if needed)
- Advanced automation and validation

## Success Indicators (MVP)

### Immediate Goals
- ✅ **Visibility:** All agent work visible in GitHub Project Board
- ✅ **Handoffs:** Clear handoff documentation in issue comments
- ✅ **Progress:** Status labels accurately reflect current state
- ✅ **Responsibility:** Clear agent assignment for each task
- ✅ **Conway's Law:** Tasks properly mapped to interface contracts

### Measurable Outcomes
- All current work items tracked as GitHub Issues
- Handoffs completed with comment-based documentation
- Weekly triage meetings resolve blockers and assign new work
- No work falls through the cracks due to lack of visibility
- Agents can easily see their current workload and dependencies

### Growth Indicators
- System works smoothly for manual processes
- Team requests automation for repetitive tasks
- Clear patterns emerge for issue types and workflows
- Handoff quality improves through standardized comments
- Conway's Law/VSM benefits become evident through better coordination
