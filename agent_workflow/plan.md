# Agent Workflow Plan

## Purpose
- Establish shared coordination scaffolding so specialized SemOps agents can operate safely.
- Map agent responsibilities to Conway-aligned interfaces and the Viable System Model (VSM).

## Phase 0 – Foundations (Week 1)
1. **Contract Baseline**
   - Draft ICS-001 … ICS-007 interface contracts (schema↔service, service↔CLI, templates, knowledge ops, docs, tooling, handoffs).
   - Store contracts in `contracts/` with version headers and `#contract-change` workflow.
2. **Shared Tooling Guardrails**
   - Finalize `scripts/test-runner.sh`, Buf pipelines, and git hooks.
   - Add CI job that hashes contract docs and enforces handoff notes.
3. **Handoff Template**
   - Create `handoffs/handoff-template.md` with required fields (inputs, outputs, tests, contract version, next agent).

## Phase 1 – Agent Roles (Weeks 2–3)
- **Schema Agent (System 1a)**: Owns `.proto`, Protovalidate annotations, `buf.lock` updates.
- **Service Agent (System 1b)**: Maintains gRPC server + validation integration.
- **CLI Agent (System 1c)**: Builds dynamic commands, ensures CLI ↔ service contract.
- **Knowledge Agent (System 1d)**: Manages templates, ingestion, RAG configuration.
- **Ops/QA Agent (System 1e)**: Runs pipelines, maintains contract tests, release packaging.
- Publish RACI matrix linking each agent to the relevant contracts.

## Phase 2 – Coordination & Governance (Weeks 4–5)
1. **System 2 (Coordination)**
   - Stand up lightweight Kanban/issue labels tied to contracts.
   - Automate notifications (e.g., Slack/webhook) when contract versions change.
2. **System 3 (Control)**
   - Define Contract Maintainer rotation, merge gatekeepers, audit cadence.
   - Extend CI to block merges lacking updated handoff entries.
3. **System 4 (Intelligence)**
   - Architecture Working Group monitors feature roadmap, backlog grooming, future interfaces.
4. **System 5 (Policy)**
   - Document SemOps charter: “Proto-first, agent-safe, VSM-aligned”.

## Phase 3 – Execution Loop (Ongoing)
1. Agent picks task → references contract version.
2. Runs required tooling, updates artifacts, prepares handoff note.
3. Next agent confirms receipt; QA agent verifies pipeline.
4. Monthly VSM retrospective: ensure coordination/control layers remain viable.

## Success Metrics
- 100% contract changes follow `#contract-change` checklist.
- CI success rate > 95% (failures only for real regressions).
- Average handoff acknowledgment < 1 business day.
- Quarterly audit shows no drift between documented contracts and code.

## Open Questions
- How to prioritize agent staffing (humans vs. automated LLM agents)?
- Do we need an additional contract for external integrations (REST/MCP) yet?
- Should handoff records live in Git or an external coordination system?

