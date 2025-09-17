"""Server adapters for SemOps gRPC interfaces."""

from .entity_service_server import EntityServiceServer, serve

__all__ = ["EntityServiceServer", "serve"]
