"""
kernel.base
===========

Base classes for all CAMEAL kernel components.

Every major subsystem (Repository, Analytics, ML, AI, Drafting,
Governance, Security, Storage, etc.) should inherit from
KernelComponent.

This ensures a consistent lifecycle across the platform.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class KernelComponent(ABC):
    """
    Abstract base class for all CAMEAL components.

    Every component must implement the same lifecycle methods.
    """

    def __init__(self, name: str) -> None:
        self._name = name
        self._initialized = False

    @property
    def name(self) -> str:
        """Return component name."""
        return self._name

    @property
    def initialized(self) -> bool:
        """Return initialization status."""
        return self._initialized

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the component.
        """
        ...

    @abstractmethod
    def shutdown(self) -> None:
        """
        Gracefully stop the component.
        """
        ...

    @abstractmethod
    def reset(self) -> None:
        """
        Reset runtime state.
        """
        ...

    @abstractmethod
    def health(self) -> dict[str, Any]:
        """
        Return health information.
        """
        ...

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}', initialized={self.initialized})"
        )
