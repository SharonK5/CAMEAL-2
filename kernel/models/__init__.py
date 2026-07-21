# kernel/models/__init__.py
"""
CAMEAL Kernel Models.

Core data structures shared across the kernel.

Provides:
- Request: Input to the kernel.
- Response: Output from the kernel.
- ExecutionContext: Immutable state flowing through the pipeline.
"""

from .request import Request
from .response import Response
# kernel/models/__init__.py
from .execution_plan import ExecutionPlan
from .execution_context import ExecutionContext
from .version import __version__, __api_version__, VERSION, API_STATUS, PACKAGE_NAME, DESCRIPTION

__all__ = [
    "Request",
    "Response",
    "ExecutionContext",
    "__version__",
    "__api_version__",
    "VERSION",
    "API_STATUS",
    "PACKAGE_NAME",
    "DESCRIPTION",
]
