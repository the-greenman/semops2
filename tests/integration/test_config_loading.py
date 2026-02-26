"""Integration tests for end-to-end configuration loading.

Tests the full configuration loading pipeline including:
- Project root discovery
- Entity type loading
- Entity package loading
- Expert resolution
- Template discovery
"""

import pytest
import yaml
from pathlib import Path


pytestmark = [pytest.mark.integration, pytest.mark.skip_until_phase0]


@pytest.mark.skip(reason="ConfigManager integration not yet complete")
class TestConfigurationLoadingIntegration:
    """Test end-to-end configuration loading."""

    def test_load_config_with_entity_packages(self, temp_entity_packages_dir, temp_semops_project):
        """Full config loading should integrate all components.

        Given: Complete .semops/ project with entity packages
        When: ConfigManager loads configuration
        Then: All config, entity types, packages, and experts are available
        """
        # Arrange
        from semops.core.config import ConfigManager

        # Act
        config = ConfigManager(working_dir=temp_semops_project)

        # Assert
        # Entity types from config
        assert "semops.core/domain" in config.entity_types

        # Entity packages loaded
        assert "domain" in config.entity_packages
        domain_package = config.entity_packages["domain"]

        assert domain_package["entity_definition"] is not None
        assert domain_package["journey_definition"] is not None
        assert domain_package["experts"] is not None

        # Experts available
        assert "domain_architect" in domain_package["experts"]["expert_types"]

    def test_expert_resolution_with_fallback(self, temp_entity_packages_dir, temp_semops_project):
        """Expert resolution should check package-local then core.

        Given: Package-local expert + core expert
        When: Resolving expert
        Then: Package-local takes precedence, core is fallback
        """
        # Arrange
        # Add core expert to project config
        core_expert_config = temp_semops_project / ".semops" / "config" / "expert_types.yaml"
        with open(core_expert_config, "r") as f:
            expert_data = yaml.safe_load(f)

        expert_data["expert_types"]["generic_analyst"] = {
            "name": "Generic Analyst",
            "description": "Core generic expert"
        }

        with open(core_expert_config, "w") as f:
            yaml.dump(expert_data, f)

        from semops.core.config import ConfigManager

        # Act
        config = ConfigManager(working_dir=temp_semops_project)

        # Package-local expert resolution
        domain_expert = config.resolve_expert(
            entity_type="semops.core/domain",
            role="domain_architect"
        )

        # Core expert fallback
        generic_expert = config.resolve_expert(
            entity_type="semops.core/domain",
            role="generic_analyst"
        )

        # Assert
        # Package-local expert resolved
        assert domain_expert is not None
        assert domain_expert["name"] == "Domain Architect"
        assert domain_expert["_resolution_source"] == "package"

        # Core expert used as fallback
        assert generic_expert is not None
        assert generic_expert["name"] == "Generic Analyst"
        assert generic_expert["_resolution_source"] == "core"

    def test_template_discovery_override(self, temp_semops_project):
        """Project templates should override builtin templates.

        Given: Builtin template + project template with same name
        When: Loading templates
        Then: Project template takes precedence
        """
        # Arrange
        from semops.core.config import ConfigManager

        # Add a custom template that overrides builtin
        templates_dir = temp_semops_project / ".semops" / "templates"
        with open(templates_dir / "domain.md.j2", "w") as f:
            f.write("""---
# Custom project template
---

# CUSTOM: {{ domain_name }}

{{ purpose }}
""")

        # Act
        config = ConfigManager(working_dir=temp_semops_project)
        template_content = config.get_template("domain.md.j2")

        # Assert
        assert "CUSTOM:" in template_content
        assert template_content.startswith("---\n# Custom project template")

    def test_config_layering_with_overrides(self, temp_semops_project):
        """Project config should override builtin defaults.

        Given: Builtin entity types + project overrides
        When: Loading config
        Then: Project overrides take effect
        """
        # Arrange
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"

        with open(config_file, "r") as f:
            data = yaml.safe_load(f)

        # Override display name and add custom field
        data["entity_types"]["semops.core/domain"]["display_name"] = "Custom Domain"
        data["entity_types"]["semops.core/domain"]["custom_field"] = "custom_value"

        with open(config_file, "w") as f:
            yaml.dump(data, f)

        from semops.core.config import ConfigManager

        # Act
        config = ConfigManager(working_dir=temp_semops_project)
        domain_type = config.get_entity_type("semops.core/domain")

        # Assert
        assert domain_type["display_name"] == "Custom Domain"
        assert domain_type["custom_field"] == "custom_value"


@pytest.mark.skip(reason="ConfigManager integration not yet complete")
class TestConfigurationValidationIntegration:
    """Test validation across multiple config components."""

    def test_entity_package_entity_type_consistency(self, temp_entity_packages_dir, temp_semops_project):
        """Entity package entity_type should match registered entity type.

        Given: Entity package referencing entity type
        When: Loading package
        Then: Entity type must be registered in config
        """
        # Arrange
        # Create package referencing non-existent entity type
        invalid_package_dir = temp_entity_packages_dir / "invalid"
        invalid_package_dir.mkdir()

        entity_def = {
            "entity_type": {
                "type_key": "nonexistent",
                "namespace": "unknown.ns",
                "id_prefix": "UNK",
                "display_name": "Nonexistent"
            }
        }
        with open(invalid_package_dir / "entity_definition.yaml", "w") as f:
            yaml.dump(entity_def, f)

        from semops.core.config import ConfigManager, ValidationError

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ConfigManager(working_dir=temp_semops_project)

        assert "unknown.ns/nonexistent" in str(exc_info.value)
        assert "not registered" in str(exc_info.value).lower()

    def test_journey_expert_references_validated(self, temp_entity_packages_dir):
        """Journey stages referencing experts should be validated.

        Given: Journey with ai.assist stage referencing expert
        When: Loading journey
        Then: Expert must exist in package or core
        """
        # Arrange
        domain_dir = temp_entity_packages_dir / "domain"

        # Load existing journey
        journey_file = domain_dir / "journey_definition.yaml"
        with open(journey_file, "r") as f:
            journey_data = yaml.safe_load(f)

        # Add stage referencing non-existent expert
        journey_data["entity_journey"]["stages"].append({
            "name": "invalid_stage",
            "type": "ai.assist",
            "agent": {
                "role": "nonexistent_expert",
                "model": "claude-3-5-sonnet"
            }
        })

        with open(journey_file, "w") as f:
            yaml.dump(journey_data, f)

        from semops.core.config import ConfigManager, ValidationError

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            config = ConfigManager(working_dir=temp_entity_packages_dir.parent)
            config.validate_journey("domain")

        assert "nonexistent_expert" in str(exc_info.value)
        assert "not found" in str(exc_info.value).lower()

    def test_id_prefix_collisions_detected(self, temp_semops_project):
        """ID prefix collisions across packages should be detected.

        Given: Two entity types with same ID prefix
        When: Loading configuration
        Then: ValidationError is raised
        """
        # Arrange
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"

        collision_data = {
            "entity_types": {
                "custom.ns/entity1": {
                    "type_key": "entity1",
                    "namespace": "custom.ns",
                    "id_prefix": "ENT",
                    "display_name": "Entity 1"
                },
                "custom.ns/entity2": {
                    "type_key": "entity2",
                    "namespace": "custom.ns",
                    "id_prefix": "ENT",  # Collision!
                    "display_name": "Entity 2"
                }
            }
        }

        with open(config_file, "w") as f:
            yaml.dump(collision_data, f)

        from semops.core.config import ConfigManager, ValidationError

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ConfigManager(working_dir=temp_semops_project)

        assert "ENT" in str(exc_info.value)
        assert "duplicate" in str(exc_info.value).lower()


@pytest.mark.skip(reason="ConfigManager integration not yet complete")
class TestConfigurationCaching:
    """Test configuration caching and reloading."""

    def test_config_is_cached(self, temp_semops_project):
        """Configuration should be cached after first load.

        Given: Loaded configuration
        When: Accessing config multiple times
        Then: Config is not reloaded from disk
        """
        # Arrange
        from semops.core.config import ConfigManager

        config = ConfigManager(working_dir=temp_semops_project)

        # Modify config file after loading
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"
        with open(config_file, "r") as f:
            data = yaml.safe_load(f)

        data["entity_types"]["semops.core/domain"]["display_name"] = "Modified"

        with open(config_file, "w") as f:
            yaml.dump(data, f)

        # Act
        # Access config again (should use cache)
        domain_type = config.get_entity_type("semops.core/domain")

        # Assert
        # Should still have old value from cache
        assert domain_type["display_name"] != "Modified"

    def test_config_reload_on_demand(self, temp_semops_project):
        """Configuration should support manual reload.

        Given: Loaded configuration
        When: Calling reload()
        Then: Configuration is reloaded from disk
        """
        # Arrange
        from semops.core.config import ConfigManager

        config = ConfigManager(working_dir=temp_semops_project)

        # Modify config file
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"
        with open(config_file, "r") as f:
            data = yaml.safe_load(f)

        data["entity_types"]["semops.core/domain"]["display_name"] = "Reloaded"

        with open(config_file, "w") as f:
            yaml.dump(data, f)

        # Act
        config.reload()
        domain_type = config.get_entity_type("semops.core/domain")

        # Assert
        assert domain_type["display_name"] == "Reloaded"
