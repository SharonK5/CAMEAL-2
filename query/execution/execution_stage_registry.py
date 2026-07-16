"""
===============================================================================
Module: query.execution.execution_stage_registry

Execution Stage Registry.
===============================================================================
"""

from __future__ import annotations

from collections import OrderedDict

from .stage import ExecutionStage


class ReadOnlyExecutionStageRegistry:
    """
    Read-only interface to the execution stage registry.
    """

    def __init__(self, stages: OrderedDict[str, ExecutionStage]) -> None:
        self._stages = stages

    def contains(self, identifier: str) -> bool:
        return identifier in self._stages

    def get(self, identifier: str) -> ExecutionStage | None:
        return self._stages.get(identifier)

    def identifiers(self) -> tuple[str, ...]:
        return tuple(self._stages.keys())

    def stages(self) -> tuple[ExecutionStage, ...]:
        return tuple(self._stages.values())

    def items(self) -> tuple[tuple[str, ExecutionStage], ...]:
        return tuple(self._stages.items())

    def size(self) -> int:
        return len(self._stages)

    def __contains__(self, identifier: str) -> bool:
        return self.contains(identifier)

    def __len__(self) -> int:
        return self.size()


class ExecutionStageRegistry(ReadOnlyExecutionStageRegistry):
    """
    Mutable execution stage registry.

    Stages are maintained in registration order.
    """

    def __init__(self) -> None:
        self._stages: OrderedDict[str, ExecutionStage] = OrderedDict()
        super().__init__(self._stages)

    def register(self, stage: ExecutionStage, identifier: str | None = None) -> None:
        """
        Register a stage. Uses stage.name if identifier not provided.
        """
        key = identifier if identifier is not None else stage.name
        if not key.strip():
            raise ValueError("Identifier cannot be empty.")
        if key in self._stages:
            raise ValueError(f"Stage '{key}' already registered.")
        self._stages[key] = stage

    def unregister(self, identifier: str) -> None:
        self._stages.pop(identifier, None)

    def clear(self) -> None:
        self._stages.clear()
