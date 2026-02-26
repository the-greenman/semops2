# ADR-0003: Actor-Expert Invocation Contract and Resolution Metadata

- **Status:** Accepted
- **Date:** 2026-02-26
- **Owners:** Architecture / Platform Governance
- **Decision Type:** Control-plane to expert-runtime contract

## Context

SemOps2 defines actors as control-plane principals and experts as analysis personas, but prior examples and schemas were inconsistent:

- mixed expert invocation styles (`expert_role` vs `expert_type`);
- missing or optional actor attribution in expert requests;
- no canonical contract for role-alias resolution metadata (`requested_role` to resolved expert key);
- inconsistent auditability across MCP, gRPC, and journey execution paths.

Without a single invocation contract, advanced external-agent behavior cannot be enforced or audited reliably.

## Decision

SemOps2 adopts one actor-expert invocation contract across CLI/API/MCP/journeys:

1. **Actors are required for expert execution**
   - Expert analysis requests must include `actor_id` (`ACT-*` pattern).
   - Anonymous expert execution is not supported for mutating or governance-relevant workflows.

2. **Expert selector model**
   - Requests may specify either:
     - `expert_type` (explicit config key), or
     - `requested_role` (journey/agent alias resolved at runtime).
   - If `requested_role` is provided, runtime resolves it using package-first precedence.

3. **Deterministic resolution precedence**
   - `entity_packages/<entity>/experts.yaml`
   - `.semops/config/expert_types.yaml`
   - built-in core fallback experts

4. **Resolution metadata is first-class**
   - Every expert response includes resolution metadata:
     - `requested_role` (if supplied),
     - `resolved_expert_type`,
     - `resolution_source`,
     - `resolver_version`,
     - `resolution_path`.

5. **Mutation boundary remains unchanged**
   - Expert outputs may propose changes, but all writes still flow through `EntityService` with `created_by_actor_id` / `updated_by_actor_id`.

## Non-Goals

- This ADR does not define LLM provider internals.
- This ADR does not replace template/journey authoring conventions.
- This ADR does not permit direct writes from expert tooling to derived stores.

## Alternatives Considered

### A. Keep role-only invocation

Rejected due to:
- ambiguous cross-interface semantics,
- weak interoperability with protobuf and typed tooling,
- poor observability of resolution behavior.

### B. Require expert_type only (no role alias)

Rejected due to:
- reduced ergonomics for journey authors,
- weaker abstraction for pluggable package contributors,
- tighter coupling between journey text and core expert catalogs.

## Consequences

### Positive

- One enforceable contract across gRPC/FastAPI/MCP.
- Stronger audit trail for advanced-agent behavior.
- Clear boundary between actor authority and expert specialization.
- Safer future evolution toward multi-agent orchestration.

### Costs

- Additional request/response metadata handling.
- Need parity tests for alias resolution and provenance.
- Slightly more complex validation and error taxonomy.

## Auditability and Verification

This decision is auditable when all of the following are true:

1. Expert requests without `actor_id` fail validation.
2. `requested_role` resolves with package-first precedence and deterministic fallback.
3. Responses include `resolved_expert_type` and resolution metadata fields.
4. Audit logs record actor, selector inputs, resolved expert, workflow, and trace ID.
5. Interface parity tests verify equivalent behavior across gRPC, FastAPI, and MCP.

## Follow-Up Documentation Updates (Required)

- Update IDL examples to include `requested_role`/resolution metadata sketch.
- Update architecture docs to avoid `expert_role` request contracts.
- Add implementation-plan tasks for actor/expert conformance and resolver audit tests.

## Change Control

Any change to required fields, precedence order, or response resolution metadata must:

1. Introduce a superseding ADR.
2. Include backward-compatibility and migration strategy.
3. Provide updated conformance and parity test criteria.
