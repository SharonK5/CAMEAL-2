"""
===============================================================================
Execution Stage Builder.

Constructs an ExecutionPipeline from a list of stage identifiers.
===============================================================================
"""

from __future__ import annotations

from typing import Sequence

from .execution_stage_resolver import ExecutionStageResolver
from .pipeline import ExecutionPipeline
from .stage import ExecutionStage


class ExecutionStageBuilder:
    """Builds pipelines from stage identifiers using a resolver."""

    def __init__(self, resolver: ExecutionStageResolver) -> None:
        self._resolver = resolver

    def build(self, identifiers: Sequence[str]) -> ExecutionPipeline:
        """Build a pipeline containing only the stages with the given identifiers."""
        pipeline = ExecutionPipeline()
        for ident in identifiers:
            stage = self._resolver._registry.get(ident)
            if stage is None:
                raise KeyError(f"Stage '{ident}' not found in registry")
            pipeline.add_stage(stage)   # use add_stage
        return pipeline

    def build_all(self) -> ExecutionPipeline:
        """Build a pipeline containing all registered stages in registration order."""
        pipeline = ExecutionPipeline()
        for stage in self._resolver._registry.stages():
            pipeline.add_stage(stage)
        return pipeline
