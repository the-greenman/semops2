"""gRPC server scaffolding for the SemOps EntityService contract."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

try:
    from semops.generated import services_pb2_grpc as services_rpc
except ImportError:  # pragma: no cover - generated modules not available yet
    services_rpc = None


LOGGER = logging.getLogger(__name__)


class EntityServiceServer(
    services_rpc.EntityServiceServicer if services_rpc else object
):
    """Thin adapter that will map gRPC requests onto the core EntityService."""

    def __init__(self, service_impl) -> None:
        self._service = service_impl
        LOGGER.debug("EntityServiceServer initialized with %s", type(service_impl))

    # TODO: Bridge all RPC methods defined in services.proto once generated stubs exist.
    # Example signature shown below as documentation for future implementation.
    if TYPE_CHECKING:

        async def ListEntities(self, request, context):  # noqa: N802 pylint: disable=invalid-name
            ...

    # Temporary implementation to make the scaffold importable.
    def __getattr__(self, name):
        raise NotImplementedError(
            f"RPC method '{name}' is not implemented yet. Update schema bindings first."
        )


def serve(*, service_impl, server_factory):
    """Placeholder entry point for wiring the gRPC server.

    Args:
        service_impl: Instance providing the business logic (core EntityService).
        server_factory: Callable returning a configured gRPC server.

    Returns:
        gRPC server instance once wiring is completed.
    """

    if services_rpc is None:
        raise RuntimeError(
            "Generated gRPC bindings are missing. Run 'buf generate' before starting the server."
        )

    server = server_factory()
    services_rpc.add_EntityServiceServicer_to_server(EntityServiceServer(service_impl), server)
    LOGGER.info("EntityService gRPC server wired and ready to start")
    return server
