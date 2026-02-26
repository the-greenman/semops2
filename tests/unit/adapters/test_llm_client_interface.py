"""Unit tests for LLM client adapter interface.

Tests the structured output interface for LLM clients with:
- Instructor/Pydantic validation
- Retry logic
- Response metadata
"""

import pytest
from typing import Dict, Any

try:
    from pydantic import BaseModel
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    # Create stub for test collection
    class BaseModel:
        pass


pytestmark = [pytest.mark.unit, pytest.mark.skip_until_phase0]


if PYDANTIC_AVAILABLE:
    # Sample Pydantic model for testing
    class SampleAnalysis(BaseModel):
        """Sample structured output schema."""
        summary: str
        confidence: float
        recommendations: list
else:
    class SampleAnalysis:
        """Stub for when pydantic not available."""
        pass


@pytest.mark.skip(reason="LLMStructuredClient not yet implemented")
class TestLLMStructuredOutput:
    """Test structured output generation with validation."""

    def test_structured_output_valid_response(self, mock_llm_client):
        """LLM client should return validated structured output.

        Given: Valid LLM response matching schema
        When: Generating structured output
        Then: Response is validated and includes metadata
        """
        # Arrange
        from semops.core.adapters.llm_client import LLMStructuredClient

        mock_llm_client.add_canned_response({
            "summary": "Test analysis",
            "confidence": 0.85,
            "recommendations": ["Recommendation 1", "Recommendation 2"]
        })

        client = LLMStructuredClient(backend=mock_llm_client)

        # Act
        result = client.generate(
            prompt="Analyze this entity",
            schema=SampleAnalysis,
            metadata={"prompt_version": "1.0.0"}
        )

        # Assert
        assert isinstance(result.data, SampleAnalysis)
        assert result.data.summary == "Test analysis"
        assert result.data.confidence == 0.85
        assert len(result.data.recommendations) == 2

        # Verify metadata
        assert result.metadata["schema_validated"] is True
        assert result.metadata["prompt_version"] == "1.0.0"
        assert "trace_id" in result.metadata

    def test_structured_output_malformed_with_retry(self, mock_llm_client):
        """LLM client should retry on malformed response.

        Given: First response is malformed, second is valid
        When: Generating structured output
        Then: Client retries and succeeds
        """
        # Arrange
        from semops.core.adapters.llm_client import LLMStructuredClient

        # First response: malformed (missing required field)
        mock_llm_client.add_canned_response({
            "summary": "Test",
            # Missing confidence and recommendations
        })

        # Second response: valid
        mock_llm_client.add_canned_response({
            "summary": "Test analysis",
            "confidence": 0.75,
            "recommendations": ["Retry succeeded"]
        })

        client = LLMStructuredClient(
            backend=mock_llm_client,
            max_retries=2
        )

        # Act
        result = client.generate(
            prompt="Analyze this entity",
            schema=SampleAnalysis
        )

        # Assert
        assert isinstance(result.data, SampleAnalysis)
        assert result.data.recommendations == ["Retry succeeded"]
        assert mock_llm_client.call_count == 2  # Retried once

    def test_structured_output_exhausted_retries(self, mock_llm_client):
        """LLM client should fail after exhausting retries.

        Given: All responses are malformed
        When: Generating structured output
        Then: ValidationError is raised after max retries
        """
        # Arrange
        from semops.core.adapters.llm_client import LLMStructuredClient, ValidationError

        # All malformed responses
        for _ in range(3):
            mock_llm_client.add_canned_response({
                "invalid": "data"
            })

        client = LLMStructuredClient(
            backend=mock_llm_client,
            max_retries=2
        )

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            client.generate(
                prompt="Analyze this entity",
                schema=SampleAnalysis
            )

        assert "validation failed" in str(exc_info.value).lower()
        assert "retries exhausted" in str(exc_info.value).lower()
        assert mock_llm_client.call_count == 3  # Initial + 2 retries

    def test_response_includes_metadata(self, mock_llm_client):
        """Response should include required metadata fields.

        Given: Valid structured output
        When: Response is returned
        Then: Metadata includes schema_validated, prompt_version, trace_id
        """
        # Arrange
        from semops.core.adapters.llm_client import LLMStructuredClient

        mock_llm_client.add_canned_response({
            "summary": "Test",
            "confidence": 0.8,
            "recommendations": []
        })

        client = LLMStructuredClient(backend=mock_llm_client)

        # Act
        result = client.generate(
            prompt="Test prompt",
            schema=SampleAnalysis,
            metadata={
                "prompt_version": "2.0.0",
                "entity_id": "DOM-001"
            }
        )

        # Assert
        metadata = result.metadata

        # Required fields
        assert "schema_validated" in metadata
        assert metadata["schema_validated"] is True

        assert "prompt_version" in metadata
        assert metadata["prompt_version"] == "2.0.0"

        assert "trace_id" in metadata
        assert isinstance(metadata["trace_id"], str)

        # Custom metadata preserved
        assert metadata["entity_id"] == "DOM-001"


@pytest.mark.skip(reason="LLMStructuredClient not yet implemented")
class TestLLMClientRetryBehavior:
    """Test retry behavior and error handling."""

    def test_exponential_backoff_on_retries(self, mock_llm_client):
        """Retries should use exponential backoff.

        Given: Retry scenario
        When: Multiple retries occur
        Then: Backoff delay increases exponentially
        """
        # Arrange
        from semops.core.adapters.llm_client import LLMStructuredClient
        import time

        # All malformed to trigger retries
        for _ in range(2):
            mock_llm_client.add_canned_response({"invalid": "data"})

        client = LLMStructuredClient(
            backend=mock_llm_client,
            max_retries=1,
            initial_backoff=0.01  # 10ms for testing
        )

        # Act
        start_time = time.time()
        try:
            client.generate(
                prompt="Test",
                schema=SampleAnalysis
            )
        except Exception:
            pass
        elapsed = time.time() - start_time

        # Assert
        # Should have some delay from backoff (at least 10ms)
        assert elapsed >= 0.01

    def test_retry_count_in_metadata(self, mock_llm_client):
        """Metadata should include retry count.

        Given: Response succeeds after retries
        When: Result is returned
        Then: Metadata includes retry_count
        """
        # Arrange
        from semops.core.adapters.llm_client import LLMStructuredClient

        # First malformed, second valid
        mock_llm_client.add_canned_response({"invalid": "data"})
        mock_llm_client.add_canned_response({
            "summary": "Success",
            "confidence": 0.9,
            "recommendations": []
        })

        client = LLMStructuredClient(
            backend=mock_llm_client,
            max_retries=2
        )

        # Act
        result = client.generate(
            prompt="Test",
            schema=SampleAnalysis
        )

        # Assert
        assert result.metadata["retry_count"] == 1


@pytest.mark.skip(reason="LLMStructuredClient not yet implemented")
class TestLLMClientConfiguration:
    """Test LLM client configuration options."""

    def test_custom_validation_error_handler(self, mock_llm_client):
        """Client should support custom validation error handling.

        Given: Custom error handler
        When: Validation fails
        Then: Custom handler is invoked
        """
        # Arrange
        from semops.core.adapters.llm_client import LLMStructuredClient

        mock_llm_client.add_canned_response({"invalid": "data"})

        error_handled = []

        def custom_error_handler(error, attempt):
            error_handled.append((error, attempt))

        client = LLMStructuredClient(
            backend=mock_llm_client,
            max_retries=0,
            on_validation_error=custom_error_handler
        )

        # Act
        try:
            client.generate(prompt="Test", schema=SampleAnalysis)
        except Exception:
            pass

        # Assert
        assert len(error_handled) == 1
        assert error_handled[0][1] == 0  # Attempt number

    def test_model_parameter_passed_to_backend(self, mock_llm_client):
        """Model parameter should be passed to LLM backend.

        Given: Client with specific model
        When: Generating output
        Then: Model parameter is passed to backend
        """
        # Arrange
        from semops.core.adapters.llm_client import LLMStructuredClient

        mock_llm_client.add_canned_response({
            "summary": "Test",
            "confidence": 0.8,
            "recommendations": []
        })

        client = LLMStructuredClient(
            backend=mock_llm_client,
            default_model="claude-3-5-sonnet"
        )

        # Act
        result = client.generate(
            prompt="Test",
            schema=SampleAnalysis
        )

        # Assert
        # Backend should have received model parameter
        assert result.metadata.get("model") == "claude-3-5-sonnet"
