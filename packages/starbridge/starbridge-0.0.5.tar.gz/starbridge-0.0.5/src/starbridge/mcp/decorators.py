from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from .models import PromptMetadata, ResourceMetadata, ToolMetadata

P = ParamSpec("P")
R = TypeVar("R")


def mcp_tool(
    server: str = "starbridge", service: str | None = None, name: str | None = None
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator to mark a method as an MCP tool.

    Args:
        server (str, optional): The server name. Defaults to "starbridge".
        service (str, optional): The service name. If not provided, derived from module name.
        name (str, optional): The tool name. If not provided, derived from function name.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__mcp_tool__ = ToolMetadata(
            server=server,
            service=service or _get_service_name(func),
            name=name or func.__name__,
        )
        return wrapper

    return decorator


def mcp_resource_iterator(
    server: str = "starbridge", service: str | None = None, type: str = None
):
    """Decorator to mark a method as a resource iterator."""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__mcp_resource_iterator__ = ResourceMetadata(
            server=server,
            service=service or _get_service_name(func),
            type=type,
        )
        return wrapper

    return decorator


def mcp_resource(
    server: str = "starbridge", service: str | None = None, type: str = None
):
    """Decorator to mark a method as a resource handler."""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__mcp_resource__ = ResourceMetadata(
            server=server,
            service=service or _get_service_name(func),
            type=type,
        )
        return wrapper

    return decorator


def mcp_prompt(
    server: str = "starbridge", service: str | None = None, type: str = None
):
    """Decorator to mark a method as a prompt handler."""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__mcp_prompt__ = PromptMetadata(
            server=server,
            service=service or _get_service_name(func),
            type=type or func.__name__.replace("prompt_", ""),
        )
        return wrapper

    return decorator


def _get_service_name(func: Callable) -> str:
    """Extract service name from function's module path."""
    return func.__module__.split(".")[1]
