# kernel/container/__init__.py
"""
CAMEAL Kernel Container.

Dependency Injection (DI) subsystem for the CAMEAL Kernel.
"""

from .container import Container
from .dependency import Dependency
from .registration import Registration
from .scopes import Scope
from .state import ContainerState

from .exceptions import (
    CircularDependencyError,
    ContainerError,
    RegistrationError,
    ResolutionError,
    ScopeError,
    StateError,
    ValidationError,
)

from .version import (
    API_STATUS,
    DESCRIPTION,
    PACKAGE_NAME,
    VERSION,
    __api_version__,
    __version__,
)

SUPPORTED_SCOPES = (
    Scope.SINGLETON,
    Scope.REQUEST,
    Scope.TRANSIENT,
)

__all__ = (
    "Container",
    "Dependency",
    "Registration",
    "Scope",
    "ContainerState",
    "ContainerError",
    "RegistrationError",
    "ResolutionError",
    "CircularDependencyError",
    "ScopeError",
    "StateError",
    "ValidationError",
    "__version__",
    "__api_version__",
    "VERSION",
    "API_STATUS",
    "PACKAGE_NAME",
    "DESCRIPTION",
    "SUPPORTED_SCOPES",
)
