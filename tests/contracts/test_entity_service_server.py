"""Contract tests for the EntityService gRPC server.

Currently skipped until the generated protobuf stubs and core service
implementation are available."""

import pytest


pytestmark = pytest.mark.skip(reason="Contract tests depend on generated gRPC bindings")


def test_entity_service_contract_placeholder():
    """Placeholder to keep the test module discoverable."""

    assert True
