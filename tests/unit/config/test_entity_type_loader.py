"""Unit tests for entity type loading and validation.

Tests the logic for loading entity type definitions from YAML files
and validating their structure.
"""

import pytest
from pathlib import Path
import yaml


pytestmark = [pytest.mark.unit, pytest.mark.skip_until_phase0]


@pytest.mark.skip(reason="EntityTypeLoader not yet implemented")
class TestEntityTypeLoading:
    """Test loading entity type definitions from YAML."""

    def test_load_entity_definition_from_yaml(self, temp_semops_project):
        """EntityTypeLoader should parse entity type YAML correctly.

        Given: Valid entity_types.yaml file
        When: EntityTypeLoader loads the file
        Then: Entity type definition is parsed with all fields
        """
        # Arrange
        from semops.core.config.entity_type_loader import EntityTypeLoader

        config_path = temp_semops_project / ".semops" / "config"

        # Act
        loader = EntityTypeLoader(config_path)
        entity_types = loader.load_entity_types()

        # Assert
        assert "semops.core/domain" in entity_types
        domain_type = entity_types["semops.core/domain"]

        assert domain_type["type_key"] == "domain"
        assert domain_type["namespace"] == "semops.core"
        assert domain_type["id_prefix"] == "DOM"
        assert domain_type["display_name"] == "Domain"
        assert "required_fields" in domain_type

    def test_entity_type_with_namespace_prefix(self, temp_semops_project):
        """Entity type key should be namespace/type_key format.

        Given: Entity with namespace="myorg" and type_key="custom"
        When: EntityTypeLoader processes it
        Then: Entity key is "myorg/custom"
        """
        # Arrange
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"

        entity_data = {
            "entity_types": {
                "myorg.project/custom": {
                    "type_key": "custom",
                    "namespace": "myorg.project",
                    "id_prefix": "CUST",
                    "display_name": "Custom Entity"
                }
            }
        }
        with open(config_file, "w") as f:
            yaml.dump(entity_data, f)

        from semops.core.config.entity_type_loader import EntityTypeLoader

        # Act
        loader = EntityTypeLoader(temp_semops_project / ".semops" / "config")
        entity_types = loader.load_entity_types()

        # Assert
        assert "myorg.project/custom" in entity_types
        custom_type = entity_types["myorg.project/custom"]
        assert custom_type["namespace"] == "myorg.project"
        assert custom_type["type_key"] == "custom"

    def test_template_bundle_path_resolution(self, temp_semops_project):
        """Template paths should be resolved relative to template directory.

        Given: Entity type with template_bundle paths
        When: EntityTypeLoader processes it
        Then: Template paths are resolved correctly
        """
        # Arrange
        from semops.core.config.entity_type_loader import EntityTypeLoader

        config_path = temp_semops_project / ".semops" / "config"

        # Act
        loader = EntityTypeLoader(config_path)
        entity_types = loader.load_entity_types()

        # Assert
        domain_type = entity_types["semops.core/domain"]
        assert "template_bundle" in domain_type
        assert domain_type["template_bundle"]["create"] == "domain.md.j2"


@pytest.mark.skip(reason="EntityTypeLoader not yet implemented")
class TestEntityTypeValidation:
    """Test validation of entity type definitions."""

    def test_required_fields_validation(self, temp_semops_project):
        """Entity type must have required fields: type_key, namespace, id_prefix.

        Given: Entity type missing required field
        When: EntityTypeLoader validates it
        Then: ValidationError is raised
        """
        # Arrange
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"

        invalid_data = {
            "entity_types": {
                "custom.ns/invalid": {
                    "type_key": "invalid",
                    "namespace": "custom.ns"
                    # Missing id_prefix
                }
            }
        }
        with open(config_file, "w") as f:
            yaml.dump(invalid_data, f)

        from semops.core.config.entity_type_loader import EntityTypeLoader, ValidationError

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            loader = EntityTypeLoader(temp_semops_project / ".semops" / "config")
            loader.load_entity_types()

        assert "id_prefix" in str(exc_info.value).lower()

    def test_id_prefix_uniqueness_check(self, temp_semops_project):
        """ID prefixes must be unique across all entity types.

        Given: Two entity types with the same id_prefix
        When: EntityTypeLoader validates them
        Then: ValidationError is raised
        """
        # Arrange
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"

        duplicate_prefix_data = {
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
                    "id_prefix": "ENT",  # Duplicate!
                    "display_name": "Entity 2"
                }
            }
        }
        with open(config_file, "w") as f:
            yaml.dump(duplicate_prefix_data, f)

        from semops.core.config.entity_type_loader import EntityTypeLoader, ValidationError

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            loader = EntityTypeLoader(temp_semops_project / ".semops" / "config")
            loader.load_entity_types()

        assert "duplicate" in str(exc_info.value).lower()
        assert "ENT" in str(exc_info.value)

    def test_id_prefix_format_validation(self, temp_semops_project):
        """ID prefix should be uppercase alphanumeric, 2-4 characters.

        Given: Entity type with invalid id_prefix format
        When: EntityTypeLoader validates it
        Then: ValidationError is raised
        """
        # Arrange
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"

        invalid_prefix_data = {
            "entity_types": {
                "custom.ns/invalid": {
                    "type_key": "invalid",
                    "namespace": "custom.ns",
                    "id_prefix": "toolong123",  # Too long
                    "display_name": "Invalid"
                }
            }
        }
        with open(config_file, "w") as f:
            yaml.dump(invalid_prefix_data, f)

        from semops.core.config.entity_type_loader import EntityTypeLoader, ValidationError

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            loader = EntityTypeLoader(temp_semops_project / ".semops" / "config")
            loader.load_entity_types()

        assert "id_prefix" in str(exc_info.value).lower()

    def test_namespace_format_validation(self, temp_semops_project):
        """Namespace should follow format: lowercase.dotted.notation.

        Given: Entity type with invalid namespace format
        When: EntityTypeLoader validates it
        Then: ValidationError is raised
        """
        # Arrange
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"

        invalid_namespace_data = {
            "entity_types": {
                "Invalid-Namespace/entity": {
                    "type_key": "entity",
                    "namespace": "Invalid-Namespace",  # Invalid format
                    "id_prefix": "ENT",
                    "display_name": "Entity"
                }
            }
        }
        with open(config_file, "w") as f:
            yaml.dump(invalid_namespace_data, f)

        from semops.core.config.entity_type_loader import EntityTypeLoader, ValidationError

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            loader = EntityTypeLoader(temp_semops_project / ".semops" / "config")
            loader.load_entity_types()

        assert "namespace" in str(exc_info.value).lower()


@pytest.mark.skip(reason="EntityTypeLoader not yet implemented")
class TestEntityTypeRegistry:
    """Test entity type registry and lookup functionality."""

    def test_get_entity_type_by_key(self, temp_semops_project):
        """Registry should support lookup by full key (namespace/type_key).

        Given: Loaded entity types
        When: Looking up by full key
        Then: Entity type definition is returned
        """
        # Arrange
        from semops.core.config.entity_type_loader import EntityTypeLoader

        loader = EntityTypeLoader(temp_semops_project / ".semops" / "config")
        entity_types = loader.load_entity_types()

        # Act
        domain_type = entity_types.get("semops.core/domain")

        # Assert
        assert domain_type is not None
        assert domain_type["type_key"] == "domain"

    def test_get_entity_type_by_prefix(self, temp_semops_project):
        """Registry should support reverse lookup by ID prefix.

        Given: Loaded entity types
        When: Looking up by id_prefix
        Then: Entity type with that prefix is returned
        """
        # Arrange
        from semops.core.config.entity_type_loader import EntityTypeLoader

        loader = EntityTypeLoader(temp_semops_project / ".semops" / "config")
        registry = loader.build_registry()

        # Act
        domain_type = registry.get_by_prefix("DOM")

        # Assert
        assert domain_type is not None
        assert domain_type["type_key"] == "domain"

    def test_list_entity_types_by_namespace(self, temp_semops_project):
        """Registry should support listing all types in a namespace.

        Given: Multiple entity types in different namespaces
        When: Filtering by namespace
        Then: Only types in that namespace are returned
        """
        # Arrange
        config_file = temp_semops_project / ".semops" / "config" / "entity_types.yaml"

        multi_namespace_data = {
            "entity_types": {
                "semops.core/domain": {
                    "type_key": "domain",
                    "namespace": "semops.core",
                    "id_prefix": "DOM",
                    "display_name": "Domain"
                },
                "custom.ns/entity1": {
                    "type_key": "entity1",
                    "namespace": "custom.ns",
                    "id_prefix": "ENT1",
                    "display_name": "Entity 1"
                },
                "custom.ns/entity2": {
                    "type_key": "entity2",
                    "namespace": "custom.ns",
                    "id_prefix": "ENT2",
                    "display_name": "Entity 2"
                }
            }
        }
        with open(config_file, "w") as f:
            yaml.dump(multi_namespace_data, f)

        from semops.core.config.entity_type_loader import EntityTypeLoader

        loader = EntityTypeLoader(temp_semops_project / ".semops" / "config")
        registry = loader.build_registry()

        # Act
        custom_types = registry.get_by_namespace("custom.ns")

        # Assert
        assert len(custom_types) == 2
        assert all(t["namespace"] == "custom.ns" for t in custom_types)
