"""
Version information for the CAMEAL Kernel Container.

Semantic Versioning:
MAJOR.MINOR.PATCH
"""

from __future__ import annotations

# Package implementation version
__version__ = "1.0.0"

# Stable public API version
__api_version__ = "1.0.0"

# Semantic version tuple
VERSION = (1, 0, 0)

# Stability level
API_STATUS = "stable"

# Package metadata
PACKAGE_NAME = "cameal.kernel.container"
DESCRIPTION = "Dependency Injection Container for the CAMEAL Kernel"

__all__ = [
    "__version__",
    "__api_version__",
    "VERSION",
    "API_STATUS",
    "PACKAGE_NAME",
    "DESCRIPTION",
]
