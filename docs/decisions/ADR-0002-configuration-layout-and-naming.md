# ADR-0002: Canonical Configuration Layout and Naming

- **Status:** Accepted
- **Date:** 2026-02-26
- **Owners:** Architecture / Developer Experience
- **Decision Type:** Configuration discovery and standards

## Context

SemOps2 documentation currently mixes multiple configuration path conventions:

- `.semops/config/*.yaml` in architecture docs
- flat paths like `.semops/entity_types.yaml` and `.semops/workflows.yaml` in contributor workflows
- mixed examples like `config/experts.yaml` vs `expert_types.yaml`

This causes onboarding errors, loader ambiguity, and drift between docs and implementation.

## Decision

SemOps2 adopts a single canonical project configuration layout rooted at:

- `.semops/config/`

Canonical file names:

- `entity_types.yaml`
- `source_types.yaml`
- `expert_types.yaml`
- `workflows.yaml` (general multi-step analysis/workflow orchestration)
- `rag_workflows.yaml` (retrieval-specific workflows)
- `storage_backends.yaml`
- `pipeline_configurations.yaml`

Templates remain under:

- `.semops/templates/`

## Naming Conventions (Option A)

To keep CLI usage readable and config parsing predictable, SemOps2 standardizes naming as follows:

1. **User-facing IDs (kebab-case):**
   - Journey IDs and workflow IDs use kebab-case (e.g., `domain-definition`, `decision-refinement`).

2. **YAML map keys (snake_case):**
   - Configuration object keys use snake_case (e.g., `define_domain_strategy`, `authority_weighted`).

3. **Entity type references:**
   - Entity types use fully-qualified `{namespace}/{type_key}` strings (e.g., `semops.core/domain`).

4. **Stage and action keys (snake_case):**
   - Internal stage/action identifiers use snake_case (e.g., `scope_clarification`, `apply_authority_weights`).

## Standard Directory Pattern

```text
<workspace-root>/
├── .semops-project
└── .semops/
    ├── config/
    │   ├── entity_types.yaml
    │   ├── source_types.yaml
    │   ├── expert_types.yaml
    │   ├── workflows.yaml
    │   ├── rag_workflows.yaml
    │   ├── storage_backends.yaml
    │   └── pipeline_configurations.yaml
    └── templates/
        ├── <entity>.md.j2
        └── ...
```

## Clean-Slate Policy

1. Only `.semops/config/*.yaml` paths are supported.
2. Flat `.semops/*.yaml` paths are not supported.
3. Loader behavior is strict: non-canonical locations fail fast with a clear error.
4. No migration or backward-compatibility behavior is required for legacy config path conventions.

This clean-slate policy does not apply to **template evolution**. SemOps2 supports template migrations (e.g., migrating entities between template versions) as an essential function.

## Consequences

### Positive

- Unambiguous onboarding and contributor guidance.
- Deterministic configuration discovery.
- Cleaner separation between config and templates.

### Costs

- Requires strict validation and clear error messages for invalid paths.

## Auditability and Verification

This decision is auditable when:

1. All contributor-facing docs use `.semops/config/*.yaml` paths.
2. Loader behavior is documented and tested as strict path validation.
3. Integration tests validate canonical path discovery when invoked from subdirectories within a workspace.
4. Integration tests assert that non-canonical config paths fail with actionable errors.

## Follow-Up Updates

- Update architecture, developer guide, and BDD examples to canonical config paths.
- Ensure workflow naming is consistent (`workflows.yaml` vs `rag_workflows.yaml` by purpose).
