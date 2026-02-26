"""Unit tests for ConfigManager.

Tests the core configuration discovery and loading logic.
All tests start skipped with @pytest.mark.skip_until_phase0 and should be
unskipped as the ConfigManager implementation progresses.
"""

import pytest
from pathlib import Path


pytestmark = [pytest.mark.unit, pytest.mark.skip_until_phase0]


@pytest.mark.skip(reason="ConfigManager not yet implemented")
class TestProjectRootDiscovery:
    """Test project root discovery logic."""

    def test_discover_project_root_from_semops_marker(self, temp_dir):
        """ConfigManager should find project root from .semops-project marker file.

        Given: A directory with .semops-project marker file
        When: ConfigManager searches for project root
        Then: It returns the directory containing the marker
        """
        # Arrange
        marker_file = temp_dir / ".semops-project"
        marker_file.touch()

        nested_dir = temp_dir / "subdir" / "nested"
        nested_dir.mkdir(parents=True)

        # Act
        from semops.core.config import ConfigManager
        config = ConfigManager(working_dir=nested_dir)

        # Assert
        assert config.project_root == temp_dir
        assert config.project_root.is_dir()

    def test_discover_project_root_from_semops_dir(self, temp_dir):
        """ConfigManager should find project root from .semops/ directory.

        Given: A directory with .semops/ directory but no marker file
        When: ConfigManager searches for project root
        Then: It returns the directory containing .semops/
        """
        # Arrange
        semops_dir = temp_dir / ".semops"
        semops_dir.mkdir()

        nested_dir = temp_dir / "subdir"
        nested_dir.mkdir()

        # Act
        from semops.core.config import ConfigManager
        config = ConfigManager(working_dir=nested_dir)

        # Assert
        assert config.project_root == temp_dir

    def test_discover_project_root_from_git_root(self, temp_dir):
        """ConfigManager should fall back to git root if .semops/ exists there.

        Given: A git repository with .semops/ at the root
        When: ConfigManager searches from a subdirectory
        Then: It returns the git root
        """
        # Arrange
        # Initialize git repo
        import subprocess
        subprocess.run(["git", "init"], cwd=temp_dir, check=True, capture_output=True)

        semops_dir = temp_dir / ".semops"
        semops_dir.mkdir()

        nested_dir = temp_dir / "src" / "nested"
        nested_dir.mkdir(parents=True)

        # Act
        from semops.core.config import ConfigManager
        config = ConfigManager(working_dir=nested_dir)

        # Assert
        assert config.project_root == temp_dir

    def test_no_project_root_raises_clear_error(self, temp_dir):
        """ConfigManager should raise a clear error when no project root is found.

        Given: A directory with no .semops-project, .semops/, or git repo
        When: ConfigManager tries to initialize
        Then: It raises ConfigurationError with helpful message
        """
        # Arrange
        isolated_dir = temp_dir / "isolated"
        isolated_dir.mkdir()

        # Act & Assert
        from semops.core.config import ConfigManager, ConfigurationError

        with pytest.raises(ConfigurationError) as exc_info:
            ConfigManager(working_dir=isolated_dir)

        assert "No SemOps project root found" in str(exc_info.value)
        assert ".semops-project" in str(exc_info.value)


@pytest.mark.skip(reason="ConfigManager not yet implemented")
class TestLayeredConfigLoading:
    """Test layered configuration loading (builtin → project → explicit)."""

    def test_layered_loading_builtin_then_project(self, temp_semops_project):
        """ConfigManager should merge builtin and project configs.

        Given: Builtin config with core entities + project config with custom entity
        When: ConfigManager loads configuration
        Then: Both builtin and project entities are available
        """
        # Arrange
        from semops.core.config import ConfigManager

        # Act
        config = ConfigManager(working_dir=temp_semops_project)

        # Assert
        # Should have builtin core entities
        assert "semops.core/domain" in config.entity_types
        assert "semops.core/meeting" in config.entity_types

        # Should also have project-specific config
        entity_type = config.get_entity_type("semops.core/domain")
        assert entity_type is not None
        assert entity_type["id_prefix"] == "DOM"

    def test_project_config_overrides_builtin(self, temp_semops_project):
        """Project config should override builtin config for same entity type.

        Given: Builtin config with domain entity + project config overriding it
        When: ConfigManager loads configuration
        Then: Project config takes precedence
        """
        # Arrange
        # Modify project config to override a builtin entity
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"

        import yaml
        with open(config_file, "r") as f:
            data = yaml.safe_load(f)

        data["entity_types"]["semops.core/domain"]["display_name"] = "Custom Domain"

        with open(config_file, "w") as f:
            yaml.dump(data, f)

        from semops.core.config import ConfigManager

        # Act
        config = ConfigManager(working_dir=temp_semops_project)

        # Assert
        entity_type = config.get_entity_type("semops.core/domain")
        assert entity_type["display_name"] == "Custom Domain"

    def test_explicit_config_path_override(self, temp_dir, temp_semops_project):
        """Explicit --config-path should take highest precedence.

        Given: Project config + separate explicit config directory
        When: ConfigManager initialized with explicit config_path
        Then: Explicit config takes precedence over project config
        """
        # Arrange
        explicit_config_dir = temp_dir / "custom_config"
        explicit_config_dir.mkdir()

        import yaml
        explicit_entity_types = {
            "entity_types": {
                "custom.namespace/entity": {
                    "type_key": "custom",
                    "namespace": "custom.namespace",
                    "id_prefix": "CUST"
                }
            }
        }
        with open(explicit_config_dir / "entity_types.yaml", "w") as f:
            yaml.dump(explicit_entity_types, f)

        from semops.core.config import ConfigManager

        # Act
        config = ConfigManager(
            working_dir=temp_semops_project,
            explicit_config_path=explicit_config_dir
        )

        # Assert
        assert "custom.namespace/entity" in config.entity_types


@pytest.mark.skip(reason="ConfigManager not yet implemented")
class TestNamespaceValidation:
    """Test namespace validation and reserved namespace rules."""

    def test_namespace_validation_semops_core_reserved(self, temp_semops_project):
        """semops.* namespace should be reserved for builtin entities.

        Given: Project config trying to define entity in semops.core namespace
        When: ConfigManager validates configuration
        Then: It raises ValidationError for reserved namespace
        """
        # Arrange
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"

        import yaml
        with open(config_file, "r") as f:
            data = yaml.safe_load(f)

        # Try to add an entity in reserved namespace
        data["entity_types"]["semops.core/custom"] = {
            "type_key": "custom",
            "namespace": "semops.core",
            "id_prefix": "CUST"
        }

        with open(config_file, "w") as f:
            yaml.dump(data, f)

        from semops.core.config import ConfigManager, ValidationError

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ConfigManager(working_dir=temp_semops_project)

        assert "reserved namespace" in str(exc_info.value).lower()
        assert "semops." in str(exc_info.value)

    def test_custom_namespace_allowed(self, temp_semops_project):
        """Custom namespaces (non-semops.*) should be allowed.

        Given: Project config with custom namespace
        When: ConfigManager loads configuration
        Then: Custom namespace entity is loaded successfully
        """
        # Arrange
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"

        import yaml
        with open(config_file, "r") as f:
            data = yaml.safe_load(f)

        data["entity_types"]["myorg.team/custom"] = {
            "type_key": "custom",
            "namespace": "myorg.team",
            "id_prefix": "CUST"
        }

        with open(config_file, "w") as f:
            yaml.dump(data, f)

        from semops.core.config import ConfigManager

        # Act
        config = ConfigManager(working_dir=temp_semops_project)

        # Assert
        assert "myorg.team/custom" in config.entity_types


@pytest.mark.skip(reason="ConfigManager not yet implemented")
class TestConfigErrorHandling:
    """Test error handling for invalid configuration."""

    def test_invalid_config_path_raises_clear_error(self, temp_dir):
        """ConfigManager should raise clear error for invalid config path.

        Given: Explicit config path that doesn't exist
        When: ConfigManager tries to initialize
        Then: It raises ConfigurationError with helpful message
        """
        # Arrange
        from semops.core.config import ConfigManager, ConfigurationError

        non_existent_path = temp_dir / "does_not_exist"

        # Act & Assert
        with pytest.raises(ConfigurationError) as exc_info:
            ConfigManager(explicit_config_path=non_existent_path)

        assert "does not exist" in str(exc_info.value).lower()
        assert str(non_existent_path) in str(exc_info.value)

    def test_malformed_yaml_raises_clear_error(self, temp_semops_project):
        """ConfigManager should raise clear error for malformed YAML.

        Given: Config file with invalid YAML syntax
        When: ConfigManager tries to load it
        Then: It raises ConfigurationError with file path and error
        """
        # Arrange
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"

        with open(config_file, "w") as f:
            f.write("invalid: yaml: syntax:\n  - broken")

        from semops.core.config import ConfigManager, ConfigurationError

        # Act & Assert
        with pytest.raises(ConfigurationError) as exc_info:
            ConfigManager(working_dir=temp_semops_project)

        assert "entity_types.yaml" in str(exc_info.value)

    def test_missing_required_field_raises_clear_error(self, temp_semops_project):
        """ConfigManager should validate required fields in entity types.

        Given: Entity type definition missing required field (e.g., id_prefix)
        When: ConfigManager validates configuration
        Then: It raises ValidationError specifying the missing field
        """
        # Arrange
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"

        import yaml
        invalid_entity_types = {
            "entity_types": {
                "custom.ns/incomplete": {
                    "type_key": "incomplete",
                    "namespace": "custom.ns"
                    # Missing required id_prefix
                }
            }
        }
        with open(config_file, "w") as f:
            yaml.dump(invalid_entity_types, f)

        from semops.core.config import ConfigManager, ValidationError

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ConfigManager(working_dir=temp_semops_project)

        assert "id_prefix" in str(exc_info.value).lower()
        assert "custom.ns/incomplete" in str(exc_info.value)
