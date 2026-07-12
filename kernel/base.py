"""
===============================================================================
Module: kernel.base

Abstract base class for all executable CAMEAL kernel components.

Responsibilities:
    - Define the common lifecycle.
    - Define the common execution interface.
    - Provide health reporting.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

# =============================================================================
# Standard Library Imports
# =============================================================================
import logging
from abc import ABC, abstractmethod
from typing import Any

# =============================================================================
# Local Imports
# =============================================================================
from .request import Request
from .response import Response

# =============================================================================
# Module Constants
# =============================================================================

logger = logging.getLogger(__name__)


class KernelComponent(ABC):
    """
    Base class for every executable kernel component.
    """

    def __init__(self, name: str) -> None:
        self._name = name
        self._initialized = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def initialized(self) -> bool:
        return self._initialized

    @abstractmethod
    def initialize(self) -> None:
        ...

    @abstractmethod
    def shutdown(self) -> None:
        ...

    @abstractmethod
    def reset(self) -> None:
        ...

    @abstractmethod
    def execute(self, request: Request) -> Response:
        """
        Execute a kernel request.
        """

    @abstractmethod
    def health(self) -> dict[str, Any]:
        ...

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}', initialized={self.initialized})"
        )
