# kernel/bootstrap/version.py
"""
Version information for the CAMEAL Kernel Bootstrap subsystem.

The Bootstrap subsystem is responsible for constructing and validating
the CAMEAL runtime before execution begins.
"""

# ---------------------------------------------------------------------
# Package Information
# ---------------------------------------------------------------------

PACKAGE_NAME = "cameal.kernel.bootstrap"

DESCRIPTION = (
    "Bootstrap subsystem responsible for constructing, validating, "
    "and initializing the CAMEAL Kernel runtime."
)

# ---------------------------------------------------------------------
# Semantic Versioning
# ---------------------------------------------------------------------

VERSION = (1, 0, 0)

__version__ = ".".join(map(str, VERSION))

# ---------------------------------------------------------------------
# Public API Version
# ---------------------------------------------------------------------

__api_version__ = "1.0"

API_STATUS = "stable"

# ---------------------------------------------------------------------
# Compatibility
# ---------------------------------------------------------------------

MINIMUM_KERNEL_VERSION = "1.0.0"

COMPATIBLE_API_VERSIONS = (
    "1.0",
)

# ---------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------

AUTHOR = "CAMEAL Project"

LICENSE = "Apache-2.0"

PYTHON_REQUIRES = ">=3.11"

# ---------------------------------------------------------------------
# Public Exports
# ---------------------------------------------------------------------

__all__ = [
    "PACKAGE_NAME",
    "DESCRIPTION",
    "VERSION",
    "__version__",
    "__api_version__",
    "API_STATUS",
    "MINIMUM_KERNEL_VERSION",
    "COMPATIBLE_API_VERSIONS",
    "AUTHOR",
    "LICENSE",
    "PYTHON_REQUIRES",
]
