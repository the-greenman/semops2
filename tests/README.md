# SemOps2 Test Suite

This directory contains the comprehensive test suite for SemOps2, organized using Test-Driven Development (TDD) principles.

## Test Structure

```
tests/
├── unit/                          # Fast, isolated unit tests
│   ├── config/                    # ✅ Config system tests
│   │   ├── test_config_manager.py
│   │   ├── test_entity_type_loader.py
│   │   └── test_package_loader.py
│   ├── core/                      # ✅ Core service tests
│   │   ├── test_entity_service.py
│   │   ├── test_expert_service.py      # TODO: Phase 2
│   │   └── test_template_service.py    # TODO: Phase 2
│   └── adapters/                  # ✅ Adapter interface tests
│       ├── test_llm_client_interface.py
│       └── test_vector_store_interface.py
├── integration/                   # Component integration tests
│   ├── test_config_loading.py     # ✅ Phase 0
│   ├── test_entity_crud_file_ops.py    # TODO: Phase 1
│   ├── test_projection_sync.py          # TODO: Phase 1
│   └── test_journey_execution.py        # TODO: Phase 2
├── contracts/                     # gRPC contract tests
│   ├── test_entity_service_server.py    # EXISTS (needs expansion)
│   └── test_expert_service_server.py    # TODO: Phase 2
├── cli/                          # CLI integration tests
│   ├── test_entity_service_integration.py  # EXISTS (needs expansion)
│   └── test_journey_cli.py                 # TODO: Phase 2
└── e2e/                          # End-to-end tests
    ├── test_domain_journey_flow.py     # TODO: Phase 2
    └── test_template_migration_flow.py  # TODO: Phase 2
```

## Test Markers

Use pytest markers to organize and run specific test categories:

```bash
# Run all unit tests (fast)
pytest -m unit

# Run integration tests
pytest -m integration

# Run tests for Phase 0 features
pytest -m skip_until_phase0

# Run tests for Phase 1 features
pytest -m skip_until_phase1

# Run contract tests
pytest -m contract

# Run all tests except e2e
pytest -m "not e2e"
```

## Test Phases

### ✅ Phase 0: Foundation (Config + Adapters)
**Status: Test structure complete, implementation pending**

Tests created:
- `test_config_manager.py` - Project root discovery, layered loading, namespace validation
- `test_entity_type_loader.py` - Entity type loading, validation, registry
- `test_package_loader.py` - Entity package loading, expert resolution, journey validation
- `test_llm_client_interface.py` - Structured LLM output, retry logic, metadata
- `test_vector_store_interface.py` - Vector store interface, Chroma/Qdrant parity
- `test_config_loading.py` (integration) - End-to-end config loading

**Activation Plan:**
1. Unskip tests progressively as implementation completes
2. Start with `test_config_manager.py::TestProjectRootDiscovery`
3. Then `test_entity_type_loader.py::TestEntityTypeLoading`
4. Follow dependency chain through integration tests

### 🔄 Phase 1: Entity Service (File-First CRUD)
**Status: Unit tests complete, integration tests TODO**

Tests created:
- ✅ `test_entity_service.py` - Full CRUD operations, actor attribution, validation

Tests TODO:
- `test_entity_crud_file_ops.py` (integration) - End-to-end file operations
- `test_projection_sync.py` (integration) - Graph/vector projection sync
- Update `test_entity_service_server.py` (contract) - gRPC contract tests

### 📋 Phase 2: Journey + Template Runtime
**Status: Tests TODO**

Tests TODO:
- `test_expert_service.py` (unit) - Expert resolution and invocation
- `test_template_service.py` (unit) - Template version management
- `test_journey_execution.py` (integration) - Journey stage execution
- `test_domain_journey_flow.py` (e2e) - Complete domain journey
- `test_template_migration_flow.py` (e2e) - Template migration
- `test_journey_cli.py` (cli) - CLI journey commands

## Running Tests

### Quick validation (fast tests only)
```bash
pytest -m "unit and not slow"
```

### Full test suite
```bash
pytest
```

### Specific phase
```bash
pytest -m skip_until_phase0
```

### Watch mode (for TDD)
```bash
pytest-watch
```

### Coverage report
```bash
pytest --cov=src --cov-report=html
```

## Test Fixtures

Common fixtures are defined in `conftest.py`:

- `temp_dir` - Temporary directory (auto-cleanup)
- `temp_semops_project` - Complete .semops/ project structure
- `temp_entity_packages_dir` - Entity packages directory with sample domain
- `sample_entity_data` - Sample domain entity data
- `sample_entity_id` - Sample entity ID
- `mock_llm_client` - Mock LLM client with canned responses
- `mock_vector_store` - Mock vector store

## Writing New Tests

### TDD Workflow

1. **Write failing test first**
   ```python
   @pytest.mark.skip(reason="Feature not implemented")
   def test_new_feature():
       # Given: Setup
       # When: Action
       # Then: Assertion
       assert expected == actual
   ```

2. **Run test to see it fail**
   ```bash
   pytest tests/unit/test_module.py::test_new_feature
   ```

3. **Implement minimal code to pass**

4. **Unskip test and verify pass**
   ```python
   # Remove @pytest.mark.skip decorator
   def test_new_feature():
       ...
   ```

5. **Refactor with tests as safety net**

### Test Naming Convention

- Test files: `test_<module_name>.py`
- Test classes: `Test<Feature>` (e.g., `TestEntityCreation`)
- Test methods: `test_<behavior>` (descriptive, no "should")

Examples:
- ✅ `test_create_entity_requires_actor_id`
- ✅ `test_expert_resolution_package_first`
- ❌ `test_entity` (too vague)
- ❌ `test_should_create_entity` (redundant "should")

### Test Structure (AAA Pattern)

```python
def test_feature_behavior():
    """Feature should behave in specific way.

    Given: Initial state and context
    When: Action is performed
    Then: Expected outcome occurs
    """
    # Arrange - Set up test data and dependencies
    service = MyService()
    data = {"key": "value"}

    # Act - Perform the action
    result = service.do_something(data)

    # Assert - Verify the outcome
    assert result.success is True
    assert result.data == expected_data
```

## Test Requirements

### Unit Tests
- ✅ No I/O operations (use mocks)
- ✅ Fast execution (< 100ms per test)
- ✅ Isolated (no test interdependencies)
- ✅ Single concept per test
- ✅ Clear failure messages

### Integration Tests
- ✅ May use fixtures and temp files
- ✅ Test component interactions
- ✅ Moderate execution time (< 1s per test)
- ✅ Setup/teardown in fixtures

### E2E Tests
- ✅ Test complete user workflows
- ✅ May be slower (< 10s per test)
- ✅ Minimal mocking
- ✅ Representative of real usage

## Continuous Integration

Tests run automatically on:
- Every commit (fast unit tests)
- Pull requests (full test suite)
- Main branch (full suite + coverage)

CI Configuration: `.github/workflows/test.yml` (TODO)

## Test Coverage Goals

- Unit test coverage: > 90%
- Integration test coverage: > 80%
- E2E test coverage: Key workflows only
- Critical paths: 100% coverage

## Troubleshooting

### Tests are skipped
- Check if you need to unskip tests as features are implemented
- Remove `@pytest.mark.skip` decorators

### Import errors
- Ensure you're running from project root
- Check PYTHONPATH includes `src/` directory

### Fixture not found
- Verify fixture is defined in `conftest.py` or test file
- Check fixture scope (function, class, module, session)

### Slow tests
- Profile with `pytest --durations=10`
- Move slow tests to integration or e2e
- Use mocks instead of real I/O

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
- [AAA Pattern](https://docs.pytest.org/en/stable/explanation/anatomy.html)
- Implementation Plan: `/workspace/docs/IMPLEMENTATION_PLAN.md`
