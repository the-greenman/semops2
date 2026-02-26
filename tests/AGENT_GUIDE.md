# Agent Implementation Guide - TDD Workflow

This guide provides step-by-step instructions for AI agents implementing SemOps2 features using Test-Driven Development.

## Quick Start

### 1. Find Your Phase
```bash
# Phase 0: Config + Adapters
cd tests/unit/config

# Phase 1: EntityService CRUD
cd tests/unit/core

# Phase 2: Journey + Templates
cd tests/unit/core && tests/integration
```

### 2. Check Test Status
```bash
# See what tests exist for your feature
pytest tests/unit/config/test_config_manager.py --collect-only

# Run tests to see failures
pytest tests/unit/config/test_config_manager.py -v
```

### 3. TDD Cycle
For each test:
1. Unskip one test
2. Run test (it should fail)
3. Implement minimal code
4. Run test (it should pass)
5. Refactor
6. Repeat

## Implementation Order

### Phase 0: Foundation

#### Step 1: ConfigManager (Core)
**File:** `src/semops/core/config/config_manager.py`

**Tests to unskip in order:**
1. `test_discover_project_root_from_semops_marker` - Basic project discovery
2. `test_discover_project_root_from_semops_dir` - Directory-based discovery
3. `test_discover_project_root_from_git_root` - Git root fallback
4. `test_no_project_root_raises_clear_error` - Error handling
5. `test_layered_loading_builtin_then_project` - Config layering
6. `test_project_config_overrides_builtin` - Override logic

**Key Implementation Points:**
- Start with simple file/directory checks
- Add git root discovery using `git rev-parse --show-toplevel`
- Implement layered loading (builtin → project → explicit)
- Clear error messages with actionable hints

**When stuck:**
- Read test docstring for Given/When/Then
- Check fixture setup in `conftest.py`
- Look at expected error messages in assertions

#### Step 2: EntityTypeLoader
**File:** `src/semops/core/config/entity_type_loader.py`

**Tests to unskip in order:**
1. `test_load_entity_definition_from_yaml` - Basic YAML loading
2. `test_entity_type_with_namespace_prefix` - Namespace handling
3. `test_required_fields_validation` - Field validation
4. `test_id_prefix_uniqueness_check` - Uniqueness validation
5. `test_id_prefix_format_validation` - Format validation

**Key Implementation Points:**
- Use PyYAML for loading
- Validate required fields: `type_key`, `namespace`, `id_prefix`
- Build registry for lookup by key and prefix
- Validate ID prefix format: 2-4 uppercase alphanumeric

#### Step 3: PackageLoader
**File:** `src/semops/core/config/package_loader.py`

**Tests to unskip in order:**
1. `test_load_entity_package_complete` - Load all package files
2. `test_expert_resolution_package_first` - Package-first expert resolution
3. `test_expert_resolution_core_fallback` - Core expert fallback
4. `test_journey_stage_validation` - Journey validation

**Key Implementation Points:**
- Load `entity_definition.yaml`, `journey_definition.yaml`, `experts.yaml`
- Implement package-first expert resolution
- Validate journey stages (type field, valid types)
- Handle missing optional files gracefully

### Phase 1: EntityService

#### Step 4: EntityService CRUD
**File:** `src/semops/core/services/entity_service.py`

**Tests to unskip in order:**
1. `test_create_entity_writes_canonical_file` - Basic create
2. `test_create_entity_requires_actor_id` - Actor attribution
3. `test_create_entity_validates_required_fields` - Validation
4. `test_get_entity_reads_from_file` - Read operation
5. `test_update_entity_preserves_frontmatter` - Update operation
6. `test_delete_entity_cascade_option` - Delete operation

**Key Implementation Points:**
- Write markdown files to `.semops/entities/{entity_type_dir}/`
- Use frontmatter (YAML) for metadata
- Generate unique IDs: `{PREFIX}-{counter}-{slug}`
- Enforce actor_id for all mutations
- Parse frontmatter on read using `python-frontmatter` or manual parsing

**File Structure:**
```
.semops/entities/
  domains/
    DOM-001-user-authentication.md
    DOM-002-payment-processing.md
```

**File Format:**
```markdown
---
entity_type: domain
entity_id: DOM-001-user-authentication
created_at: 2026-02-26T10:00:00Z
created_by_actor_id: ACT-human-alice
updated_at: 2026-02-26T10:00:00Z
updated_by_actor_id: ACT-human-alice
domain_name: User Authentication
purpose: Manage user identity and access control
---

# User Authentication

## Purpose
Manage user identity and access control
```

### Phase 2: Journey Runtime

#### Step 5: ExpertService
**File:** `src/semops/core/services/expert_service.py`

**Tests to create and unskip:**
1. Expert resolution (package-first, core fallback)
2. Expert invocation with actor_id
3. Selector contract (`expert_type` or `requested_role`)
4. Metadata in responses (`requested_role`, `resolved_expert_type`, `resolution_source`, `trace_id`)

#### Step 5b: Expert Invocation Contract (ADR-0003)
**Files:**
- `src/semops/core/adapters/expert_invocation_adapter.py`
- `tests/contracts/test_expert_invocation_contract.py`

**Tests to create and unskip:**
1. Missing `actor_id` rejected
2. `requested_role` resolves package-first then core fallback
3. Interface parity across gRPC/FastAPI/MCP for same invocation semantics
4. Invalid selector combinations rejected consistently

#### Step 6: JourneyExecutor
**File:** `src/semops/core/services/journey_executor.py`

**Tests to create and unskip:**
1. Stage execution (human.create, ai.assist, human.review, system.commit)
2. Journey state persistence
3. Checkpoint and resume
4. `agent.role` alias resolution via ExpertInvocationAdapter
5. Mutation boundary invariant (`system.commit` routes through EntityService)

### Phase 0 Addendum: External Runtime Adapters

Add these after basic config/package loaders are stable:
1. `PromptRegistry` + telemetry adapter tests
2. `RAGPipelineExecutor` (Haystack-backed) tests
3. `ApiGatewayAdapter` + `MCPToolAdapter` parity tests

## Common Patterns

### Reading YAML Files
```python
import yaml
from pathlib import Path

def load_yaml(file_path: Path) -> dict:
    with open(file_path, "r") as f:
        return yaml.safe_load(f)
```

### Writing Markdown with Frontmatter
```python
def write_entity_file(path: Path, frontmatter: dict, content: str):
    import yaml

    with open(path, "w") as f:
        f.write("---\n")
        yaml.dump(frontmatter, f)
        f.write("---\n\n")
        f.write(content)
```

### Error Messages
Always include:
- What went wrong
- What was expected
- How to fix it

```python
class ValidationError(Exception):
    """Raised when validation fails."""
    pass

# Good error message
raise ValidationError(
    f"Entity type 'custom.ns/entity' is missing required field 'id_prefix'. "
    f"Add 'id_prefix' to entity definition in entity_types.yaml"
)
```

## Debugging Tests

### Test fails with ImportError
```bash
# Check module exists
ls -la src/semops/core/config/

# Check __init__.py files exist
find src -name "__init__.py"

# Run from project root
cd /workspace
pytest tests/unit/config/test_config_manager.py
```

### Test fails with unexpected error
```bash
# Run single test with full traceback
pytest tests/unit/config/test_config_manager.py::TestProjectRootDiscovery::test_discover_project_root_from_semops_marker -vvs

# Add print statements in test
def test_something(temp_dir):
    print(f"temp_dir = {temp_dir}")
    print(f"contents = {list(temp_dir.iterdir())}")
    ...
```

### Fixture not working
```bash
# Check fixture is defined
grep -r "def temp_semops_project" tests/

# Verify fixture in conftest.py
cat tests/conftest.py | grep -A 20 "def temp_semops_project"
```

## Code Style

### Imports
```python
# Standard library
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Third-party
import yaml
import pytest

# Local
from semops.core.config import ConfigManager
from semops.core.services.entity_service import EntityService
```

### Type Hints
```python
def create_entity(
    entity_type: str,
    data: Dict[str, Any],
    actor_id: str
) -> Dict[str, Any]:
    """Create new entity."""
    ...
```

### Docstrings
```python
def resolve_expert(self, entity_type: str, role: str) -> Optional[Dict[str, Any]]:
    """Resolve expert using package-first precedence.

    Args:
        entity_type: Full entity type key (namespace/type_key)
        role: Expert role to resolve

    Returns:
        Expert definition dict or None if not found

    Resolution order:
        1. entity_packages/{entity}/experts.yaml
        2. .semops/config/expert_types.yaml
        3. Builtin core experts
    """
    ...
```

## When You're Stuck

### Read the Architecture Docs
- `/workspace/docs/IMPLEMENTATION_PLAN.md` - Overall plan
- `/workspace/docs/ARCHITECTURE.md` - System architecture
- `/workspace/docs/EXPERT_SYSTEM_ARCHITECTURE.md` - Expert system details

### Check Examples
- `/workspace/examples/entity_packages/domain/` - Complete entity package
- `/workspace/examples/config/` - Configuration examples

### Ask Questions
If a test requirement is unclear:
1. Read the test docstring (Given/When/Then)
2. Check the assertions to see what's expected
3. Look at fixture setup in `conftest.py`
4. Examine similar tests for patterns

### Start Simple
If implementation seems complex:
1. Make the test pass with the simplest code
2. Hardcode values if needed
3. Refactor to generalize
4. Add error handling last

Example progression:
```python
# Step 1: Hardcode to make test pass
def get_entity_type(self, key: str):
    if key == "semops.core/domain":
        return {"type_key": "domain", "namespace": "semops.core"}
    return None

# Step 2: Read from dict
def get_entity_type(self, key: str):
    return self._entity_types.get(key)

# Step 3: Add validation
def get_entity_type(self, key: str):
    if not key:
        raise ValueError("Entity type key cannot be empty")
    return self._entity_types.get(key)
```

## Testing Your Implementation

### Run Tests Frequently
```bash
# Run tests after each small change
pytest tests/unit/config/test_config_manager.py::TestProjectRootDiscovery::test_discover_project_root_from_semops_marker -v

# Run all tests in a file
pytest tests/unit/config/test_config_manager.py -v

# Run all tests in a phase
pytest -m skip_until_phase0 -v
```

### Check Coverage
```bash
# Generate coverage report
pytest tests/unit/config/ --cov=src/semops/core/config --cov-report=term-missing

# Aim for >90% coverage on core modules
```

## Success Criteria

### Phase 0 Complete When:
- ✅ All Phase 0 unit tests pass
- ✅ `test_config_loading.py` integration tests pass
- ✅ ConfigManager can load config from `.semops/`
- ✅ Entity packages are loaded with experts
- ✅ Expert resolution works package-first

### Phase 1 Complete When:
- ✅ All Phase 1 unit tests pass
- ✅ Can create/read/update/delete entities
- ✅ Entity files written to canonical location
- ✅ Actor attribution enforced
- ✅ Frontmatter parsed correctly

### Phase 2 Complete When:
- ✅ All Phase 2 tests pass
- ✅ Journey stages execute
- ✅ Expert invocation works with ADR-0003 selector contract
- ✅ Response metadata includes resolved expert attribution fields
- ✅ Template migration functional
- ✅ End-to-end journey completes

## Next Steps After TDD Structure

Once tests are created, implementation follows this pattern:

1. **Create module structure**
   ```bash
   mkdir -p src/semops/core/config
   touch src/semops/core/config/__init__.py
   touch src/semops/core/config/config_manager.py
   ```

2. **Run tests to see failures**
   ```bash
   pytest tests/unit/config/test_config_manager.py -v
   ```

3. **Implement to make tests pass**
   - Start with simplest test
   - Unskip one test at a time
   - Make it pass with minimal code
   - Refactor

4. **Move to next feature**
   - Follow dependency order
   - Build incrementally
   - Keep tests passing

Good luck! The tests are your specification. Trust them.
