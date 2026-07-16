"""
===============================================================================
Module: query.execution.repository_stage
===============================================================================
"""

from __future__ import annotations

from repository.repository_manager import RepositoryManager

from .context_keys import ContextKeys
from .contracts import RepositoryResult, Repository
from .execution_context import ExecutionContext
from .stage import ExecutionStage


class RepositoryStage(ExecutionStage):
    def __init__(self, manager: RepositoryManager) -> None:
        self._manager = manager

    @property
    def name(self) -> str:
        return "repository"

    def execute(
        self,
        request,
        context: ExecutionContext,
    ) -> RepositoryResult:
        repositories = tuple(
            self._manager.get(identifier)
            for identifier in request.repositories
        )

        context.set(ContextKeys.REPOSITORIES, repositories)

        return RepositoryResult(
            success=True,
            stage=self.name,
            repositories=repositories,
            count=len(repositories),
            metadata=(("resolved", True),),
        )
