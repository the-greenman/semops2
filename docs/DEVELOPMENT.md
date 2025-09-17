# SemOps2 Development Guide

This document provides guidelines for developing with the SemOps2 repository, including information about Git hooks, testing, and generated code management.

## Table of Contents

- [Git Hooks Overview](#git-hooks-overview)
- [Generated Files Policy](#generated-files-policy)
- [Testing Requirements](#testing-requirements)
- [Development Workflow](#development-workflow)
- [Troubleshooting](#troubleshooting)
- [Emergency Procedures](#emergency-procedures)

## Git Hooks Overview

SemOps2 uses Git hooks to enforce repository quality standards automatically. These hooks ensure code consistency, prevent accidental corruption of generated files, and maintain high code quality.

### Pre-commit Hook

**Location**: `.git/hooks/pre-commit`

**Purpose**: Validates commits before they are created

**Checks performed**:
1. **Generated File Protection**: Prevents manual modifications to generated code
2. **Quick Tests**: Runs fast validation tests (pytest + buf lint)
3. **Schema Formatting**: Ensures protobuf schemas are properly formatted

**Execution time**: ~30-60 seconds

### Pre-push Hook

**Location**: `.git/hooks/pre-push`

**Purpose**: Comprehensive validation before pushing to remote

**Checks performed**:
1. **Repository State**: Validates working directory and staging area
2. **Schema Integrity**: Deep validation of protobuf schemas
3. **Generated File Consistency**: Ensures generated files match schemas
4. **Comprehensive Tests**: Full test suite with coverage
5. **Sensitive Information**: Scans for accidentally committed secrets

**Execution time**: ~2-5 minutes

## Generated Files Policy

### Protected File Patterns

The following files are automatically generated and **must not be manually edited**:

```
src/semops/generated/**/*.py      # Python protobuf code
src/semops/generated/**/*.pyi     # Python type stubs
generated/docs/**/*               # Generated documentation
generated/api/**/*                # OpenAPI specifications
*.pb2.py                          # Protocol buffer message classes
*_pb2.py                          # Protocol buffer message classes
*.pb2_grpc.py                     # gRPC service stubs
*_pb2_grpc.py                     # gRPC service stubs
*.swagger.json                    # Swagger/OpenAPI specs
*.swagger.yaml                    # Swagger/OpenAPI specs
```

### Regeneration Process

When you need to update generated files:

1. **Modify source schemas** in `schema/**/*.proto`
2. **Update configuration** if needed (`buf.yaml`, `buf.gen.yaml`)
3. **Regenerate code**:
   ```bash
   buf generate
   ```
4. **Commit both schema changes and generated files**:
   ```bash
   git add schema/ src/semops/generated/ generated/
   git commit -m "Update entity schema and regenerate code"
   ```

### Schema File Patterns

Changes to these files trigger regeneration validation:

```
schema/**/*.proto                 # Protocol buffer schemas
buf.yaml                          # Buf workspace configuration
buf.gen.yaml                      # Code generation configuration
```

## Testing Requirements

### Test Modes

#### Quick Mode (Pre-commit)
- **Command**: `scripts/test-runner.sh quick`
- **Duration**: ~30-60 seconds
- **Includes**:
  - Basic pytest execution
  - Schema linting (`buf lint`)
  - Format validation (`buf format --diff`)

#### Full Mode (Pre-push/CI)
- **Command**: `scripts/test-runner.sh full`
- **Duration**: ~2-5 minutes
- **Includes**:
  - Comprehensive pytest with coverage
  - Schema validation and generation testing
  - Generated file consistency checks

### Running Tests Manually

```bash
# Quick validation (pre-commit style)
scripts/test-runner.sh quick

# Full test suite (pre-push style)
scripts/test-runner.sh full

# Check generated file consistency
scripts/validate-generated.sh check

# Regenerate all generated files
scripts/validate-generated.sh regenerate
```

### Test Configuration

- **Test Location**: `tests/`
- **Test Runner**: pytest
- **Coverage Target**: 80%
- **Python Environment**: Automatically detected (venv or system)

## Development Workflow

### Standard Workflow

1. **Create feature branch**:
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes** to source code or schemas

3. **If schemas changed, regenerate code**:
   ```bash
   buf generate
   ```

4. **Run tests locally**:
   ```bash
   scripts/test-runner.sh quick
   ```

5. **Commit changes** (hooks will validate automatically):
   ```bash
   git add .
   git commit -m "Add new feature"
   ```

6. **Push to remote** (comprehensive validation will run):
   ```bash
   git push origin feature/my-feature
   ```

### Schema Development Workflow

1. **Modify protobuf schemas** in `schema/`

2. **Validate schemas**:
   ```bash
   buf lint
   buf format --diff
   ```

3. **Regenerate code**:
   ```bash
   buf generate
   ```

4. **Update tests** if interfaces changed

5. **Commit schema and generated code together**:
   ```bash
   git add schema/ src/semops/generated/ generated/ tests/
   git commit -m "Update schema: add new entity fields"
   ```

### Dependency Updates

1. **Update buf dependencies**:
   ```bash
   buf dep update
   ```

2. **Regenerate code** with new dependencies:
   ```bash
   buf generate
   ```

3. **Test thoroughly**:
   ```bash
   scripts/test-runner.sh full
   ```

4. **Commit updated lock file and generated code**:
   ```bash
   git add buf.lock src/semops/generated/ generated/
   git commit -m "Update protobuf dependencies"
   ```

## Troubleshooting

### Common Issues

#### "Generated file modified" Error

**Problem**: Hook detects manual changes to generated files

**Solution**:
```bash
# Check which files are problematic
scripts/validate-generated.sh check

# Regenerate clean files
buf generate

# Stage the regenerated files
git add src/semops/generated/ generated/

# Commit
git commit -m "Regenerate protobuf code"
```

#### "Tests failed" Error

**Problem**: Tests are failing in pre-commit hook

**Solution**:
```bash
# Run tests manually to see details
scripts/test-runner.sh quick

# Fix the failing tests
# Then commit again
git commit -m "Fix tests"
```

#### "Schema formatting" Error

**Problem**: Protobuf schemas are not properly formatted

**Solution**:
```bash
# Auto-fix formatting
buf format -w

# Stage the formatted files
git add schema/

# Commit
git commit -m "Fix schema formatting"
```

#### "Generated files out of sync" Error

**Problem**: Generated files don't match current schemas

**Solution**:
```bash
# Regenerate all files
buf generate

# Check what changed
git diff src/semops/generated/ generated/

# Stage and commit the updates
git add src/semops/generated/ generated/
git commit -m "Sync generated files with schemas"
```

### Hook Debugging

#### Enable Verbose Output

```bash
# For test runner
VERBOSE=true scripts/test-runner.sh quick

# For validation script
scripts/validate-generated.sh check --verbose
```

#### Check Hook Logs

Hooks log their output to the terminal. If you need to debug:

1. **Test hooks manually**:
   ```bash
   .git/hooks/pre-commit
   .git/hooks/pre-push origin https://github.com/user/repo.git
   ```

2. **Check script permissions**:
   ```bash
   ls -la .git/hooks/pre-*
   ls -la scripts/*.sh
   ```

3. **Verify script locations**:
   ```bash
   find . -name "test-runner.sh" -o -name "validate-generated.sh"
   ```

## Emergency Procedures

### Bypassing Hooks

**⚠️ Use only in emergencies** - hooks exist for important reasons!

#### Skip Pre-commit Hook

```bash
git commit --no-verify -m "Emergency commit"
```

#### Skip Pre-push Hook

```bash
git push --no-verify origin branch-name
```

### Fixing Broken Repository State

#### Reset Generated Files

```bash
# Remove all generated files
rm -rf src/semops/generated/ generated/

# Regenerate from clean state
buf generate

# Stage and commit
git add src/semops/generated/ generated/
git commit -m "Reset generated files to clean state"
```

#### Reset Hooks

```bash
# Re-copy hooks from repository
cp scripts/hooks/pre-commit .git/hooks/
cp scripts/hooks/pre-push .git/hooks/
chmod +x .git/hooks/pre-*
```

### Recovery Commands

#### Restore Working Directory

```bash
# Discard all local changes
git reset --hard HEAD

# Clean untracked files
git clean -fd

# Regenerate files
buf generate
```

#### Fix Dependency Issues

```bash
# Update all dependencies
buf dep update

# Regenerate code
buf generate

# Run full test suite
scripts/test-runner.sh full
```

## Environment Setup

### Required Tools

- **Python 3.8+**: For running tests and generated code
- **buf**: For protocol buffer management
- **Git**: Version control with hooks

### Optional Tools

- **Virtual Environment**: Recommended for Python dependency isolation
- **IDE with Protobuf Support**: For better schema editing experience

### Environment Variables

- `PYTHON_CMD`: Python command to use (default: `python3`)
- `VENV_PATH`: Virtual environment path (default: `.venv`)
- `VERBOSE`: Enable verbose output (default: `false`)

## Best Practices

### Commit Messages

- Use clear, descriptive commit messages
- Include "regenerate" in messages when updating generated files
- Reference issue numbers when applicable

### Branch Naming

- Use descriptive branch names
- Include issue numbers: `feature/123-add-validation`
- Use prefixes: `feature/`, `bugfix/`, `hotfix/`

### Testing

- Write tests for new features
- Update tests when changing interfaces
- Ensure tests pass before committing

### Schema Design

- Use semantic versioning for breaking changes
- Add field comments and validation rules
- Consider backward compatibility

## Support

For issues with hooks or development workflow:

1. Check this documentation
2. Review troubleshooting section
3. Check project issue tracker
4. Contact development team

---

**Remember**: Hooks are designed to help maintain code quality. If you find yourself frequently bypassing them, consider whether the underlying issue needs to be addressed rather than worked around.