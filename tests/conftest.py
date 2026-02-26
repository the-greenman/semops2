"""Shared test fixtures for SemOps2 test suite.

This module provides reusable fixtures for all test layers:
- Temporary project structures
- Mock services and adapters
- Sample data and entity packages
- Test configuration
"""

import tempfile
from pathlib import Path
from typing import Dict, Any
import pytest
import yaml


# =============================================================================
# Test Project Structure Fixtures
# =============================================================================

@pytest.fixture
def temp_dir():
    """Create a temporary directory that gets cleaned up after the test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_semops_project(temp_dir):
    """Create a complete temporary .semops/ project structure.

    Structure:
        .semops-project (marker file)
        .semops/
            config/
                entity_types.yaml
                expert_types.yaml
                source_types.yaml
                workflows.yaml
                rag_workflows.yaml
                storage_backends.yaml
            templates/
                domain.md.j2

    Returns:
        Path: Root directory of the temporary project
    """
    # Create marker file
    (temp_dir / ".semops-project").touch()

    # Create config directory
    config_dir = temp_dir / ".semops" / "config"
    config_dir.mkdir(parents=True)

    # Create templates directory
    templates_dir = temp_dir / ".semops" / "templates"
    templates_dir.mkdir(parents=True)

    # Create basic entity_types.yaml
    entity_types = {
        "entity_types": {
            "semops.core/domain": {
                "type_key": "domain",
                "namespace": "semops.core",
                "id_prefix": "DOM",
                "display_name": "Domain",
                "template_bundle": {
                    "create": "domain.md.j2"
                },
                "required_fields": ["domain_name", "purpose"]
            }
        }
    }
    with open(config_dir / "entity_types.yaml", "w") as f:
        yaml.dump(entity_types, f)

    # Create basic expert_types.yaml
    expert_types = {
        "expert_types": {
            "strategic_analyst": {
                "name": "Strategic Analyst",
                "description": "Strategic business analysis expert"
            }
        }
    }
    with open(config_dir / "expert_types.yaml", "w") as f:
        yaml.dump(expert_types, f)

    # Create basic template
    template_content = """---
entity_type: domain
entity_id: {{ entity_id }}
created_at: {{ created_at }}
created_by_actor_id: {{ created_by_actor_id }}
---

# {{ domain_name }}

## Purpose
{{ purpose }}
"""
    with open(templates_dir / "domain.md.j2", "w") as f:
        f.write(template_content)

    return temp_dir


@pytest.fixture
def temp_entity_packages_dir(temp_semops_project):
    """Create entity_packages directory with sample domain package.

    Returns:
        Path: entity_packages directory
    """
    packages_dir = temp_semops_project / "entity_packages"
    domain_dir = packages_dir / "domain"
    domain_dir.mkdir(parents=True)

    # Create entity_definition.yaml
    entity_def = {
        "entity_type": {
            "type_key": "domain",
            "namespace": "semops.core",
            "id_prefix": "DOM",
            "name_field": "domain_name",
            "slug_field": "domain_slug",
            "display_name": "Domain",
            "template_bundle": {
                "create": "create.md.j2",
                "analyze": "analyze.md.j2"
            },
            "template_version": "1.0.0",
            "required_fields": ["domain_name", "purpose"]
        }
    }
    with open(domain_dir / "entity_definition.yaml", "w") as f:
        yaml.dump(entity_def, f)

    # Create experts.yaml
    experts = {
        "expert_types": {
            "domain_architect": {
                "name": "Domain Architect",
                "description": "Defines domain boundaries",
                "persona": {"role": "Organizational architect"},
                "expertise": ["scope_definition", "boundary_setting"]
            }
        }
    }
    with open(domain_dir / "experts.yaml", "w") as f:
        yaml.dump(experts, f)

    # Create journey_definition.yaml (simplified)
    journey = {
        "entity_journey": {
            "journey_id": "domain-definition",
            "entity_type": "semops.core/domain",
            "journey_type": "creation_refinement",
            "stages": [
                {
                    "name": "draft_creation",
                    "type": "human.create",
                    "required_fields": ["domain_name"]
                },
                {
                    "name": "scope_clarification",
                    "type": "ai.assist",
                    "agent": {
                        "role": "domain_architect",
                        "model": "claude-3-5-sonnet"
                    }
                }
            ]
        }
    }
    with open(domain_dir / "journey_definition.yaml", "w") as f:
        yaml.dump(journey, f)

    return packages_dir


# =============================================================================
# Sample Data Fixtures
# =============================================================================

@pytest.fixture
def sample_entity_data() -> Dict[str, Any]:
    """Sample entity data for testing."""
    return {
        "domain_name": "User Authentication",
        "purpose": "Manage user identity and access control",
        "scope_included": ["Login", "Registration", "Password reset"],
        "scope_excluded": ["Authorization policies"],
        "authority_level": "engineering",
        "created_by_actor_id": "ACT-human-test-user"
    }


@pytest.fixture
def sample_entity_id() -> str:
    """Sample entity ID for testing."""
    return "DOM-001-user-authentication"


# =============================================================================
# Mock Service Fixtures
# =============================================================================

@pytest.fixture
def mock_llm_client():
    """Mock LLM client with canned responses.

    Returns a mock that implements the LLMStructuredClient interface.
    """
    class MockLLMClient:
        def __init__(self):
            self.call_count = 0
            self.canned_responses = []

        def generate(self, prompt: str, schema: Any, **kwargs) -> Dict[str, Any]:
            """Generate a canned response."""
            self.call_count += 1

            if self.canned_responses:
                return self.canned_responses.pop(0)

            # Default canned response
            return {
                "content": "Generated analysis",
                "metadata": {
                    "schema_validated": True,
                    "prompt_version": "1.0.0",
                    "trace_id": f"trace-{self.call_count}"
                }
            }

        def add_canned_response(self, response: Dict[str, Any]):
            """Add a canned response to the queue."""
            self.canned_responses.append(response)

    return MockLLMClient()


@pytest.fixture
def mock_vector_store():
    """Mock vector store adapter.

    Returns a mock that implements the VectorStoreAdapter interface.
    """
    class MockVectorStore:
        def __init__(self):
            self.documents = []

        def ingest(self, documents: list):
            """Store documents."""
            self.documents.extend(documents)

        def search(self, query: str, k: int = 5):
            """Return mock search results."""
            return [
                {"id": f"doc-{i}", "content": f"Result {i}", "score": 0.9 - i * 0.1}
                for i in range(min(k, len(self.documents)))
            ]

        def filter(self, metadata_filter: Dict[str, Any]):
            """Return filtered documents."""
            return [doc for doc in self.documents if self._matches_filter(doc, metadata_filter)]

        @staticmethod
        def _matches_filter(doc: Dict, filter_dict: Dict) -> bool:
            """Simple filter matching."""
            return all(doc.get(k) == v for k, v in filter_dict.items())

    return MockVectorStore()


# =============================================================================
# Test Markers and Skip Helpers
# =============================================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "skip_until_implemented: mark test to skip until feature is implemented"
    )
