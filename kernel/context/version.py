# kernel/context/version.py
"""
Version information for the CAMEAL Kernel Context subsystem.

This module exposes semantic versioning metadata for both the
implementation and the public API contract.

Public API:
    - ExecutionContext
    - RequestContext
    - SecurityContext
    - WorkflowContext
    - TraceContext
    - ProvenanceContext
    - ContextBuilder
"""

PACKAGE_NAME = "cameal.kernel.context"

DESCRIPTION = (
    "Execution context subsystem for the CAMEAL Kernel. "
    "Provides immutable runtime context propagation, "
    "traceability, provenance, security, workflow, and request context."
)

# ---------------------------------------------------------------------
# Semantic Versioning
# ---------------------------------------------------------------------

#: Current implementation version.
VERSION = (1, 0, 0)

#: Human-readable implementation version.
__version__ = ".".join(map(str, VERSION))

# ---------------------------------------------------------------------
# Public API Version
# ---------------------------------------------------------------------

#: Public API version.
API_VERSION = (1, 0)

#: Human-readable API version.
__api_version__ = ".".join(map(str, API_VERSION))

#: Stability indicator.
API_STATUS = "stable"

# ---------------------------------------------------------------------
# Compatibility
# ---------------------------------------------------------------------

#: Minimum supported kernel version.
MIN_KERNEL_VERSION = "1.0.0"

#: Maximum compatible kernel version.
MAX_KERNEL_VERSION = "1.x"

# ---------------------------------------------------------------------
# Module Metadata
# ---------------------------------------------------------------------

AUTHOR = "CAMEAL Project"

LICENSE = "Apache-2.0"

__all__ = [
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
