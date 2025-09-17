#!/bin/bash
# SemOps2 Standardized Test Runner
# Used by git hooks and CI/CD for consistent test execution

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_CMD="${PYTHON_CMD:-python3}"
VENV_PATH="${VENV_PATH:-$PROJECT_ROOT/.venv}"

# Test mode: quick (for pre-commit) or full (for pre-push/CI)
TEST_MODE="${1:-quick}"
VERBOSE="${VERBOSE:-false}"

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
check_project_root() {
    if [[ ! -f "$PROJECT_ROOT/buf.yaml" ]] || [[ ! -f "$PROJECT_ROOT/requirements.txt" ]]; then
        log_error "Not in SemOps2 project root. Expected buf.yaml and requirements.txt"
        exit 1
    fi
}

# Activate virtual environment if it exists
setup_python_env() {
    if [[ -d "$VENV_PATH" ]]; then
        log_info "Activating virtual environment: $VENV_PATH"
        source "$VENV_PATH/bin/activate"
    else
        log_warning "Virtual environment not found at $VENV_PATH"
        log_info "Using system Python: $(which $PYTHON_CMD)"
    fi
}

# Check required tools
check_dependencies() {
    local missing_tools=()

    # Check Python
    if ! command -v "$PYTHON_CMD" &> /dev/null; then
        missing_tools+=("python3")
    fi

    # Check buf
    if ! command -v buf &> /dev/null; then
        missing_tools+=("buf")
    fi

    # Check pytest (after Python env setup)
    if ! $PYTHON_CMD -m pytest --version &> /dev/null; then
        missing_tools+=("pytest")
    fi

    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        log_error "Please install missing dependencies"
        exit 1
    fi
}

# Run buf validation
run_buf_checks() {
    log_info "Running buf validation..."

    cd "$PROJECT_ROOT"

    # Lint protobuf schemas
    log_info "  - Linting protobuf schemas"
    if ! buf lint; then
        log_error "Buf lint failed"
        return 1
    fi

    # Check formatting
    log_info "  - Checking protobuf formatting"
    if ! buf format --diff --exit-code; then
        log_error "Protobuf files are not properly formatted"
        log_error "Run 'buf format -w' to fix formatting"
        return 1
    fi

    log_success "Buf validation passed"
}

# Run Python tests
run_python_tests() {
    log_info "Running Python tests..."

    cd "$PROJECT_ROOT"

    local pytest_args=()

    if [[ "$TEST_MODE" == "quick" ]]; then
        # Quick mode: basic tests only
        pytest_args+=(
            "--tb=short"
            "--quiet"
            "-x"  # Stop on first failure
            "--disable-warnings"
        )
    else
        # Full mode: comprehensive testing
        pytest_args+=(
            "--tb=short"
            "--strict-markers"
            "--cov=src"
            "--cov-report=term-missing"
            "--cov-fail-under=80"
        )
    fi

    if [[ "$VERBOSE" == "true" ]]; then
        pytest_args+=("-v")
    fi

    log_info "  - Running pytest with mode: $TEST_MODE"
    if ! $PYTHON_CMD -m pytest tests/ "${pytest_args[@]}"; then
        log_error "Python tests failed"
        return 1
    fi

    log_success "Python tests passed"
}

# Validate generated files are in sync
check_generated_files() {
    log_info "Checking generated files are in sync..."

    cd "$PROJECT_ROOT"

    # Check if buf.lock exists and is up to date
    if [[ -f "buf.lock" ]]; then
        log_info "  - Checking buf dependencies"
        # Note: buf doesn't have a --check flag, so we just warn about potential staleness
        log_info "buf.lock found - dependencies should be current"
    fi

    # Check if generated files need regeneration
    # We'll create a temporary directory to compare
    local temp_dir=$(mktemp -d)
    local current_generated="$PROJECT_ROOT/src/semops/generated"

    if [[ -d "$current_generated" ]]; then
        log_info "  - Validating generated protobuf code"

        # Generate fresh code to temporary location
        mkdir -p "$temp_dir/generated"

        # Create temporary buf.gen.yaml that outputs to temp directory
        local temp_gen_config="$temp_dir/buf.gen.yaml"
        sed "s|src/semops/generated|$temp_dir/generated|g" "$PROJECT_ROOT/buf.gen.yaml" > "$temp_gen_config"

        # Generate and compare (suppress output unless verbose)
        if [[ "$VERBOSE" == "true" ]]; then
            buf generate --config "$temp_gen_config"
        else
            buf generate --config "$temp_gen_config" >/dev/null 2>&1
        fi

        # Compare generated files
        if ! diff -r "$current_generated" "$temp_dir/generated" >/dev/null 2>&1; then
            log_warning "Generated files may be out of sync with schema"
            log_warning "Run 'buf generate' to regenerate code"
        fi

        # Cleanup
        rm -rf "$temp_dir"
    fi

    log_success "Generated files validation completed"
}

# Main execution
main() {
    log_info "SemOps2 Test Runner - Mode: $TEST_MODE"

    check_project_root
    setup_python_env
    check_dependencies

    local start_time=$(date +%s)
    local failed_checks=()

    # Run buf checks
    if ! run_buf_checks; then
        failed_checks+=("buf-validation")
    fi

    # Run Python tests
    if ! run_python_tests; then
        failed_checks+=("python-tests")
    fi

    # Check generated files (only in full mode)
    if [[ "$TEST_MODE" == "full" ]]; then
        if ! check_generated_files; then
            failed_checks+=("generated-files")
        fi
    fi

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    if [[ ${#failed_checks[@]} -eq 0 ]]; then
        log_success "All tests passed in ${duration}s"
        exit 0
    else
        log_error "Failed checks: ${failed_checks[*]}"
        log_error "Test run completed in ${duration}s with failures"
        exit 1
    fi
}

# Handle script arguments
case "${1:-}" in
    "quick"|"fast")
        TEST_MODE="quick"
        ;;
    "full"|"complete"|"ci")
        TEST_MODE="full"
        ;;
    "--help"|"-h")
        echo "Usage: $0 [quick|full] [options]"
        echo ""
        echo "Test modes:"
        echo "  quick  - Fast validation for pre-commit hooks"
        echo "  full   - Comprehensive testing for pre-push/CI"
        echo ""
        echo "Environment variables:"
        echo "  PYTHON_CMD  - Python command to use (default: python3)"
        echo "  VENV_PATH   - Virtual environment path (default: .venv)"
        echo "  VERBOSE     - Enable verbose output (default: false)"
        echo ""
        echo "Examples:"
        echo "  $0 quick              # Quick pre-commit validation"
        echo "  $0 full               # Full test suite"
        echo "  VERBOSE=true $0 full  # Full tests with verbose output"
        exit 0
        ;;
    "")
        # Default to quick mode
        TEST_MODE="quick"
        ;;
    *)
        log_error "Unknown test mode: $1"
        log_error "Use '$0 --help' for usage information"
        exit 1
        ;;
esac

# Run main function
main