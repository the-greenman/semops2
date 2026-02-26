# Quick Start Guide for Agents

**Welcome!** This guide gets you started implementing SemOps2 using Test-Driven Development.

## 📋 Prerequisites

1. **Read these files first:**
   - [TDD_SETUP_COMPLETE.md](TDD_SETUP_COMPLETE.md) - What's already done
   - [tests/AGENT_GUIDE.md](tests/AGENT_GUIDE.md) - Detailed implementation guide
   - [docs/progress/AGENT_TASK_LIST.md](docs/progress/AGENT_TASK_LIST.md) - Task breakdown

2. **Verify test infrastructure:**
   ```bash
   cd /workspace
   pytest tests/ --collect-only -q
   # Should show: 81 tests collected
   ```

## 🎯 Start Here: Phase 0, Task 0.1.1

### Step 1: Create Module Structure

```bash
# Create directories
mkdir -p src/semops/core/config
mkdir -p src/semops/core/services
mkdir -p src/semops/core/adapters
mkdir -p src/semops/core/models

# Create __init__.py files
touch src/semops/core/__init__.py
touch src/semops/core/config/__init__.py
touch src/semops/core/services/__init__.py
touch src/semops/core/adapters/__init__.py
touch src/semops/core/models/__init__.py
```

**Verify:**
```bash
pytest tests/ --collect-only -q
# Should still show: 81 tests collected
```

**✅ Task 0.1.1 Complete!** Move to Task 0.1.2.

---

### Step 2: Create Exception Classes

**File:** `src/semops/core/exceptions.py`

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

**Verify:**
```bash
python -c "from semops.core.exceptions import ConfigurationError; print('OK')"
```

**✅ Task 0.1.2 Complete!** Move to Task 0.2.1.

---

### Step 3: Implement ConfigManager (Project Root Discovery)

**File:** `src/semops/core/config/config_manager.py`

```python
"""Configuration manager for SemOps2."""

from pathlib import Path
from typing import Optional
import subprocess
from semops.core.exceptions import ConfigurationError


class ConfigManager:
    """Manages SemOps configuration loading and discovery."""

    def __init__(self, working_dir: Optional[Path] = None):
        """Initialize ConfigManager.

        Args:
            working_dir: Directory to start search from. Defaults to cwd.
        """
        self.working_dir = Path(working_dir) if working_dir else Path.cwd()
        self.project_root = self._discover_project_root()

    def _discover_project_root(self) -> Path:
        """Discover project root from working directory.

        Resolution order:
        1. Look for .semops-project marker file
        2. Look for .semops/ directory
        3. Check git root for .semops/
        4. Raise error if not found

        Returns:
            Path to project root

        Raises:
            ConfigurationError: If no project root found
        """
        current = self.working_dir.resolve()

        # Walk up directory tree
        for parent in [current] + list(current.parents):
            # Check for .semops-project marker
            if (parent / ".semops-project").exists():
                return parent

            # Check for .semops/ directory
            if (parent / ".semops").is_dir():
                return parent

        # Try git root
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=current,
                capture_output=True,
                text=True,
                check=True
            )
            git_root = Path(result.stdout.strip())
            if (git_root / ".semops").is_dir():
                return git_root
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Not found
        raise ConfigurationError(
            f"No SemOps project root found from {self.working_dir}\n"
            f"Looked for:\n"
            f"  - .semops-project marker file\n"
            f"  - .semops/ directory\n"
            f"  - Git repository root with .semops/\n\n"
            f"Initialize a new project with: semops init"
        )
```

**Now unskip ONE test:**

Edit `tests/unit/config/test_config_manager.py`:
- Find `test_discover_project_root_from_semops_marker`
- Remove the `@pytest.mark.skip(reason="...")` decorator

**Run the test:**
```bash
pytest tests/unit/config/test_config_manager.py::TestProjectRootDiscovery::test_discover_project_root_from_semops_marker -v
```

**Expected:** ✅ Test passes!

**Continue:** Unskip the next test, run it, make it pass. Repeat for all 4 tests in `TestProjectRootDiscovery`.

---

## 🔄 TDD Cycle

For every feature, follow this cycle:

```
1. Unskip ONE test
   └─► Edit test file, remove @pytest.mark.skip

2. Run test (should FAIL)
   └─► pytest path/to/test::TestClass::test_method -v

3. Implement minimal code
   └─► Write just enough to pass the test

4. Run test (should PASS)
   └─► pytest path/to/test::TestClass::test_method -v

5. Refactor (optional)
   └─► Improve code while keeping tests green

6. Repeat for next test
```

## 📊 Track Progress

```bash
# See how many tests pass
pytest tests/unit/config/test_config_manager.py -v --tb=no

# Check Phase 0 progress
pytest -m skip_until_phase0 -v --tb=no

# Generate coverage
pytest tests/unit/config/ --cov=src/semops/core/config --cov-report=term-missing
```

## 🗺️ Task Order

**Phase 0 (Foundation):**
1. ✅ Module structure (Task 0.1.1)
2. ✅ Exceptions (Task 0.1.2)
3. 🟡 ConfigManager Discovery (Task 0.2.1) ← **START HERE**
4. ConfigManager Loading (Task 0.2.2)
5. ConfigManager Namespace (Task 0.2.3)
6. ConfigManager Errors (Task 0.2.4)
7. EntityTypeLoader (Tasks 0.3.1-0.3.3)
8. PackageLoader (Tasks 0.4.1-0.4.3)
9. LLM Client (Task 0.5.1)
10. Vector Store (Task 0.5.2)
11. Integration Tests (Task 0.6.1)

**Phase 1 (Entity Service):**
12. Entity models (Task 1.1.1)
13. Entity creation (Task 1.1.2)
14. Entity updates (Task 1.1.3)
15. Entity retrieval (Task 1.1.4)
16. Entity deletion (Task 1.1.5)
17. Actor attribution (Task 1.1.6)
18. gRPC server (Task 1.2.1)

**Phase 2 (Journeys):**
19. ExpertService (Task 2.1.1)
20. Journey executor (Task 2.2.1)
21. TemplateService (Task 2.3.1)

## 📚 Key Files

**Tests:**
- `tests/unit/config/test_config_manager.py` (12 tests)
- `tests/unit/config/test_entity_type_loader.py` (15 tests)
- `tests/unit/config/test_package_loader.py` (14 tests)
- `tests/unit/core/test_entity_service.py` (17 tests)

**Implementation:**
- `src/semops/core/config/config_manager.py`
- `src/semops/core/config/entity_type_loader.py`
- `src/semops/core/config/package_loader.py`
- `src/semops/core/services/entity_service.py`

**Documentation:**
- `tests/README.md` - Test suite overview
- `tests/AGENT_GUIDE.md` - Detailed implementation guide
- `docs/progress/AGENT_TASK_LIST.md` - Complete task breakdown
- `docs/IMPLEMENTATION_PLAN.md` - Architecture plan

## 🆘 When Stuck

### Test Won't Pass
1. Read the test docstring (Given/When/Then)
2. Check the assertions to see what's expected
3. Look at the fixture setup in `conftest.py`
4. Run with `-vvs` for full output: `pytest test_file.py::test_name -vvs`

### Import Error
```bash
# Make sure you're in project root
cd /workspace

# Check module structure
ls -la src/semops/core/

# Verify __init__.py files exist
find src -name "__init__.py"
```

### Fixture Not Working
```bash
# Check fixture definition
grep -r "def temp_semops_project" tests/

# View fixture code
cat tests/conftest.py | grep -A 30 "def temp_semops_project"
```

### Don't Know What to Implement
1. Read the test name - it tells you what to build
2. Look at the assertions - they show expected behavior
3. Check the docstring - it has Given/When/Then
4. See `tests/AGENT_GUIDE.md` for examples

## ✅ Success Criteria

### ConfigManager Complete (12 tests):
```bash
pytest tests/unit/config/test_config_manager.py -v
# All 12 tests should pass
```

### Phase 0 Complete (48 tests):
```bash
pytest -m skip_until_phase0 -v
# All 48 tests should pass
```

### Phase 1 Complete (17 tests):
```bash
pytest tests/unit/core/test_entity_service.py -v
# All 17 tests should pass
```

## 🎓 Learning Resources

- **pytest docs:** https://docs.pytest.org/
- **TDD intro:** https://en.wikipedia.org/wiki/Test-driven_development
- **Python type hints:** https://docs.python.org/3/library/typing.html
- **Pydantic:** https://docs.pydantic.dev/

## 🚀 Ready to Start!

You now have everything you need:
- ✅ 81 tests written and ready
- ✅ Test infrastructure configured
- ✅ Fixtures and mocks available
- ✅ Documentation complete
- ✅ Task list with clear order

**Start with Task 0.1.1 and follow the TDD cycle!**

Questions? Check:
1. `tests/AGENT_GUIDE.md` for detailed instructions
2. `docs/progress/AGENT_TASK_LIST.md` for task breakdown
3. Test docstrings for expected behavior

Good luck! 🎯
