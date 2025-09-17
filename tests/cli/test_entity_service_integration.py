"""Integration tests for the CLI talking to the EntityService.

This scaffold ensures pytest discovers the module once the CLI layer
binds to the generated gRPC clients."""

import pytest


pytestmark = pytest.mark.skip(reason="CLI integration tests require CLI and gRPC wiring")


def test_cli_integration_placeholder():
    """Placeholder assertion while the CLI scaffolding is built out."""

    assert True
