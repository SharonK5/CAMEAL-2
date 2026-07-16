"""
===============================================================================
Module: services.service

Abstract Service Contract.

Defines the common lifecycle for all CAMEAL services.

Services implement business logic while execution stages coordinate
workflow.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Service(ABC):
    """
    Base class for all CAMEAL services.

    Services encapsulate business logic and are intended to be invoked
    by execution stages. They should remain independent of workflow
    orchestration.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the unique service identifier.
        """

    @property
    def initialized(self) -> bool:
        """
        Indicates whether the service has been initialized.
        """
        return getattr(self, "_initialized", False)

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the service.

        Called once before the service is used.
        """

    @abstractmethod
    def shutdown(self) -> None:
        """
        Shutdown the service and release resources.

        Called when the service is no longer required.
        """

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def ensure_initialized(self) -> None:
        """
        Ensure the service has been initialized.

        Raises
        ------
        RuntimeError
            If initialize() has not been called.
        """
        if not self.initialized:
            raise RuntimeError(
                f"Service '{self.name}' has not been initialized."
            )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name={self.name!r}, initialized={self.initialized})"
        )
