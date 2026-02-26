# Agent Implementation Task List

**Project:** SemOps2 TDD Implementation
**Date Created:** 2026-02-26
**Status:** Ready for agent execution (aligned to ADR-0001/0002/0003 baseline)

This document provides a sequential task list for agents to implement SemOps2 features using Test-Driven Development. Each task is self-contained and builds on previous tasks.

## Task Organization

Tasks are organized by:
- **Phase** - Implementation phase (0, 1, 2)
- **Priority** - Critical path vs. supporting features
- **Dependencies** - What must be completed first
- **Estimated Complexity** - Small (S), Medium (M), Large (L)

## Legend

- 🔴 **Blocked** - Cannot start until dependencies complete
- 🟡 **Ready** - Can start now
- 🟢 **In Progress** - Currently being worked on
- ✅ **Complete** - Done and tests passing

---

# Phase 0: Foundation (Config + Adapters)

## Milestone 0.1: Project Structure Setup

### Task 0.1.1: Create Core Module Structure
**Status:** 🟡 Ready
**Complexity:** S
**Dependencies:** None

**Objective:** Create the base directory structure and `__init__.py` files.

**Actions:**
```bash
mkdir -p src/semops/core/config
mkdir -p src/semops/core/services
mkdir -p src/semops/core/adapters
mkdir -p src/semops/core/models

touch src/semops/core/__init__.py
touch src/semops/core/config/__init__.py
touch src/semops/core/services/__init__.py
touch src/semops/core/adapters/__init__.py
touch src/semops/core/models/__init__.py
```

**Validation:**
```bash
pytest tests/ --collect-only -q  # Should still collect 81 tests
```

**Completion Criteria:**
- [ ] All directories created
- [ ] All `__init__.py` files exist
- [ ] Tests still collect successfully

---

### Task 0.1.2: Create Exception Classes
**Status:** 🔴 Blocked by 0.1.1
**Complexity:** S
**Dependencies:** 0.1.1

**Objective:** Define custom exception classes used throughout the codebase.

**File:** `src/semops/core/exceptions.py`

**Implementation:**
```python
"""Custom exceptions for SemOps2."""

class SemOpsError(Exception):
    """Base exception for all SemOps errors."""
    pass

class ConfigurationError(SemOpsError):
    """Raised when configuration is invalid or missing."""
    pass

class ValidationError(SemOpsError):
    """Raised when validation fails."""
    pass

class EntityNotFoundError(SemOpsError):
    """Raised when an entity cannot be found."""
    pass

class NoExpertFoundError(SemOpsError):
    """Raised when expert resolution fails."""
    pass
```

**Tests Affected:**
- All error handling tests across Phase 0 and Phase 1

**Validation:**
```bash
python -c "from semops.core.exceptions import ConfigurationError; print('OK')"
```

**Completion Criteria:**
- [ ] File created with all exception classes
- [ ] Exceptions can be imported
- [ ] Docstrings present

---

## Milestone 0.2: ConfigManager Implementation

### Task 0.2.1: Implement Project Root Discovery
**Status:** 🔴 Blocked by 0.1.2
**Complexity:** M
**Dependencies:** 0.1.1, 0.1.2
**Tests:** `tests/unit/config/test_config_manager.py::TestProjectRootDiscovery` (4 tests)

**Objective:** Implement logic to discover the SemOps project root from any working directory.

**File:** `src/semops/core/config/config_manager.py`

**Implementation Steps:**

1. **Create ConfigManager class skeleton:**
   ```python
   from pathlib import Path
   from typing import Optional
   from semops.core.exceptions import ConfigurationError

   class ConfigManager:
       def __init__(self, working_dir: Optional[Path] = None):
           self.working_dir = working_dir or Path.cwd()
           self.project_root = self._discover_project_root()

       def _discover_project_root(self) -> Path:
           """Discover project root from working directory."""
           pass
   ```

2. **Implement discovery logic (in priority order):**
   - Check for `.semops-project` marker file
   - Check for `.semops/` directory
   - Check for git root with `.semops/`
   - Raise `ConfigurationError` if not found

3. **Unskip tests one at a time:**
   - `test_discover_project_root_from_semops_marker`
   - `test_discover_project_root_from_semops_dir`
   - `test_discover_project_root_from_git_root`
   - `test_no_project_root_raises_clear_error`

**Key Implementation Details:**
- Use `Path.parent` to walk up directory tree
- Use `subprocess.run(["git", "rev-parse", "--show-toplevel"])` for git root
- Include helpful error messages with suggestions

**Validation:**
```bash
# Unskip and run tests one at a time
pytest tests/unit/config/test_config_manager.py::TestProjectRootDiscovery::test_discover_project_root_from_semops_marker -v

# After all 4 tests pass:
pytest tests/unit/config/test_config_manager.py::TestProjectRootDiscovery -v
```

**Completion Criteria:**
- [ ] All 4 TestProjectRootDiscovery tests pass
- [ ] Clear error messages for failure cases
- [ ] Git root discovery works

**Reference:**
- See [tests/AGENT_GUIDE.md](/workspace/tests/AGENT_GUIDE.md) Step 1: ConfigManager

---

### Task 0.2.2: Implement Layered Configuration Loading
**Status:** 🔴 Blocked by 0.2.1
**Complexity:** L
**Dependencies:** 0.2.1
**Tests:** `tests/unit/config/test_config_manager.py::TestLayeredConfigLoading` (3 tests)

**Objective:** Load and merge configuration from builtin → project → explicit sources.

**File:** `src/semops/core/config/config_manager.py` (extend)

**Implementation Steps:**

1. **Add configuration loading methods:**
   ```python
   def _load_builtin_config(self) -> dict:
       """Load builtin default configuration."""
       pass

   def _load_project_config(self) -> dict:
       """Load project-specific configuration from .semops/config/."""
       pass

   def _merge_configs(self, builtin: dict, project: dict, explicit: dict) -> dict:
       """Deep merge configurations with proper precedence."""
       pass
   ```

2. **Create builtin defaults:**
   - Define core entity types (domain, meeting, decision, etc.)
   - Store as embedded Python dict or load from packaged YAML

3. **Load project config from `.semops/config/*.yaml`:**
   - `entity_types.yaml`
   - `expert_types.yaml`
   - Handle missing files gracefully

4. **Implement deep merge logic:**
   - Project overrides builtin
   - Explicit overrides both

**Unskip Tests:**
- `test_layered_loading_builtin_then_project`
- `test_project_config_overrides_builtin`
- `test_explicit_config_path_override`

**Key Implementation Details:**
- Use PyYAML for loading
- Deep merge, not shallow override
- Preserve builtin config when project doesn't override

**Validation:**
```bash
pytest tests/unit/config/test_config_manager.py::TestLayeredConfigLoading -v
```

**Completion Criteria:**
- [ ] All 3 TestLayeredConfigLoading tests pass
- [ ] Builtin config defined
- [ ] Config files loaded from `.semops/config/`
- [ ] Merge logic works correctly

---

### Task 0.2.3: Implement Namespace Validation
**Status:** 🔴 Blocked by 0.2.2
**Complexity:** M
**Dependencies:** 0.2.2
**Tests:** `tests/unit/config/test_config_manager.py::TestNamespaceValidation` (2 tests)

**Objective:** Validate that `semops.*` namespace is reserved and custom namespaces are allowed.

**File:** `src/semops/core/config/config_manager.py` (extend)

**Implementation Steps:**

1. **Add validation method:**
   ```python
   def _validate_namespace(self, entity_type_key: str, namespace: str, is_builtin: bool = False) -> None:
       """Validate namespace is not reserved unless builtin."""
       if namespace.startswith("semops.") and not is_builtin:
           raise ValidationError(
               f"Entity type '{entity_type_key}' uses reserved namespace '{namespace}'. "
               f"The 'semops.*' namespace is reserved for builtin entity types. "
               f"Use a custom namespace like 'myorg.team' instead."
           )
   ```

2. **Call validation during config loading:**
   - Validate project config entity types
   - Skip validation for builtin config
   - Clear error messages

**Unskip Tests:**
- `test_namespace_validation_semops_core_reserved`
- `test_custom_namespace_allowed`

**Validation:**
```bash
pytest tests/unit/config/test_config_manager.py::TestNamespaceValidation -v
```

**Completion Criteria:**
- [ ] All 2 TestNamespaceValidation tests pass
- [ ] Reserved namespace check works
- [ ] Custom namespaces allowed

---

### Task 0.2.4: Implement Error Handling
**Status:** 🔴 Blocked by 0.2.3
**Complexity:** S
**Dependencies:** 0.2.3
**Tests:** `tests/unit/config/test_config_manager.py::TestConfigErrorHandling` (3 tests)

**Objective:** Provide clear error messages for common configuration errors.

**File:** `src/semops/core/config/config_manager.py` (extend)

**Implementation Steps:**

1. **Add error handling for:**
   - Invalid config path
   - Malformed YAML
   - Missing required fields

2. **Use try/except with clear messages:**
   ```python
   try:
       with open(config_file, "r") as f:
           data = yaml.safe_load(f)
   except yaml.YAMLError as e:
       raise ConfigurationError(
           f"Invalid YAML in {config_file}: {e}\n"
           f"Please check the syntax and try again."
       )
   ```

**Unskip Tests:**
- `test_invalid_config_path_raises_clear_error`
- `test_malformed_yaml_raises_clear_error`
- `test_missing_required_field_raises_clear_error`

**Validation:**
```bash
pytest tests/unit/config/test_config_manager.py::TestConfigErrorHandling -v

# All ConfigManager tests should pass now
pytest tests/unit/config/test_config_manager.py -v
```

**Completion Criteria:**
- [ ] All 3 TestConfigErrorHandling tests pass
- [ ] Clear error messages with context
- [ ] All 12 ConfigManager tests pass

---

## Milestone 0.3: EntityTypeLoader Implementation

### Task 0.3.1: Implement Entity Type YAML Loading
**Status:** 🔴 Blocked by 0.2.4
**Complexity:** M
**Dependencies:** 0.2.4
**Tests:** `tests/unit/config/test_entity_type_loader.py::TestEntityTypeLoading` (3 tests)

**Objective:** Load and parse entity type definitions from YAML files.

**File:** `src/semops/core/config/entity_type_loader.py`

**Implementation Steps:**

1. **Create EntityTypeLoader class:**
   ```python
   import yaml
   from pathlib import Path
   from typing import Dict, Any
   from semops.core.exceptions import ValidationError

   class EntityTypeLoader:
       def __init__(self, config_path: Path):
           self.config_path = config_path

       def load_entity_types(self) -> Dict[str, Dict[str, Any]]:
           """Load entity types from entity_types.yaml."""
           pass
   ```

2. **Load entity_types.yaml:**
   - Read from `{config_path}/entity_types.yaml`
   - Parse YAML
   - Return dict keyed by `namespace/type_key`

3. **Handle template bundle paths:**
   - Resolve template paths relative to template directory
   - Store paths as-is (no validation yet)

**Unskip Tests:**
- `test_load_entity_definition_from_yaml`
- `test_entity_type_with_namespace_prefix`
- `test_template_bundle_path_resolution`

**Validation:**
```bash
pytest tests/unit/config/test_entity_type_loader.py::TestEntityTypeLoading -v
```

**Completion Criteria:**
- [ ] All 3 TestEntityTypeLoading tests pass
- [ ] YAML loading works
- [ ] Namespace/type_key format correct

---

### Task 0.3.2: Implement Entity Type Validation
**Status:** 🔴 Blocked by 0.3.1
**Complexity:** M
**Dependencies:** 0.3.1
**Tests:** `tests/unit/config/test_entity_type_loader.py::TestEntityTypeValidation` (4 tests)

**Objective:** Validate entity type definitions for required fields, uniqueness, and format.

**File:** `src/semops/core/config/entity_type_loader.py` (extend)

**Implementation Steps:**

1. **Add validation method:**
   ```python
   def _validate_entity_type(self, entity_type_key: str, entity_type: dict) -> None:
       """Validate entity type has required fields and correct format."""
       required_fields = ["type_key", "namespace", "id_prefix"]
       for field in required_fields:
           if field not in entity_type:
               raise ValidationError(
                   f"Entity type '{entity_type_key}' is missing required field '{field}'. "
                   f"Add '{field}' to entity definition in entity_types.yaml"
               )
   ```

2. **Validate ID prefix:**
   - Format: 2-4 uppercase alphanumeric characters
   - Uniqueness: No duplicate prefixes
   - Use regex: `^[A-Z0-9]{2,4}$`

3. **Validate namespace format:**
   - Format: lowercase.dotted.notation
   - Use regex: `^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)*$`

**Unskip Tests:**
- `test_required_fields_validation`
- `test_id_prefix_uniqueness_check`
- `test_id_prefix_format_validation`
- `test_namespace_format_validation`

**Validation:**
```bash
pytest tests/unit/config/test_entity_type_loader.py::TestEntityTypeValidation -v
```

**Completion Criteria:**
- [ ] All 4 TestEntityTypeValidation tests pass
- [ ] Required fields checked
- [ ] ID prefix format validated
- [ ] Uniqueness enforced

---

### Task 0.3.3: Implement Entity Type Registry
**Status:** 🔴 Blocked by 0.3.2
**Complexity:** M
**Dependencies:** 0.3.2
**Tests:** `tests/unit/config/test_entity_type_loader.py::TestEntityTypeRegistry` (3 tests)

**Objective:** Create registry for efficient entity type lookup.

**File:** `src/semops/core/config/entity_type_registry.py`

**Implementation Steps:**

1. **Create EntityTypeRegistry class:**
   ```python
   class EntityTypeRegistry:
       def __init__(self, entity_types: Dict[str, Dict[str, Any]]):
           self._entity_types = entity_types
           self._prefix_index = self._build_prefix_index()
           self._namespace_index = self._build_namespace_index()

       def get(self, key: str) -> Optional[Dict[str, Any]]:
           """Get entity type by full key (namespace/type_key)."""
           pass

       def get_by_prefix(self, prefix: str) -> Optional[Dict[str, Any]]:
           """Get entity type by ID prefix."""
           pass

       def get_by_namespace(self, namespace: str) -> List[Dict[str, Any]]:
           """Get all entity types in namespace."""
           pass
   ```

2. **Build indexes:**
   - Prefix → entity type
   - Namespace → list of entity types

3. **Integrate with EntityTypeLoader:**
   - Add `build_registry()` method
   - Return EntityTypeRegistry instance

**Unskip Tests:**
- `test_get_entity_type_by_key`
- `test_get_entity_type_by_prefix`
- `test_list_entity_types_by_namespace`

**Validation:**
```bash
pytest tests/unit/config/test_entity_type_loader.py::TestEntityTypeRegistry -v

# All EntityTypeLoader tests should pass now
pytest tests/unit/config/test_entity_type_loader.py -v
```

**Completion Criteria:**
- [ ] All 3 TestEntityTypeRegistry tests pass
- [ ] Lookup by key works
- [ ] Lookup by prefix works
- [ ] Filter by namespace works
- [ ] All 15 EntityTypeLoader tests pass

---

## Milestone 0.4: PackageLoader Implementation

### Task 0.4.1: Implement Entity Package Loading
**Status:** 🔴 Blocked by 0.3.3
**Complexity:** M
**Dependencies:** 0.3.3
**Tests:** `tests/unit/config/test_package_loader.py::TestEntityPackageLoading` (4 tests)

**Objective:** Load complete entity packages including entity_definition, journey, and experts.

**File:** `src/semops/core/config/package_loader.py`

**Implementation Steps:**

1. **Create PackageLoader class:**
   ```python
   class PackageLoader:
       def __init__(self, packages_dir: Path):
           self.packages_dir = packages_dir

       def load_all_packages(self) -> Dict[str, Dict[str, Any]]:
           """Load all entity packages from entity_packages/ directory."""
           pass

       def load_package(self, package_name: str) -> Dict[str, Any]:
           """Load a specific entity package by name."""
           pass
   ```

2. **Load package files:**
   - `entity_definition.yaml` (required)
   - `journey_definition.yaml` (optional)
   - `experts.yaml` (optional)

3. **Handle missing files:**
   - Raise error if entity_definition missing
   - Set others to None if missing

**Unskip Tests:**
- `test_load_entity_package_complete`
- `test_load_package_by_name`
- `test_missing_entity_definition_raises_error`
- `test_package_with_only_entity_definition_allowed`

**Validation:**
```bash
pytest tests/unit/config/test_package_loader.py::TestEntityPackageLoading -v
```

**Completion Criteria:**
- [ ] All 4 TestEntityPackageLoading tests pass
- [ ] All three files loaded
- [ ] Optional files handled gracefully

---

### Task 0.4.2: Implement Expert Resolution
**Status:** 🔴 Blocked by 0.4.1
**Complexity:** M
**Dependencies:** 0.4.1
**Tests:** `tests/unit/config/test_package_loader.py::TestExpertResolution` (3 tests)

**Objective:** Resolve experts with package-first precedence, then core fallback.

**File:** `src/semops/core/config/package_loader.py` (extend)

**Implementation Steps:**

1. **Add expert resolution method:**
   ```python
   def resolve_expert(
       self,
       entity_type: str,
       role: str,
       core_experts: Optional[Dict[str, Any]] = None
   ) -> Optional[Dict[str, Any]]:
       """Resolve expert using package-first precedence.

       Resolution order:
       1. entity_packages/{entity}/experts.yaml
       2. core_experts (from .semops/config/expert_types.yaml)
       3. None if not found
       """
       pass
   ```

2. **Add metadata to resolved expert:**
   - `_resolution_source`: "package" or "core"
   - Helps with debugging and tracing

**Unskip Tests:**
- `test_expert_resolution_package_first`
- `test_expert_resolution_core_fallback`
- `test_expert_resolution_not_found_returns_none`

**Validation:**
```bash
pytest tests/unit/config/test_package_loader.py::TestExpertResolution -v
```

**Completion Criteria:**
- [ ] All 3 TestExpertResolution tests pass
- [ ] Package experts have priority
- [ ] Core experts used as fallback
- [ ] Metadata included

---

### Task 0.4.3: Implement Journey Validation
**Status:** 🔴 Blocked by 0.4.2
**Complexity:** M
**Dependencies:** 0.4.2
**Tests:** `tests/unit/config/test_package_loader.py::TestJourneyValidation` (3 tests)

**Objective:** Validate journey definitions for required fields and correct stage types.

**File:** `src/semops/core/config/package_loader.py` (extend)

**Implementation Steps:**

1. **Add journey validation:**
   ```python
   VALID_STAGE_TYPES = ["human.create", "ai.assist", "human.review", "system.commit"]

   def _validate_journey(self, journey_data: dict) -> None:
       """Validate journey definition."""
       for stage in journey_data.get("entity_journey", {}).get("stages", []):
           # Check required fields
           if "type" not in stage:
               raise ValidationError(
                   f"Journey stage '{stage.get('name', 'unnamed')}' is missing required field 'type'"
               )

           # Validate stage type
           if stage["type"] not in VALID_STAGE_TYPES:
               raise ValidationError(
                   f"Invalid stage type '{stage['type']}'. "
                   f"Must be one of: {', '.join(VALID_STAGE_TYPES)}"
               )

           # Check ai.assist stages have agent
           if stage["type"] == "ai.assist" and "agent" not in stage:
               raise ValidationError(
                   f"Stage '{stage['name']}' is type 'ai.assist' but missing required 'agent' field"
               )
   ```

**Unskip Tests:**
- `test_journey_stage_validation`
- `test_journey_stage_types_validated`
- `test_journey_ai_assist_stage_requires_agent`

**Validation:**
```bash
pytest tests/unit/config/test_package_loader.py::TestJourneyValidation -v

# All PackageLoader tests should pass now
pytest tests/unit/config/test_package_loader.py -v
```

**Completion Criteria:**
- [ ] All 3 TestJourneyValidation tests pass
- [ ] Stage types validated
- [ ] ai.assist stages require agent
- [ ] All 14 PackageLoader tests pass

---

## Milestone 0.5: Adapter Interfaces

**Alignment:** This milestone must satisfy Workstream J in `IMPLEMENTATION_PLAN.md`, including adapter boundaries for prompt ops, RAG orchestration, API/MCP surfaces, and actor/expert invocation conformance (ADR-0003).

### Task 0.5.1: Create LLMStructuredClient Interface
**Status:** 🔴 Blocked by 0.1.2
**Complexity:** M
**Dependencies:** 0.1.2
**Tests:** `tests/unit/adapters/test_llm_client_interface.py` (8 tests)

**Objective:** Define abstract interface for structured LLM outputs with Instructor/Pydantic.

**File:** `src/semops/core/adapters/llm_client.py`

**Implementation Steps:**

1. **Create abstract interface:**
   ```python
   from abc import ABC, abstractmethod
   from typing import Dict, Any, Type, TypeVar
   from pydantic import BaseModel
   from dataclasses import dataclass

   T = TypeVar('T', bound=BaseModel)

   @dataclass
   class LLMResult:
       """Result from LLM generation."""
       data: BaseModel
       metadata: Dict[str, Any]

   class LLMStructuredClient:
       """Client for structured LLM outputs with validation."""

       def __init__(
           self,
           backend: Any,
           max_retries: int = 2,
           initial_backoff: float = 0.1,
           default_model: str = "claude-3-5-sonnet",
           on_validation_error: Optional[callable] = None
       ):
           self.backend = backend
           self.max_retries = max_retries
           self.initial_backoff = initial_backoff
           self.default_model = default_model
           self.on_validation_error = on_validation_error

       def generate(
           self,
           prompt: str,
           schema: Type[T],
           metadata: Optional[Dict[str, Any]] = None
       ) -> LLMResult:
           """Generate structured output with retries."""
           pass
   ```

2. **Implement retry logic with exponential backoff:**
   - Try to validate response with Pydantic
   - On validation error, retry with backoff
   - Track retry count in metadata

3. **Add metadata to results:**
   - `schema_validated`: bool
   - `prompt_version`: from input metadata
   - `trace_id`: unique identifier
   - `retry_count`: number of retries
   - `model`: model used

**Unskip Tests (one at a time):**
- `test_structured_output_valid_response`
- `test_structured_output_malformed_with_retry`
- `test_structured_output_exhausted_retries`
- `test_response_includes_metadata`
- `test_exponential_backoff_on_retries`
- `test_retry_count_in_metadata`
- `test_custom_validation_error_handler`
- `test_model_parameter_passed_to_backend`

**Validation:**
```bash
pytest tests/unit/adapters/test_llm_client_interface.py -v
```

**Completion Criteria:**
- [ ] All 8 LLM client tests pass
- [ ] Retry logic works
- [ ] Metadata included
- [ ] Exponential backoff implemented

**Note:** This requires Pydantic and Instructor. Run:
```bash
pip install pydantic>=2.0.0 instructor>=1.0.0
```

---

### Task 0.5.2: Create VectorStoreAdapter Interface
**Status:** 🔴 Blocked by 0.1.2
**Complexity:** L
**Dependencies:** 0.1.2
**Tests:** `tests/unit/adapters/test_vector_store_interface.py` (14 tests)

**Objective:** Define abstract vector store interface with Chroma and Qdrant implementations.

**File:** `src/semops/core/adapters/vector_store.py`

**Implementation Steps:**

1. **Create abstract interface:**
   ```python
   from abc import ABC, abstractmethod
   from typing import List, Dict, Any, Optional

   class VectorStoreAdapter(ABC):
       """Abstract interface for vector stores."""

       @abstractmethod
       def ingest(self, documents: List[Dict[str, Any]]) -> None:
           """Ingest documents with embeddings."""
           pass

       @abstractmethod
       def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
           """Search for similar documents."""
           pass

       @abstractmethod
       def filter(self, metadata_filter: Dict[str, Any]) -> List[Dict[str, Any]]:
           """Filter documents by metadata."""
           pass

       @abstractmethod
       def delete(self, document_id: str) -> None:
           """Delete document by ID."""
           pass

       @abstractmethod
       def get_collection(self, name: str):
           """Get or create collection."""
           pass
   ```

2. **Implement Chroma backend:**
   - File: `src/semops/core/adapters/vector_store_chroma.py`
   - Use chromadb library
   - Generate embeddings automatically

3. **Implement Qdrant backend:**
   - File: `src/semops/core/adapters/vector_store_qdrant.py`
   - Use qdrant-client library
   - Match Chroma API

**Unskip Tests:**
- Start with interface tests (4 tests)
- Then Chroma implementation (3 tests)
- Then Qdrant implementation (2 tests)
- Finally parity tests (3 tests)
- Skip performance tests (2 tests) until needed

**Validation:**
```bash
# Interface tests
pytest tests/unit/adapters/test_vector_store_interface.py::TestVectorStoreInterface -v

# Chroma tests
pytest tests/unit/adapters/test_vector_store_interface.py::TestChromaImplementation -v

# All tests
pytest tests/unit/adapters/test_vector_store_interface.py -v
```

**Completion Criteria:**
- [ ] Interface defined
- [ ] Chroma implementation works
- [ ] Qdrant implementation works (or marked for Phase 3)
- [ ] Backend parity validated
- [ ] At least 10/14 tests pass (skip perf tests)

**Note:** This is a larger task. Can be split into sub-tasks if needed.

---

### Task 0.5.3: Create PromptRegistry + Telemetry Adapter
**Status:** 🔴 Blocked by 0.1.2
**Complexity:** M
**Dependencies:** 0.1.2
**Tests:** Create `tests/unit/adapters/test_prompt_registry.py`

**Objective:** Manage prompt resolution/rendering/version usage tracking with a stable internal interface.

**Files:**
- `src/semops/core/adapters/prompt_registry.py`
- `src/semops/core/adapters/prompt_telemetry.py`

**Implementation Requirements:**
- Provide `resolve/render/record_usage` operations.
- Keep in-repo prompts as source of truth; telemetry is additive.
- Include `prompt_version` and `trace_id` in usage metadata.

**Required Tests (minimum):**
- resolve prompt by key/version
- render with variables
- record usage emits expected metadata
- missing prompt/version raises clear error

---

### Task 0.5.4: Create RAGPipelineExecutor (Haystack-backed)
**Status:** 🔴 Blocked by 0.1.2, 0.5.2
**Complexity:** L
**Dependencies:** 0.1.2, 0.5.2
**Tests:** Create `tests/unit/adapters/test_rag_pipeline_executor.py`

**Objective:** Implement `RAGPipelineExecutor` behind SemOps adapter boundaries with Haystack as orchestration layer.

**File:** `src/semops/core/adapters/rag_pipeline_executor.py`

**Implementation Requirements:**
- Method shape: `run(workflow_id, query, context_entity_id, backend_hint)`.
- Config-driven workflow selection (`.semops/config/rag_workflows.yaml`).
- Preserve backend abstraction (`Chroma` local, `Qdrant` production).
- Return metadata including `backend_used`.

**Required Tests (minimum):**
- workflow dispatch by `workflow_id`
- backend selection via `backend_hint`
- schema/metadata shape parity across backends
- clear failure mode for unknown workflow/backend

---

### Task 0.5.5: Create API/MCP Surface Adapters
**Status:** 🔴 Blocked by 0.5.1, 0.5.4
**Complexity:** L
**Dependencies:** 0.5.1, 0.5.4
**Tests:** Create `tests/contracts/test_interface_parity.py`

**Objective:** Add adapter scaffolding for FastAPI over gRPC clients and official MCP Python SDK without leaking framework primitives into domain services.

**Files:**
- `src/semops/core/adapters/api_gateway_adapter.py`
- `src/semops/core/adapters/mcp_tool_adapter.py`

**Implementation Requirements:**
- Contract-bound translation layer only.
- Parity checks for equivalent semantics across gRPC, FastAPI, MCP.
- No bypass of EntityService mutation boundary.

**Required Tests (minimum):**
- same request semantics and status mapping across interfaces
- error mapping parity
- mutation path enforcement invariant

---

### Task 0.5.6: Create ExpertInvocationAdapter (ADR-0003)
**Status:** 🔴 Blocked by 0.4.2, 0.5.1
**Complexity:** M
**Dependencies:** 0.4.2, 0.5.1
**Tests:** Create `tests/unit/adapters/test_expert_invocation_adapter.py`

**Objective:** Enforce actor-aware expert invocation contract and role-alias resolution semantics.

**File:** `src/semops/core/adapters/expert_invocation_adapter.py`

**Implementation Requirements:**
- Require `actor_id`.
- Support selector contract: `expert_type` OR `requested_role`.
- Resolve `requested_role` package-first, then core fallback.
- Attach resolution metadata: `requested_role`, `resolved_expert_type`, `resolution_source`.

**Required Tests (minimum):**
- reject request when `actor_id` missing
- resolve explicit `expert_type`
- resolve `requested_role` package-first
- resolve core fallback when package expert absent
- reject ambiguous/invalid selector input

---

## Milestone 0.6: Integration Testing

### Task 0.6.1: Integration Test - Config Loading
**Status:** 🔴 Blocked by 0.2.4, 0.3.3, 0.4.3
**Complexity:** M
**Dependencies:** All config components complete
**Tests:** `tests/integration/test_config_loading.py` (9 tests)

**Objective:** Verify end-to-end configuration loading works correctly.

**Actions:**

1. **Ensure all dependencies complete:**
   - ConfigManager ✓
   - EntityTypeLoader ✓
   - PackageLoader ✓

2. **Run integration tests:**
   - These tests should mostly work if unit tests pass
   - May need minor ConfigManager updates

3. **Unskip tests:**
   - `test_load_config_with_entity_packages`
   - `test_expert_resolution_with_fallback`
   - `test_template_discovery_override`
   - `test_config_layering_with_overrides`
   - Validation tests (3 tests)
   - Caching tests (2 tests)

**Validation:**
```bash
pytest tests/integration/test_config_loading.py -v
```

**Completion Criteria:**
- [ ] All 9 integration tests pass
- [ ] End-to-end config loading works
- [ ] Expert resolution works across components
- [ ] Template discovery works

---

## Phase 0 Summary

**Total Tasks:** 19
**Total Tests:** 50 (41 unit + 9 integration) plus adapter tests added in Milestone 0.5.3-0.5.6

**Completion Checklist:**
- [ ] All module structure created
- [ ] ConfigManager complete (12 tests)
- [ ] EntityTypeLoader complete (15 tests)
- [ ] PackageLoader complete (14 tests)
- [ ] LLMStructuredClient complete (8 tests)
- [ ] VectorStoreAdapter complete (10+ tests)
- [ ] PromptRegistry + telemetry adapter complete
- [ ] RAGPipelineExecutor (Haystack-backed) complete
- [ ] API/MCP adapters complete
- [ ] ExpertInvocationAdapter (ADR-0003) complete
- [ ] Integration tests pass (9 tests)

**When Phase 0 is complete:**
```bash
# All Phase 0 tests should pass
pytest -m skip_until_phase0 -v

# Summary check
pytest tests/unit/config/ tests/unit/adapters/ tests/integration/ -v --tb=short
```

---

# Phase 1: Entity Service (File-First CRUD)

## Milestone 1.1: Entity Service Core

### Task 1.1.1: Create Entity Models
**Status:** 🔴 Blocked by Phase 0
**Complexity:** S
**Dependencies:** Phase 0 complete

**Objective:** Define Pydantic models for entities.

**File:** `src/semops/core/models/entity.py`

**Implementation:**
```python
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class Entity(BaseModel):
    """Entity data model."""
    entity_id: str
    entity_type: str
    created_at: datetime
    created_by_actor_id: str
    updated_at: datetime
    updated_by_actor_id: str
    data: Dict[str, Any]
```

**Completion Criteria:**
- [ ] Entity model defined
- [ ] All fields typed
- [ ] Model can be imported

---

### Task 1.1.2: Implement Entity Creation
**Status:** 🔴 Blocked by 1.1.1, Phase 0
**Complexity:** L
**Dependencies:** 1.1.1, ConfigManager, EntityTypeLoader
**Tests:** `tests/unit/core/test_entity_service.py::TestEntityCreation` (5 tests)

**Objective:** Implement entity creation with file writes and validation.

**File:** `src/semops/core/services/entity_service.py`

**Implementation Steps:**

1. **Create EntityService class:**
   ```python
   class EntityService:
       def __init__(self, project_root: Path, config_manager: ConfigManager):
           self.project_root = project_root
           self.config_manager = config_manager
           self.entities_dir = project_root / ".semops" / "entities"

       def create_entity(
           self,
           entity_type: str,
           data: Dict[str, Any],
           actor_id: str
       ) -> Dict[str, Any]:
           """Create new entity and write to canonical file."""
           pass
   ```

2. **Implement creation logic:**
   - Validate required fields
   - Validate actor_id not None
   - Generate unique entity_id: `{PREFIX}-{counter}-{slug}`
   - Set timestamps (created_at, updated_at)
   - Write markdown file with frontmatter
   - Return entity dict

3. **File writing:**
   - Path: `.semops/entities/{entity_type_dir}/{entity_id}.md`
   - Format: YAML frontmatter + markdown content
   - Use Jinja2 templates if available

**Unskip Tests:**
- `test_create_entity_writes_canonical_file`
- `test_create_entity_validates_required_fields`
- `test_create_entity_requires_actor_id`
- `test_create_entity_generates_unique_id`
- `test_create_entity_sets_timestamps`

**Validation:**
```bash
pytest tests/unit/core/test_entity_service.py::TestEntityCreation -v
```

**Completion Criteria:**
- [ ] All 5 TestEntityCreation tests pass
- [ ] Files written to correct location
- [ ] Frontmatter formatted correctly
- [ ] Actor attribution enforced

---

### Task 1.1.3: Implement Entity Updates
**Status:** 🔴 Blocked by 1.1.2
**Complexity:** M
**Dependencies:** 1.1.2
**Tests:** `tests/unit/core/test_entity_service.py::TestEntityUpdate` (3 tests)

**Objective:** Update entities while preserving frontmatter metadata.

**File:** `src/semops/core/services/entity_service.py` (extend)

**Implementation Steps:**

1. **Add update method:**
   ```python
   def update_entity(
       self,
       entity_id: str,
       data: Dict[str, Any],
       actor_id: str
   ) -> Dict[str, Any]:
       """Update existing entity."""
       # 1. Load current entity
       # 2. Validate actor_id
       # 3. Merge data (preserve non-updated fields)
       # 4. Update updated_at and updated_by_actor_id
       # 5. Write file
       # 6. Return updated entity
       pass
   ```

2. **Frontmatter preservation:**
   - Load existing frontmatter
   - Merge with updates (updates override)
   - Preserve created_at, created_by_actor_id
   - Update updated_at, updated_by_actor_id

**Unskip Tests:**
- `test_update_entity_preserves_frontmatter`
- `test_update_entity_requires_actor_id`
- `test_update_nonexistent_entity_raises_error`

**Validation:**
```bash
pytest tests/unit/core/test_entity_service.py::TestEntityUpdate -v
```

**Completion Criteria:**
- [ ] All 3 TestEntityUpdate tests pass
- [ ] Frontmatter preserved
- [ ] Actor attribution enforced

---

### Task 1.1.4: Implement Entity Retrieval
**Status:** 🔴 Blocked by 1.1.2
**Complexity:** M
**Dependencies:** 1.1.2
**Tests:** `tests/unit/core/test_entity_service.py::TestEntityRetrieval` (3 tests)

**Objective:** Read entities from canonical files and list by type.

**File:** `src/semops/core/services/entity_service.py` (extend)

**Implementation Steps:**

1. **Add get_entity method:**
   ```python
   def get_entity(self, entity_id: str) -> Dict[str, Any]:
       """Get entity by ID from canonical file."""
       # 1. Find file by entity_id
       # 2. Parse frontmatter
       # 3. Parse markdown content
       # 4. Return entity dict
       pass
   ```

2. **Add list_entities method:**
   ```python
   def list_entities(self, entity_type: str) -> List[Dict[str, Any]]:
       """List all entities of given type."""
       # 1. Find all files in entity type directory
       # 2. Load each entity
       # 3. Return list
       pass
   ```

3. **Frontmatter parsing:**
   - Use `python-frontmatter` library or manual parsing
   - Parse YAML between `---` delimiters
   - Return dict with frontmatter fields

**Unskip Tests:**
- `test_get_entity_reads_from_file`
- `test_list_entities_by_type`
- `test_get_nonexistent_entity_raises_error`

**Validation:**
```bash
pytest tests/unit/core/test_entity_service.py::TestEntityRetrieval -v
```

**Completion Criteria:**
- [ ] All 3 TestEntityRetrieval tests pass
- [ ] Frontmatter parsed correctly
- [ ] List returns all entities

---

### Task 1.1.5: Implement Entity Deletion
**Status:** 🔴 Blocked by 1.1.4
**Complexity:** M
**Dependencies:** 1.1.4
**Tests:** `tests/unit/core/test_entity_service.py::TestEntityDeletion` (2 tests)

**Objective:** Delete entities with optional cascade.

**File:** `src/semops/core/services/entity_service.py` (extend)

**Implementation Steps:**

1. **Add delete method:**
   ```python
   def delete_entity(
       self,
       entity_id: str,
       cascade: bool = False,
       actor_id: str = None
   ) -> Dict[str, Any]:
       """Delete entity and optionally children."""
       # 1. Validate actor_id
       # 2. Find entity file
       # 3. If cascade, find and delete children
       # 4. Delete file
       # 5. Return deletion result
       pass
   ```

2. **Cascade logic:**
   - Find child entities (relationships)
   - Delete children first (recursive)
   - Track deleted count

**Unskip Tests:**
- `test_delete_entity_cascade_option`
- `test_delete_entity_requires_actor_id`

**Validation:**
```bash
pytest tests/unit/core/test_entity_service.py::TestEntityDeletion -v
```

**Completion Criteria:**
- [ ] All 2 TestEntityDeletion tests pass
- [ ] Cascade works
- [ ] Actor attribution enforced

---

### Task 1.1.6: Enforce Actor Attribution
**Status:** 🔴 Blocked by 1.1.5
**Complexity:** S
**Dependencies:** 1.1.5
**Tests:** `tests/unit/core/test_entity_service.py::TestActorAttribution` (3 tests)

**Objective:** Ensure all mutations record actor attribution.

**File:** `src/semops/core/services/entity_service.py` (validation)

**Actions:**

1. **Review all mutation methods:**
   - create_entity
   - update_entity
   - delete_entity

2. **Ensure actor_id validation:**
   - All methods check `actor_id is not None`
   - Clear error if missing

3. **Ensure actor recording:**
   - created_by_actor_id on creation
   - updated_by_actor_id on updates

**Unskip Tests:**
- `test_mutation_without_actor_id_rejected`
- `test_created_by_actor_id_recorded`
- `test_updated_by_actor_id_recorded`

**Validation:**
```bash
pytest tests/unit/core/test_entity_service.py::TestActorAttribution -v

# All EntityService tests should pass now
pytest tests/unit/core/test_entity_service.py -v
```

**Completion Criteria:**
- [ ] All 3 TestActorAttribution tests pass
- [ ] All 17 EntityService tests pass
- [ ] Actor attribution enforced consistently

---

## Milestone 1.2: gRPC Server Integration

### Task 1.2.1: Expand EntityService gRPC Server
**Status:** 🔴 Blocked by 1.1.6
**Complexity:** L
**Dependencies:** EntityService complete
**Tests:** `tests/contracts/test_entity_service_server.py`

**Objective:** Implement gRPC server methods to call EntityService.

**File:** `src/server/entity_service_server.py` (expand)

**Implementation Steps:**

1. **Review protobuf schema:**
   - Read `schema/semops/v1/services.proto`
   - Understand request/response types

2. **Implement RPC methods:**
   ```python
   async def CreateEntity(self, request, context):
       """Create entity via EntityService."""
       actor_id = request.actor_id
       if not actor_id:
           raise ValidationError("actor_id is required")
       result = self._service.create_entity(
           entity_type=request.entity_type,
           data=dict(request.variables),
           actor_id=actor_id
       )
       return CreateEntityResponse(entity=result)
   ```
   - If the current protobuf message does not yet include `actor_id`, update the schema first.
   - Do not rely on transport metadata as the long-term source of actor attribution.

3. **Implement all RPC methods:**
   - CreateEntity
   - GetEntity
   - UpdateEntity
   - DeleteEntity
   - ListEntities
   - AnalyzeEntity (contract-aligned with actor-aware expert invocation)

4. **Add tests:**
   - Expand `test_entity_service_server.py`
   - Test each RPC method
   - Test error handling

**Validation:**
```bash
pytest tests/contracts/test_entity_service_server.py -v
```

**Completion Criteria:**
- [ ] All RPC methods implemented
- [ ] Contract tests expanded and passing
- [ ] Error handling works

---

## Milestone 1.3: Projection and Reconciliation (Phase 1 Extension)

**Note:** These tasks can be deferred to Phase 1.5 or skipped for MVP.

### Task 1.3.1: Add Projection Hooks
**Status:** 🔴 Blocked by 1.1.6
**Complexity:** M
**Dependencies:** EntityService complete

**Objective:** Add hooks to update derived indexes after mutations.

**File:** `src/semops/core/services/entity_service.py` (extend)

**Implementation:** Add `_update_projections()` method called after each mutation.

**Tests:** Create `tests/integration/test_projection_sync.py`

---

## Phase 1 Summary

**Total Tasks:** 8
**Total Tests:** 17 unit + contract tests

**Completion Checklist:**
- [ ] EntityService complete (17 tests)
- [ ] gRPC server expanded
- [ ] Contract tests passing
- [ ] File-first CRUD working

**When Phase 1 is complete:**
```bash
# All Phase 1 tests should pass
pytest -m skip_until_phase1 -v

# Summary check
pytest tests/unit/core/test_entity_service.py tests/contracts/test_entity_service_server.py -v
```

---

# Phase 2: Journey + Template Runtime

**Note:** Phase 2 is execution-critical for ADR-0003 and external-agent readiness. Include explicit conformance and parity tests before marking complete.

## Milestone 2.1: ExpertService

### Task 2.1.1: Implement ExpertService
**Objective:** Expert resolution and invocation with actor_id.

**File:** `src/semops/core/services/expert_service.py`

**Tests:** Create `tests/unit/core/test_expert_service.py`

**Required tests (minimum):**
- request rejected when `actor_id` missing
- selector contract enforcement (`expert_type` xor `requested_role`)
- package-first role resolution
- core fallback role resolution
- response metadata includes:
  - `requested_role`
  - `resolved_expert_type`
  - `resolution_source`
  - `trace_id`

---

### Task 2.1.2: Implement Expert Contract Conformance Tests
**Objective:** Enforce ADR-0003 across service and adapter boundaries.

**Tests:** Create `tests/contracts/test_expert_invocation_contract.py`

**Required tests (minimum):**
- gRPC/FastAPI/MCP request semantics are equivalent
- missing `actor_id` rejected across interfaces
- same input yields same `resolved_expert_type` and response metadata
- invalid selector combinations rejected consistently

---

## Milestone 2.2: Journey Execution

### Task 2.2.1: Implement Journey Executor
**Objective:** Execute journey stages (human.create, ai.assist, etc.).

**File:** `src/semops/core/services/journey_executor.py`

**Tests:** Create `tests/integration/test_journey_execution.py`

**Required tests (minimum):**
- `ai.assist` stage role alias resolves through ExpertInvocationAdapter
- journey runtime forwards `actor_id` into expert invocation
- system.commit still routes through EntityService mutation boundary

---

## Milestone 2.3: Template Management

### Task 2.3.1: Implement TemplateService
**Objective:** Template version management and migration.

**File:** `src/semops/core/services/template_service.py`

**Tests:** Create `tests/unit/core/test_template_service.py`

---

## Phase 2 Summary

**Completion Checklist:**
- [ ] ExpertService complete
- [ ] ADR-0003 selector + metadata conformance verified
- [ ] Journey execution works
- [ ] Template migration works
- [ ] E2E journey completes

---

# Task Dependencies Diagram

```
Phase 0:
0.1.1 (Structure) ─┬─► 0.1.2 (Exceptions) ─┬─► 0.2.1 (ConfigManager Discovery)
                   │                        │
                   │                        ├─► 0.5.1 (LLM Client)
                   │                        └─► 0.5.2 (Vector Store)
                   │
                   └─────────────────────────────────► [All other tasks need structure]

0.2.1 ─► 0.2.2 ─► 0.2.3 ─► 0.2.4 (ConfigManager Complete)
                                  │
                                  ├─► 0.3.1 ─► 0.3.2 ─► 0.3.3 (EntityTypeLoader Complete)
                                  │                              │
                                  └──────────────────────────────┴─► 0.4.1 ─► 0.4.2 ─► 0.4.3 (PackageLoader Complete)
                                                                                                    │
0.2.4 + 0.3.3 + 0.4.3 ───────────────────────────────────────────────────────────────────────────┴─► 0.6.1 (Integration)

Phase 1:
[Phase 0 Complete] ─► 1.1.1 ─► 1.1.2 ─┬─► 1.1.3 (Update)
                                       ├─► 1.1.4 (Retrieval)
                                       └─► 1.1.5 (Deletion) ─► 1.1.6 (Attribution)
                                                                       │
                                                                       └─► 1.2.1 (gRPC Server)

Phase 2:
[Phase 1 Complete] ─► 2.1.1 (ExpertService) ─┬─► 2.2.1 (Journey Executor)
                                              └─► 2.3.1 (TemplateService)
```

---

# Quick Reference Commands

## Check Test Status
```bash
# Count tests by phase
pytest -m skip_until_phase0 --collect-only -q | grep collected
pytest -m skip_until_phase1 --collect-only -q | grep collected

# Run specific task tests
pytest tests/unit/config/test_config_manager.py::TestProjectRootDiscovery -v

# Run all passing tests
pytest -v
```

## Implementation Workflow
```bash
# 1. Create implementation file
touch src/semops/core/config/config_manager.py

# 2. Edit test file, unskip ONE test
# Remove @pytest.mark.skip from one test

# 3. Run test (should fail)
pytest tests/unit/config/test_config_manager.py::TestProjectRootDiscovery::test_discover_project_root_from_semops_marker -v

# 4. Implement minimal code

# 5. Run test (should pass)
pytest tests/unit/config/test_config_manager.py::TestProjectRootDiscovery::test_discover_project_root_from_semops_marker -v

# 6. Repeat
```

## Progress Tracking
```bash
# Check how many tests pass
pytest tests/unit/config/ -v --tb=no | grep -E "passed|failed|skipped"

# Generate coverage report
pytest tests/unit/config/ --cov=src/semops/core/config --cov-report=term-missing
```

---

# Success Metrics

## Phase 0 Complete:
- [ ] 50/50 baseline tests passing (config + current adapters + integration)
- [ ] ConfigManager loads config from `.semops/`
- [ ] Entity packages loaded with experts
- [ ] Expert resolution works
- [ ] LLM client interface works
- [ ] Vector store interface works
- [ ] PromptRegistry, RAGPipelineExecutor, API/MCP adapters, and ExpertInvocationAdapter tests added and passing

## Phase 1 Complete:
- [ ] 17/17 EntityService tests passing
- [ ] Create/read/update/delete entities
- [ ] Files written to canonical location
- [ ] Actor attribution enforced
- [ ] gRPC server works

## Phase 2 Complete:
- [ ] ExpertService works
- [ ] Journey stages execute
- [ ] Template migration works
- [ ] E2E journey completes

---

**Last Updated:** 2026-02-26
**Total Tasks:** 29+ tasks (19 Phase 0, 8 Phase 1, 2+ Phase 2)
**Total Tests:** 81 currently collected + Phase 2 and conformance tests to be added

**Ready for agent execution once new adapter/conformance tests are added and unskipped.**
