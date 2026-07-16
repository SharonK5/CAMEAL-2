"""
===============================================================================
Module: query.execution.base_stage

Abstract execution stage.

All execution stages inherit from this class.
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from query.query_request import QueryRequest

from .contracts import StageResult
from .execution_context import ExecutionContext


class BaseStage(ABC):
    """
    Base class for every execution stage.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable stage name.
        """

    @abstractmethod
    def execute(
        self,
        request: QueryRequest,
        context: ExecutionContext,
    ) -> StageResult:
        """
        Execute the stage.
        """
