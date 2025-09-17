# Task Management Plan: GitHub Integration

## Goals
- Maintain a single source of truth for agent tasks tied to interface contracts (ICS-001 … ICS-007).
- Mirror the Conway + VSM workflow using GitHub Projects, Issues, and Actions.
- Automate validation, handoff tracking, and SLA enforcement.

## Repository Structure
- `contracts/ICS-###.md` – interface contracts (immutable, versioned).
- `tasks/` – YAML task records (`tasks/ICS-001/001.yaml`).
- `agent_workflow/handoffs/` – completed handoff templates (`handoff_{id}.yaml`).
- `agent_workflow/plan.md` – overall workflow (already merged).
- `agent_workflow/task_management_plan.md` – this plan.
- `agent_workflow/capabilities/agents.yaml` – registry of agent capabilities referenced in task validation.

## Task Record Schema (YAML)
```yaml
task_id: "ICS-001-001"
title: "Add protovalidate schema annotations"
contracts:
  - ICS-001
originating_agent: "Schema Agent"
receiving_agent: "Service Agent"
handoff_id: "HO-20250301-SCHEMA-SERVICE"
priority: high
state: idea|ready|in_progress|review|handoff|done|blocked
sla_hours: 24
dependencies:
  - task_id: "ICS-005-004"
    reason: "Requires CI pipeline for validation"
    status: "completed"
  - external_dependency: "buf_v1.58_release"
    reason: "New protovalidate features needed"
    status: "pending"
expected_outputs:
  - path: "schema/semops/v1/core.proto"
    acceptance: "Protovalidate annotations compiled"
tests_required:
  - cmd: "buf lint schema"
  - cmd: "buf generate schema"
  - cmd: "pytest tests/contracts"
required_capabilities:
  - protobuf_schema_design
  - protovalidate_annotations
  - buf_toolchain
estimated_effort_hours: 4
actual_effort_hours: null
contract_changes:
  - contract: "ICS-001"
    version_from: "v1.2.0"
    version_to: "v1.3.0"
    breaking: true
    migration_guide: "docs/migrations/ICS-001-v1.3.0.md"
risks:
  - type: "breaking_change"
    impact: "high"
    probability: "medium"
    mitigation: "Staged rollout with backward compatibility"
  - type: "sla_breach"
    impact: "medium"
    probability: "low"
    mitigation: "Backup agent assignment"
metrics:
  cycle_time_days: null
  handoff_ack_hours: null
  first_time_acceptance: null
  rework_count: 0
notes: ""
```

## State Machine
```
idea → ready → in_progress → review → handoff → done
                         ↘ blocked
```
- Transitions triggered via Issue workflow or automation.
- `blocked` requires escalation + comment explaining root cause.

## GitHub Project Workflow
- Use a single GitHub Project (e.g., “SemOps Agent Board”).
- Each task YAML has a corresponding Issue created via GitHub Action.
- Columns map to states (Idea, Ready, In Progress, Review, Handoff, Done, Blocked).
- Labels: `ICS-001`, `ICS-002`, …, `priority:high`, `agent:schema`, etc.
- Swimlanes per agent or contract to visualize load.

## Automation & Checks
1. **Task Sync Action**
   - On PR touching `/tasks`, validate YAML schema, ensure contract IDs exist.
   - Validate agent capabilities match required capabilities.
   - Load capability definitions from `agent_workflow/capabilities/agents.yaml`; block if missing or outdated.
   - Create/update GitHub Issues to match YAML (title, description, labels, assignees).
   - Reconciliation job detects and corrects task/issue synchronization drift.
2. **Handoff Validation Action**
   - Confirm matching handoff YAML in `agent_workflow/handoffs/` when state=`handoff`.
   - Check required fields (inputs, outputs, tests, version).
   - Validate handoff completeness against task requirements.
3. **SLA Monitor Action**
   - Flag tasks stuck in `ready` > SLA hours; comment and tag receiving agent + Contract Maintainer.
   - Auto-move unresolved handoffs after SLA to escalation column.
   - Predictive warnings when tasks approach SLA breach.
4. **Metrics Collector Action**
   - Calculate cycle time, acknowledgment time, rework rate, first-time acceptance rate.
   - Store in `metrics/` JSON for dashboards and VSM health monitoring.
   - Track agent utilization and contract stability metrics.
5. **Contract Change Validation**
   - Automated breaking change detection for contract modifications.
   - Semantic versioning enforcement with migration guide requirements.
   - Impact analysis for dependent tasks and agents.
6. **Risk Assessment Automation**
   - Auto-escalate high-impact, high-probability risks to Contract Maintainer.
   - Monitor risk mitigation progress and effectiveness.
   - Generate risk reports for monthly VSM retrospectives.

## Handoff Template Location
- Template in `agent_workflow/handoff-template.yaml`.
- Completed handoffs stored in `agent_workflow/handoffs/HO-*.yaml`.
- Action cross-checks `handoff_id` in task YAML with file name.

## Governance & Reviews
- Contract Maintainer reviews any PR touching `contracts/` or `tasks/` via CODEOWNERS.
- Weekly triage (System 3) moves `idea` → `ready`, assigns owners, verifies dependencies.
- Daily async update: each agent posts statuses referencing task IDs.
- Monthly VSM retrospective uses metrics JSON to validate viability.

## Migration Steps
1. Create directories (`contracts/`, `tasks/`, `metrics/`, `agent_workflow/handoffs/`).
2. Add GitHub Action workflows:
   - `validate-tasks.yml` - Task schema validation and capability checking
   - `handoff-check.yml` - Handoff completeness validation
   - `sla-monitor.yml` - SLA monitoring with predictive warnings
   - `metrics-collector.yml` - Comprehensive metrics collection
   - `contract-validation.yml` - Contract change impact analysis
   - `risk-assessment.yml` - Risk escalation and monitoring
   - `task-sync.yml` - Daily reconciliation of tasks and issues
3. Set up GitHub Project columns + automation (link Issues on creation).
4. Add Issue templates for new tasks and contract changes.
5. Create JSON schema for task YAML validation.
6. Implement agent capability registry and validation.
7. Set up metrics dashboards for VSM health monitoring.
8. Configure CODEOWNERS for contract review governance.
9. Document process in `agent_workflow/README.md`.

## Agent Capability Registry
- Location: `agent_workflow/capabilities/agents.yaml`.
- Contents: list of agents, capabilities, certifications, backup coverage.
- Maintenance: Ops/QA Agent updates registry during onboarding/offboarding; Contract Maintainer reviews changes.
- Validation: Task sync action rejects tasks that reference undefined capabilities.

## Success Indicators
- 100% tasks in `/tasks` mirrored to GitHub Issues (automation parity).
- SLA breaches automatically escalate within 1 hour.
- Metrics show <10% handoff rejection/rework rate.
- Contract violations caught pre-merge 100% of the time.
- Agent utilization remains balanced within 20% variance across agents.
- Contract stability: <5% breaking changes per contract per quarter.
- First-time handoff acceptance rate >90%.
- VSM health score >0.8 based on coordination effectiveness metrics.
- Risk mitigation completion rate >95% within defined timeframes.
- Task/issue synchronization drift detected and corrected within 24 hours.
