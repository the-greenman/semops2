"""Unit tests for entity package loading.

Tests loading complete entity packages including:
- entity_definition.yaml
- journey_definition.yaml
- experts.yaml
- template files
"""

import pytest
import yaml
from pathlib import Path


pytestmark = [pytest.mark.unit, pytest.mark.skip_until_phase0]


@pytest.mark.skip(reason="PackageLoader not yet implemented")
class TestEntityPackageLoading:
    """Test loading complete entity packages."""

    def test_load_entity_package_complete(self, temp_entity_packages_dir):
        """PackageLoader should load all components of an entity package.

        Given: Complete entity package with all YAML files
        When: PackageLoader loads the package
        Then: All components (entity def, journey, experts) are loaded
        """
        # Arrange
        from semops.core.config.package_loader import PackageLoader

        # Act
        loader = PackageLoader(temp_entity_packages_dir)
        packages = loader.load_all_packages()

        # Assert
        assert "domain" in packages
        domain_package = packages["domain"]

        assert "entity_definition" in domain_package
        assert "journey_definition" in domain_package
        assert "experts" in domain_package

        # Verify entity definition
        assert domain_package["entity_definition"]["entity_type"]["type_key"] == "domain"

        # Verify journey definition
        assert domain_package["journey_definition"]["entity_journey"]["journey_id"] == "domain-definition"

        # Verify experts
        assert "domain_architect" in domain_package["experts"]["expert_types"]

    def test_load_package_by_name(self, temp_entity_packages_dir):
        """PackageLoader should load a specific package by name.

        Given: Multiple entity packages available
        When: Loading a specific package by name
        Then: Only that package is loaded
        """
        # Arrange
        from semops.core.config.package_loader import PackageLoader

        loader = PackageLoader(temp_entity_packages_dir)

        # Act
        domain_package = loader.load_package("domain")

        # Assert
        assert domain_package is not None
        assert domain_package["entity_definition"]["entity_type"]["type_key"] == "domain"

    def test_missing_entity_definition_raises_error(self, temp_entity_packages_dir):
        """Package without entity_definition.yaml should raise ValidationError.

        Given: Package directory missing entity_definition.yaml
        When: PackageLoader tries to load it
        Then: ValidationError is raised
        """
        # Arrange
        incomplete_package_dir = temp_entity_packages_dir / "incomplete"
        incomplete_package_dir.mkdir()

        # Only create journey, no entity_definition
        journey_data = {
            "entity_journey": {
                "journey_id": "test-journey",
                "entity_type": "test/entity"
            }
        }
        with open(incomplete_package_dir / "journey_definition.yaml", "w") as f:
            yaml.dump(journey_data, f)

        from semops.core.config.package_loader import PackageLoader, ValidationError

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            loader = PackageLoader(temp_entity_packages_dir)
            loader.load_package("incomplete")

        assert "entity_definition.yaml" in str(exc_info.value)

    def test_package_with_only_entity_definition_allowed(self, temp_entity_packages_dir):
        """Package with only entity_definition.yaml should be valid.

        Given: Package with only entity_definition.yaml (no journey or experts)
        When: PackageLoader loads it
        Then: Package loads successfully with optional components as None
        """
        # Arrange
        minimal_package_dir = temp_entity_packages_dir / "minimal"
        minimal_package_dir.mkdir()

        entity_def = {
            "entity_type": {
                "type_key": "minimal",
                "namespace": "custom.ns",
                "id_prefix": "MIN",
                "display_name": "Minimal Entity"
            }
        }
        with open(minimal_package_dir / "entity_definition.yaml", "w") as f:
            yaml.dump(entity_def, f)

        from semops.core.config.package_loader import PackageLoader

        # Act
        loader = PackageLoader(temp_entity_packages_dir)
        minimal_package = loader.load_package("minimal")

        # Assert
        assert minimal_package["entity_definition"] is not None
        assert minimal_package.get("journey_definition") is None
        assert minimal_package.get("experts") is None


@pytest.mark.skip(reason="PackageLoader not yet implemented")
class TestExpertResolution:
    """Test expert resolution with package-first precedence."""

    def test_expert_resolution_package_first(self, temp_entity_packages_dir):
        """Expert resolution should check package-local experts first.

        Given: Package-local expert + core expert with same name
        When: Resolving expert for that package
        Then: Package-local expert takes precedence
        """
        # Arrange
        from semops.core.config.package_loader import PackageLoader

        loader = PackageLoader(temp_entity_packages_dir)
        domain_package = loader.load_package("domain")

        # Act
        # Resolve expert for domain entity type
        expert_def = loader.resolve_expert(
            entity_type="semops.core/domain",
            role="domain_architect"
        )

        # Assert
        assert expert_def is not None
        assert expert_def["name"] == "Domain Architect"
        assert expert_def["description"] == "Defines domain boundaries"

    def test_expert_resolution_core_fallback(self, temp_entity_packages_dir, temp_semops_project):
        """Expert resolution should fall back to core experts.

        Given: Package without local expert + core expert config
        When: Resolving expert not in package
        Then: Core expert is used
        """
        # Arrange
        # Add core expert to project config
        core_expert_config = temp_semops_project / ".semops" / "config" / "expert_types.yaml"
        expert_data = {
            "expert_types": {
                "strategic_analyst": {
                    "name": "Strategic Analyst",
                    "description": "Core strategic expert"
                }
            }
        }
        with open(core_expert_config, "w") as f:
            yaml.dump(expert_data, f)

        from semops.core.config.package_loader import PackageLoader

        loader = PackageLoader(temp_entity_packages_dir)

        # Act
        # Try to resolve expert not in domain package
        expert_def = loader.resolve_expert(
            entity_type="semops.core/domain",
            role="strategic_analyst",
            core_experts=expert_data["expert_types"]
        )

        # Assert
        assert expert_def is not None
        assert expert_def["name"] == "Strategic Analyst"

    def test_expert_resolution_not_found_returns_none(self, temp_entity_packages_dir):
        """Expert resolution should return None for unknown experts.

        Given: No matching expert in package or core
        When: Resolving unknown expert
        Then: None is returned (or NoExpertFound exception)
        """
        # Arrange
        from semops.core.config.package_loader import PackageLoader

        loader = PackageLoader(temp_entity_packages_dir)

        # Act
        expert_def = loader.resolve_expert(
            entity_type="semops.core/domain",
            role="nonexistent_expert",
            core_experts={}
        )

        # Assert
        assert expert_def is None


@pytest.mark.skip(reason="PackageLoader not yet implemented")
class TestJourneyValidation:
    """Test journey definition validation."""

    def test_journey_stage_validation(self, temp_entity_packages_dir):
        """Journey stages should be validated for required fields.

        Given: Journey with invalid stage definition
        When: PackageLoader validates it
        Then: ValidationError is raised
        """
        # Arrange
        invalid_journey_dir = temp_entity_packages_dir / "invalid_journey"
        invalid_journey_dir.mkdir()

        # Create entity definition
        entity_def = {
            "entity_type": {
                "type_key": "invalid",
                "namespace": "custom.ns",
                "id_prefix": "INV",
                "display_name": "Invalid"
            }
        }
        with open(invalid_journey_dir / "entity_definition.yaml", "w") as f:
            yaml.dump(entity_def, f)

        # Create invalid journey (stage missing required type field)
        invalid_journey = {
            "entity_journey": {
                "journey_id": "invalid-journey",
                "entity_type": "custom.ns/invalid",
                "stages": [
                    {
                        "name": "broken_stage"
                        # Missing required 'type' field
                    }
                ]
            }
        }
        with open(invalid_journey_dir / "journey_definition.yaml", "w") as f:
            yaml.dump(invalid_journey, f)

        from semops.core.config.package_loader import PackageLoader, ValidationError

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            loader = PackageLoader(temp_entity_packages_dir)
            loader.load_package("invalid_journey")

        assert "stage" in str(exc_info.value).lower()
        assert "type" in str(exc_info.value).lower()

    def test_journey_stage_types_validated(self, temp_entity_packages_dir):
        """Journey stage types should be one of allowed values.

        Given: Journey stage with invalid type
        When: PackageLoader validates it
        Then: ValidationError is raised
        """
        # Arrange
        invalid_stage_dir = temp_entity_packages_dir / "invalid_stage"
        invalid_stage_dir.mkdir()

        entity_def = {
            "entity_type": {
                "type_key": "invalid_stage",
                "namespace": "custom.ns",
                "id_prefix": "INS",
                "display_name": "Invalid Stage"
            }
        }
        with open(invalid_stage_dir / "entity_definition.yaml", "w") as f:
            yaml.dump(entity_def, f)

        invalid_journey = {
            "entity_journey": {
                "journey_id": "invalid-stage-journey",
                "entity_type": "custom.ns/invalid_stage",
                "stages": [
                    {
                        "name": "bad_stage",
                        "type": "invalid.stage.type"  # Not a valid stage type
                    }
                ]
            }
        }
        with open(invalid_stage_dir / "journey_definition.yaml", "w") as f:
            yaml.dump(invalid_journey, f)

        from semops.core.config.package_loader import PackageLoader, ValidationError

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            loader = PackageLoader(temp_entity_packages_dir)
            loader.load_package("invalid_stage")

        assert "stage type" in str(exc_info.value).lower()
        # Should mention allowed types: human.create, ai.assist, human.review, system.commit
        assert any(t in str(exc_info.value) for t in ["human.create", "ai.assist"])

    def test_journey_ai_assist_stage_requires_agent(self, temp_entity_packages_dir):
        """ai.assist stages must have agent configuration.

        Given: ai.assist stage without agent field
        When: PackageLoader validates it
        Then: ValidationError is raised
        """
        # Arrange
        missing_agent_dir = temp_entity_packages_dir / "missing_agent"
        missing_agent_dir.mkdir()

        entity_def = {
            "entity_type": {
                "type_key": "missing_agent",
                "namespace": "custom.ns",
                "id_prefix": "MIA",
                "display_name": "Missing Agent"
            }
        }
        with open(missing_agent_dir / "entity_definition.yaml", "w") as f:
            yaml.dump(entity_def, f)

        journey_missing_agent = {
            "entity_journey": {
                "journey_id": "missing-agent-journey",
                "entity_type": "custom.ns/missing_agent",
                "stages": [
                    {
                        "name": "ai_stage",
                        "type": "ai.assist"
                        # Missing required 'agent' field for ai.assist
                    }
                ]
            }
        }
        with open(missing_agent_dir / "journey_definition.yaml", "w") as f:
            yaml.dump(journey_missing_agent, f)

        from semops.core.config.package_loader import PackageLoader, ValidationError

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            loader = PackageLoader(temp_entity_packages_dir)
            loader.load_package("missing_agent")

        assert "agent" in str(exc_info.value).lower()
        assert "ai.assist" in str(exc_info.value)
