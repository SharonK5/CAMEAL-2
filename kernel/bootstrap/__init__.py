# kernel/bootstrap/__init__.py
"""
CAMEAL Kernel Bootstrap.

Initializes the kernel, registers components, and starts the runtime.

Public API:
    - Bootstrap: Main bootstrap class.
    - Configuration: Configuration loader.
"""

from .bootstrap import Bootstrap
from .configuration import Configuration
from .builder import Builder

from .exceptions import (
    BootstrapError,
    ConfigurationError,
    DiscoveryError,
    LoaderError,
    ValidationError,
    RegistrationError,
    DependencyError,
    InitializationError,
)

from .version import (
    PACKAGE_NAME,
    DESCRIPTION,
    VERSION,
    __version__,
    __api_version__,
    API_STATUS,
    MINIMUM_KERNEL_VERSION,
    COMPATIBLE_API_VERSIONS,
    AUTHOR,
    LICENSE,
    PYTHON_REQUIRES,
)

__all__ = [
    "Bootstrap",
    "Configuration",
    "Builder",
    "BootstrapError",
    "ConfigurationError",
    "DiscoveryError",
    "LoaderError",
    "ValidationError",
    "RegistrationError",
    "DependencyError",
    "InitializationError",
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
