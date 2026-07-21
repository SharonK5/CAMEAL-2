# kernel/events/version.py
"""
Version information for the CAMEAL Kernel Events.

Semantic Versioning:
MAJOR.MINOR.PATCH
"""

from __future__ import annotations

__version__ = "1.0.0"
__api_version__ = "1.0.0"
VERSION = (1, 0, 0)
API_STATUS = "stable"
PACKAGE_NAME = "cameal.kernel.events"
DESCRIPTION = "Event Bus and Execution Pipeline for the CAMEAL Kernel"

__all__ = [
    "__version__",
    "__api_version__",
    "VERSION",
    "API_STATUS",
    "PACKAGE_NAME",
    "DESCRIPTION",
]
