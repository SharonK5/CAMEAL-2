# kernel/lifecycle/version.py
"""
Version information for the CAMEAL Kernel Lifecycle.

Semantic Versioning:
MAJOR.MINOR.PATCH
"""

from __future__ import annotations

__version__ = "1.0.0"
__api_version__ = "1.0.0"
VERSION = (1, 0, 0)
API_STATUS = "stable"
PACKAGE_NAME = "cameal.kernel.lifecycle"
DESCRIPTION = "Standard lifecycle contract for kernel-managed components"

__all__ = [
    "__version__",
    "__api_version__",
    "VERSION",
    "API_STATUS",
    "PACKAGE_NAME",
    "DESCRIPTION",
]
