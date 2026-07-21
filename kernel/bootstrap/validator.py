# kernel/bootstrap/validator.py
"""
Runtime validation before kernel startup.
"""

from typing import Optional
from ..container import Container
from ..managers import (
    EngineManager,
    RepositoryManager,
    WorkflowManager,
    ContextManager,
    PluginManager,
    SchedulerManager,
)
from .exceptions import ValidationError


class Validator:
    """
    Validates that the runtime has all required components.
    """

    @staticmethod
    def validate_runtime(
        container: Optional[Container],
        engine_manager: Optional[EngineManager],
        repository_manager: Optional[RepositoryManager],
        workflow_manager: Optional[WorkflowManager],
        context_manager: Optional[ContextManager],
        plugin_manager: Optional[PluginManager],
        scheduler_manager: Optional[SchedulerManager],
    ) -> None:
        Validator.validate_container(container)
        Validator.validate_engines(engine_manager)
        Validator.validate_repositories(repository_manager)
        Validator.validate_workflows(workflow_manager)
        Validator.validate_context(context_manager)
        Validator.validate_plugins(plugin_manager)
        Validator.validate_scheduler(scheduler_manager)

    @staticmethod
    def validate_container(container: Optional[Container]) -> None:
        if container is None:
            raise ValidationError("Container is required")

    @staticmethod
    def validate_engines(engine_manager: Optional[EngineManager]) -> None:
        if engine_manager is None:
            raise ValidationError("Engine manager is required")

    @staticmethod
    def validate_repositories(repository_manager: Optional[RepositoryManager]) -> None:
        if repository_manager is None:
            raise ValidationError("Repository manager is required")

    @staticmethod
    def validate_workflows(workflow_manager: Optional[WorkflowManager]) -> None:
        if workflow_manager is None:
            raise ValidationError("Workflow manager is required")
        if len(workflow_manager) == 0:
            raise ValidationError("At least one workflow must be registered")

    @staticmethod
    def validate_context(context_manager: Optional[ContextManager]) -> None:
        if context_manager is None:
            raise ValidationError("Context manager is required")

    @staticmethod
    def validate_plugins(plugin_manager: Optional[PluginManager]) -> None:
        if plugin_manager is None:
            raise ValidationError("Plugin manager is required")

    @staticmethod
    def validate_scheduler(scheduler_manager: Optional[SchedulerManager]) -> None:
        if scheduler_manager is None:
            raise ValidationError("Scheduler manager is required")
