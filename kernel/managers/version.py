# kernel/managers/version.py
"""
Version information for the CAMEAL Kernel Managers subsystem.
"""

PACKAGE_NAME = "cameal.kernel.managers"
DESCRIPTION = "Runtime orchestration managers for the CAMEAL Kernel."

__version__ = "1.0.0"
__api_version__ = "1.0"
API_VERSION = (1, 0)
API_STATUS = "stable"

AUTHOR = "CAMEAL Project"
LICENSE = "Apache-2.0"

VERSION = tuple(int(part) for part in __version__.split("."))

MIN_KERNEL_VERSION = "1.0.0"
MAX_KERNEL_VERSION = "1.x"

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
