# kernel/managers/repository_manager.py
"""
Repository Manager – manages domain repositories.
"""

from typing import Dict, List, Type
from ..lifecycle import Lifecycle, HealthStatus
from .manager import Manager
from .exceptions import ManagerValidationError


class RepositoryManager(Manager):
    """
    Manages domain repositories.

    Responsibilities:
        - Register repositories by name.
        - Resolve repositories by name.
        - Start and stop all repositories.
        - Aggregate health status.
    """

    def __init__(self) -> None:
        super().__init__("repository_manager")

    def register(self, name: str, repository: Lifecycle) -> None:
        """Register a repository."""
        self._validator.validate_name(name)
        self._validator.validate_not_none(repository, "repository")
        super().register(name, repository)

    def start_all(self) -> None:
        """Start all registered repositories."""
        for name in self._registry.list():
            repo = self._registry.get(name)
            if repo.state.value in ("created", "initialized", "validated"):
                repo.start()

    def stop_all(self) -> None:
        """Stop all registered repositories (reverse order)."""
        for name in reversed(self._registry.list()):
            self._registry.get(name).stop()

    def health_all(self) -> Dict[str, HealthStatus]:
        """Return health status of all repositories."""
        return {name: self._registry.get(name).health() for name in self._registry.list()}

    def __len__(self) -> int:
        return len(self._registry)
