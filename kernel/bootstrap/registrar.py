# kernel/bootstrap/registrar.py
"""
Registers kernel components.
"""

from typing import Any, Dict, List, Optional, Type

from ..container import Container
from ..managers import (
    EngineManager,
    RepositoryManager,
    WorkflowManager,
    PluginManager,
    SchedulerManager,
)
from ..orchestrator import ExecutionPlan
from .loader import Loader
from .exceptions import RegistrationError


class Registrar:
    """
    Registers kernel components.
    """

    def __init__(self, container: Container) -> None:
        self._container = container

    def register_engines(self, engine_manager: EngineManager,
                         registrations: List[Dict[str, Any]]) -> None:
        """Register engines."""
        for reg in registrations:
            name = reg.get("name")
            class_path = reg.get("class")
            capabilities = reg.get("capabilities", [])
            if not name or not class_path:
                raise RegistrationError("Engine registration missing name or class")
            try:
                engine = Loader.instantiate(class_path)
                engine_manager.register(name, engine, capabilities)
            except Exception as e:
                raise RegistrationError(f"Failed to register engine '{name}': {e}") from e

    def register_repositories(self, repository_manager: RepositoryManager,
                              registrations: List[Dict[str, Any]]) -> None:
        """Register repositories."""
        for reg in registrations:
            name = reg.get("name")
            class_path = reg.get("class")
            if not name or not class_path:
                raise RegistrationError("Repository registration missing name or class")
            try:
                repo = Loader.instantiate(class_path)
                repository_manager.register(name, repo)
            except Exception as e:
                raise RegistrationError(f"Failed to register repository '{name}': {e}") from e

    def register_workflows(self, workflow_manager: WorkflowManager,
                           registrations: List[Dict[str, Any]]) -> None:
        """Register workflows."""
        for reg in registrations:
            name = reg.get("name")
            steps = reg.get("steps", [])
            default = reg.get("default", False)
            if not name:
                raise RegistrationError("Workflow registration missing name")
            try:
                # ✅ FIX: ExecutionPlan expects workflow_name and engine_names
                plan = ExecutionPlan(workflow_name=name, engine_names=tuple(steps))
                workflow_manager.register(name, plan, default=default)
            except Exception as e:
                raise RegistrationError(f"Failed to register workflow '{name}': {e}") from e
