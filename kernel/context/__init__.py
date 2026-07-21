# kernel/context/__init__.py
"""
CAMEAL Kernel Context.

Execution context management for the CAMEAL Kernel.

Provides immutable runtime context propagation, traceability, provenance,
security, workflow, and request context.

Public API:
    - ExecutionContext
    - RequestContext
    - SecurityContext
    - WorkflowContext
    - TraceContext
    - ProvenanceContext
    - ContextBuilder
"""

from .execution_context import ExecutionContext
from .request_context import RequestContext
from .security_context import SecurityContext
from .workflow_context import WorkflowContext
from .trace_context import TraceContext
from .provenance_context import ProvenanceContext
from .context_builder import ContextBuilder
from .context_validator import ContextValidator
from .context_registry import ContextRegistry

from .exceptions import (
    ContextError,
    ContextValidationError,
    ContextBuilderError,
    ContextNotFoundError,
    ContextRegistryError,
)

from .version import (
    __version__,
    __api_version__,
    VERSION,
    API_VERSION,
    API_STATUS,
    PACKAGE_NAME,
    DESCRIPTION,
    MIN_KERNEL_VERSION,
    MAX_KERNEL_VERSION,
    AUTHOR,
    LICENSE,
)

__all__ = [
    "ExecutionContext",
    "RequestContext",
    "SecurityContext",
    "WorkflowContext",
    "TraceContext",
    "ProvenanceContext",
    "ContextBuilder",
    "ContextValidator",
    "ContextRegistry",
    "ContextError",
    "ContextValidationError",
    "ContextBuilderError",
    "ContextNotFoundError",
    "ContextRegistryError",
    "__version__",
    "__api_version__",
    "VERSION",
    "API_VERSION",
    "API_STATUS",
    "PACKAGE_NAME",
    "DESCRIPTION",
    "MIN_KERNEL_VERSION",
    "MAX_KERNEL_VERSION",
    "AUTHOR",
    "LICENSE",
]
