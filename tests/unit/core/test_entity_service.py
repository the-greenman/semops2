"""Unit tests for EntityService.

Tests file-first CRUD operations, actor attribution, and validation.
"""

import pytest
from pathlib import Path
from datetime import datetime


pytestmark = [pytest.mark.unit, pytest.mark.skip_until_phase1]


@pytest.mark.skip(reason="EntityService not yet implemented")
class TestEntityCreation:
    """Test entity creation logic."""

    def test_create_entity_writes_canonical_file(self, temp_semops_project, sample_entity_data):
        """Creating an entity should write canonical markdown file.

        Given: Valid entity data with actor_id
        When: Creating entity via EntityService
        Then: Markdown file with frontmatter is written to canonical location
        """
        # Arrange
        from semops.core.services.entity_service import EntityService

        service = EntityService(project_root=temp_semops_project)

        # Act
        entity = service.create_entity(
            entity_type="semops.core/domain",
            data=sample_entity_data,
            actor_id="ACT-human-test-user"
        )

        # Assert
        assert entity["entity_id"] is not None
        assert entity["entity_id"].startswith("DOM-")

        # Check file exists
        entity_file = temp_semops_project / ".semops" / "entities" / "domains" / f"{entity['entity_id']}.md"
        assert entity_file.exists()

        # Verify file content
        content = entity_file.read_text()
        assert "---" in content  # Frontmatter markers
        assert sample_entity_data["domain_name"] in content
        assert sample_entity_data["purpose"] in content

    def test_create_entity_validates_required_fields(self, temp_semops_project):
        """Creating entity without required fields should fail.

        Given: Entity data missing required field
        When: Creating entity
        Then: ValidationError is raised
        """
        # Arrange
        from semops.core.services.entity_service import EntityService, ValidationError

        service = EntityService(project_root=temp_semops_project)

        incomplete_data = {
            "domain_name": "Test Domain"
            # Missing required 'purpose' field
        }

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            service.create_entity(
                entity_type="semops.core/domain",
                data=incomplete_data,
                actor_id="ACT-human-test-user"
            )

        assert "purpose" in str(exc_info.value).lower()
        assert "required" in str(exc_info.value).lower()

    def test_create_entity_requires_actor_id(self, temp_semops_project, sample_entity_data):
        """Creating entity without actor_id should fail.

        Given: Entity data without actor_id
        When: Creating entity
        Then: ValidationError is raised
        """
        # Arrange
        from semops.core.services.entity_service import EntityService, ValidationError

        service = EntityService(project_root=temp_semops_project)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            service.create_entity(
                entity_type="semops.core/domain",
                data=sample_entity_data,
                actor_id=None  # Missing actor_id
            )

        assert "actor_id" in str(exc_info.value).lower()
        assert "required" in str(exc_info.value).lower()

    def test_create_entity_generates_unique_id(self, temp_semops_project, sample_entity_data):
        """Each created entity should have unique ID.

        Given: Multiple entities with same name
        When: Creating entities
        Then: Each gets unique entity_id
        """
        # Arrange
        from semops.core.services.entity_service import EntityService

        service = EntityService(project_root=temp_semops_project)

        # Act
        entity1 = service.create_entity(
            entity_type="semops.core/domain",
            data=sample_entity_data,
            actor_id="ACT-human-test-user"
        )

        entity2 = service.create_entity(
            entity_type="semops.core/domain",
            data=sample_entity_data,  # Same data
            actor_id="ACT-human-test-user"
        )

        # Assert
        assert entity1["entity_id"] != entity2["entity_id"]
        assert entity1["entity_id"].startswith("DOM-")
        assert entity2["entity_id"].startswith("DOM-")

    def test_create_entity_sets_timestamps(self, temp_semops_project, sample_entity_data):
        """Created entity should have created_at timestamp.

        Given: Entity creation
        When: Creating entity
        Then: created_at and updated_at are set
        """
        # Arrange
        from semops.core.services.entity_service import EntityService

        service = EntityService(project_root=temp_semops_project)

        # Act
        before = datetime.utcnow()
        entity = service.create_entity(
            entity_type="semops.core/domain",
            data=sample_entity_data,
            actor_id="ACT-human-test-user"
        )
        after = datetime.utcnow()

        # Assert
        assert "created_at" in entity
        assert "updated_at" in entity

        created_at = datetime.fromisoformat(entity["created_at"])
        assert before <= created_at <= after


@pytest.mark.skip(reason="EntityService not yet implemented")
class TestEntityUpdate:
    """Test entity update logic."""

    def test_update_entity_preserves_frontmatter(self, temp_semops_project, sample_entity_data, sample_entity_id):
        """Updating entity should preserve frontmatter metadata.

        Given: Existing entity
        When: Updating entity data
        Then: Frontmatter metadata is preserved and merged
        """
        # Arrange
        from semops.core.services.entity_service import EntityService

        service = EntityService(project_root=temp_semops_project)

        # Create entity
        entity = service.create_entity(
            entity_type="semops.core/domain",
            data=sample_entity_data,
            actor_id="ACT-human-test-user"
        )

        # Act
        updated_data = {"purpose": "Updated purpose"}
        updated_entity = service.update_entity(
            entity_id=entity["entity_id"],
            data=updated_data,
            actor_id="ACT-human-updated-user"
        )

        # Assert
        assert updated_entity["purpose"] == "Updated purpose"
        assert updated_entity["domain_name"] == sample_entity_data["domain_name"]  # Preserved
        assert updated_entity["created_at"] == entity["created_at"]  # Preserved
        assert updated_entity["updated_at"] != entity["updated_at"]  # Changed

    def test_update_entity_requires_actor_id(self, temp_semops_project, sample_entity_data):
        """Updating entity without actor_id should fail.

        Given: Existing entity
        When: Updating without actor_id
        Then: ValidationError is raised
        """
        # Arrange
        from semops.core.services.entity_service import EntityService, ValidationError

        service = EntityService(project_root=temp_semops_project)

        entity = service.create_entity(
            entity_type="semops.core/domain",
            data=sample_entity_data,
            actor_id="ACT-human-test-user"
        )

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            service.update_entity(
                entity_id=entity["entity_id"],
                data={"purpose": "Updated"},
                actor_id=None  # Missing
            )

        assert "actor_id" in str(exc_info.value).lower()

    def test_update_nonexistent_entity_raises_error(self, temp_semops_project):
        """Updating non-existent entity should fail.

        Given: Non-existent entity_id
        When: Attempting to update
        Then: EntityNotFoundError is raised
        """
        # Arrange
        from semops.core.services.entity_service import EntityService, EntityNotFoundError

        service = EntityService(project_root=temp_semops_project)

        # Act & Assert
        with pytest.raises(EntityNotFoundError) as exc_info:
            service.update_entity(
                entity_id="DOM-999-nonexistent",
                data={"purpose": "Updated"},
                actor_id="ACT-human-test-user"
            )

        assert "DOM-999-nonexistent" in str(exc_info.value)


@pytest.mark.skip(reason="EntityService not yet implemented")
class TestEntityRetrieval:
    """Test entity retrieval logic."""

    def test_get_entity_reads_from_file(self, temp_semops_project, sample_entity_data):
        """Getting entity should read from canonical file.

        Given: Existing entity file
        When: Getting entity by ID
        Then: Entity data is loaded from file
        """
        # Arrange
        from semops.core.services.entity_service import EntityService

        service = EntityService(project_root=temp_semops_project)

        entity = service.create_entity(
            entity_type="semops.core/domain",
            data=sample_entity_data,
            actor_id="ACT-human-test-user"
        )

        # Act
        retrieved = service.get_entity(entity_id=entity["entity_id"])

        # Assert
        assert retrieved["entity_id"] == entity["entity_id"]
        assert retrieved["domain_name"] == sample_entity_data["domain_name"]
        assert retrieved["purpose"] == sample_entity_data["purpose"]

    def test_list_entities_by_type(self, temp_semops_project, sample_entity_data):
        """Listing entities should return all of specified type.

        Given: Multiple entities of different types
        When: Listing by entity_type
        Then: Only entities of that type are returned
        """
        # Arrange
        from semops.core.services.entity_service import EntityService

        service = EntityService(project_root=temp_semops_project)

        # Create multiple entities
        entity1 = service.create_entity(
            entity_type="semops.core/domain",
            data=sample_entity_data,
            actor_id="ACT-human-test-user"
        )

        entity2 = service.create_entity(
            entity_type="semops.core/domain",
            data={**sample_entity_data, "domain_name": "Another Domain"},
            actor_id="ACT-human-test-user"
        )

        # Act
        entities = service.list_entities(entity_type="semops.core/domain")

        # Assert
        assert len(entities) == 2
        entity_ids = {e["entity_id"] for e in entities}
        assert entity1["entity_id"] in entity_ids
        assert entity2["entity_id"] in entity_ids

    def test_get_nonexistent_entity_raises_error(self, temp_semops_project):
        """Getting non-existent entity should fail.

        Given: Non-existent entity_id
        When: Getting entity
        Then: EntityNotFoundError is raised
        """
        # Arrange
        from semops.core.services.entity_service import EntityService, EntityNotFoundError

        service = EntityService(project_root=temp_semops_project)

        # Act & Assert
        with pytest.raises(EntityNotFoundError) as exc_info:
            service.get_entity(entity_id="DOM-999-nonexistent")

        assert "DOM-999-nonexistent" in str(exc_info.value)


@pytest.mark.skip(reason="EntityService not yet implemented")
class TestEntityDeletion:
    """Test entity deletion logic."""

    def test_delete_entity_cascade_option(self, temp_semops_project, sample_entity_data):
        """Delete with cascade should delete child entities.

        Given: Parent entity with children
        When: Deleting with cascade=True
        Then: Parent and children are deleted
        """
        # Arrange
        from semops.core.services.entity_service import EntityService

        service = EntityService(project_root=temp_semops_project)

        parent = service.create_entity(
            entity_type="semops.core/domain",
            data=sample_entity_data,
            actor_id="ACT-human-test-user"
        )

        # Act
        result = service.delete_entity(
            entity_id=parent["entity_id"],
            cascade=True,
            actor_id="ACT-human-test-user"
        )

        # Assert
        assert result["success"] is True
        assert result["deleted_count"] >= 1

        # Verify entity is gone
        from semops.core.services.entity_service import EntityNotFoundError
        with pytest.raises(EntityNotFoundError):
            service.get_entity(entity_id=parent["entity_id"])

    def test_delete_entity_requires_actor_id(self, temp_semops_project, sample_entity_data):
        """Deleting entity without actor_id should fail.

        Given: Existing entity
        When: Deleting without actor_id
        Then: ValidationError is raised
        """
        # Arrange
        from semops.core.services.entity_service import EntityService, ValidationError

        service = EntityService(project_root=temp_semops_project)

        entity = service.create_entity(
            entity_type="semops.core/domain",
            data=sample_entity_data,
            actor_id="ACT-human-test-user"
        )

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            service.delete_entity(
                entity_id=entity["entity_id"],
                actor_id=None  # Missing
            )

        assert "actor_id" in str(exc_info.value).lower()


@pytest.mark.skip(reason="EntityService not yet implemented")
class TestActorAttribution:
    """Test actor attribution enforcement."""

    def test_mutation_without_actor_id_rejected(self, temp_semops_project, sample_entity_data):
        """All mutations must include actor_id.

        Given: Mutation operation without actor_id
        When: Attempting mutation
        Then: ValidationError is raised
        """
        # Arrange
        from semops.core.services.entity_service import EntityService, ValidationError

        service = EntityService(project_root=temp_semops_project)

        # Act & Assert - Create without actor_id
        with pytest.raises(ValidationError) as exc_info:
            service.create_entity(
                entity_type="semops.core/domain",
                data=sample_entity_data,
                actor_id=None
            )

        assert "actor_id" in str(exc_info.value).lower()
        assert "required" in str(exc_info.value).lower()

    def test_created_by_actor_id_recorded(self, temp_semops_project, sample_entity_data):
        """Entity should record who created it.

        Given: Entity creation with actor_id
        When: Creating entity
        Then: created_by_actor_id is recorded
        """
        # Arrange
        from semops.core.services.entity_service import EntityService

        service = EntityService(project_root=temp_semops_project)

        # Act
        entity = service.create_entity(
            entity_type="semops.core/domain",
            data=sample_entity_data,
            actor_id="ACT-human-alice"
        )

        # Assert
        assert entity["created_by_actor_id"] == "ACT-human-alice"

    def test_updated_by_actor_id_recorded(self, temp_semops_project, sample_entity_data):
        """Entity should record who updated it.

        Given: Entity update with actor_id
        When: Updating entity
        Then: updated_by_actor_id is recorded
        """
        # Arrange
        from semops.core.services.entity_service import EntityService

        service = EntityService(project_root=temp_semops_project)

        entity = service.create_entity(
            entity_type="semops.core/domain",
            data=sample_entity_data,
            actor_id="ACT-human-alice"
        )

        # Act
        updated = service.update_entity(
            entity_id=entity["entity_id"],
            data={"purpose": "Updated purpose"},
            actor_id="ACT-human-bob"
        )

        # Assert
        assert updated["created_by_actor_id"] == "ACT-human-alice"
        assert updated["updated_by_actor_id"] == "ACT-human-bob"
