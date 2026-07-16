"""
===============================================================================
Module: query.execution.stage_manager

Execution Stage Manager.

Coordinates stage creation, validation, registration,
resolution, and pipeline construction.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .execution_stage_registry import ExecutionStageRegistry
from .execution_stage_validator import ExecutionStageValidator
from .execution_stage_resolver import ExecutionStageResolver
from .execution_stage_builder import ExecutionStageBuilder
from .pipeline import ExecutionPipeline
from .stage import ExecutionStage


class StageManager:
    """
    Coordinates execution stage infrastructure.

    The manager is the single orchestration point
    for execution stages.
    """

    def __init__(
        self,
        registry: ExecutionStageRegistry | None = None,
        validator: ExecutionStageValidator | None = None,
    ) -> None:
        self._registry = registry or ExecutionStageRegistry()
        self._validator = validator or ExecutionStageValidator()
        self._resolver = ExecutionStageResolver(self._registry)
        self._builder = ExecutionStageBuilder(self._resolver)

    # ------------------------------------------------------------------
    # Components
    # ------------------------------------------------------------------

    @property
    def registry(self) -> ExecutionStageRegistry:
        return self._registry

    @property
    def validator(self) -> ExecutionStageValidator:
        return self._validator

    @property
    def resolver(self) -> ExecutionStageResolver:
        return self._resolver

    @property
    def builder(self) -> ExecutionStageBuilder:
        return self._builder

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, stage: ExecutionStage) -> None:
        """Register a stage. Uses stage.name as identifier."""
        self._validator.validate(stage)
        self._registry.register(stage)

    def unregister(self, identifier: str) -> None:
        self._registry.unregister(identifier)

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def get(self, identifier: str) -> ExecutionStage:
        return self._resolver.get(identifier)

    def contains(self, identifier: str) -> bool:
        return self._resolver.exists(identifier)

    # ------------------------------------------------------------------
    # Pipeline Construction
    # ------------------------------------------------------------------

    def build(self, identifiers: tuple[str, ...]) -> ExecutionPipeline:
        return self._builder.build(identifiers)

    def build_all(self) -> ExecutionPipeline:
        return self._builder.build_all()

    # ------------------------------------------------------------------
    # Registry Utilities
    # ------------------------------------------------------------------

    def identifiers(self) -> tuple[str, ...]:
        return self._registry.identifiers()

    def stages(self) -> tuple[ExecutionStage, ...]:
        return self._registry.stages()

    def clear(self) -> None:
        self._registry.clear()

    def size(self) -> int:
        return self._registry.size()
