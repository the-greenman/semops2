# SemOps2 Developer Guide

This guide provides a practical overview of the development workflows for `semops2`. It is designed for both human and AI developers contributing to the system.

## Core Architectural Principles

Before you begin, be familiar with the core principles defined in `IDL_ARCHITECTURE.md` and `INTERFACE_CONTRACT.md`:

1.  **Protobuf-First Service Definition**: Service contracts are the source of truth.
2.  **Configuration-Driven**: Entities and workflows are defined in YAML, not code.
3.  **Generic Service Layer**: A single set of services handles all entity types.
4.  **Decoupled Configuration**: The tool is separate from the knowledge bases it manages.

## Onboarding & Setup

1.  **Install Dependencies**: Install Python dependencies from `requirements.txt`.
2.  **Install Protobuf Compiler**: Install `protoc` and the `buf` CLI for code generation.
3.  **Install Git Hooks**: Run `pre-commit install` to set up the pre-commit hooks.
4.  **Run Tests**: Execute `pytest` in the root directory to ensure the system is working correctly.

## CI/CD and Git Hooks

To automate the enforcement of our architectural principles, the project uses a combination of pre-commit hooks and CI/CD actions.

### Pre-Commit Hooks

These run automatically on every `git commit` to catch errors locally before they are ever pushed.

-   **Formatting**: Runs `black` and `isort` to ensure consistent code style.
-   **Linting**: Runs `flake8` or a similar linter to catch common Python errors.
-   **Protobuf Checks**: Ensures that if a `.proto` file was changed, the corresponding generated code is also up-to-date.

### CI/CD Actions (e.g., on GitHub Actions)

These run automatically when a pull request is opened to protect the main branch.

-   **Run All Tests**: Executes the full `pytest` suite.
-   **Static Analysis**: Performs a static check to verify that all service classes correctly implement their Protobuf-generated abstract base classes.
-   **Breaking Change Detection**: Runs `buf breaking --against main` to detect and fail the build if a change to a `.proto` file is not backwards-compatible.

## Common Development Workflows

### Workflow 1: Modifying a Core Service

This workflow enforces the "Protobuf-first" principle.

1.  **Define the Change**: Open `schema/v1/services.proto` and add or modify the method in the appropriate service definition (e.g., add a `delete_entity` method to `EntityService`).
2.  **Generate Code**: Run the code generation script (e.g., `make generate`). This will update the abstract base class in `src/core/interfaces/` (e.g., `EntityServiceABC`).
3.  **Implement the Interface**: Your IDE will now likely show an error in the concrete service class (e.g., `src/core/entity_service.py`) because it does not implement the new abstract method. Implement the required logic.
4.  **Write Tests**: Add unit tests for the new method in the corresponding `tests/` file, mocking any dependencies.
5.  **Update BDD Scenarios**: If this is a user-facing change, add a new scenario to `docs/ENTITY_CONFIGURATION.md` to describe the behavior.

### Workflow 2: Adding a New Entity Type

This workflow is purely configuration-based and requires no changes to the `semops2` source code.

1.  **Navigate to Your Knowledge Base**: Go to the root of your knowledge base project (the directory with the `.semops-project` file).
2.  **Configure the Entity**: Open `.semops/config/entity_types.yaml` and add a new entry for your entity (e.g., `decision`). Define its ID prefix, parent, directory structure, and other properties.
3.  **Create the Template**: Create a new Jinja2 template for your entity in `.semops/templates/` (e.g., `decision.md.j2`).
4.  **Use the New Entity**: Run `semops` again. The new commands (e.g., `semops decision create`) will be automatically available.

### Workflow 3: Creating a New AI Workflow

This workflow is also purely configuration-based.

1.  **Navigate to Your Knowledge Base**: Go to the root of your knowledge base project.
2.  **Define Experts (Optional)**: If your workflow requires new AI personas, add them to `.semops/config/expert_types.yaml`.
3.  **Define the Workflow**: Open `.semops/config/workflows.yaml` and define your new workflow. Specify its name, applicable entity types, and the sequence of steps, including the expert, task, and any inputs for each step.
4.  **Execute the Workflow**: The new workflow is immediately available via the `analyze` command (e.g., `semops domain analyze --workflow <your-new-workflow>`).
