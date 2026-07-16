"""
===============================================================================
Security execution stage.

Executes authorization and risk evaluation.

Author: Sharon Kaitano
===============================================================================
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from query.query_request import QueryRequest

from .base_stage import BaseStage
from .contracts import SecurityResult
from .context_keys import ContextKeys
from .execution_context import ExecutionContext


@runtime_checkable
class SecurityManager(Protocol):
    """Protocol for a security manager that can authorize a query request."""

    def authorize(self, request: QueryRequest) -> SecurityResult:
        ...


class SecurityStage(BaseStage):
    """
    Executes the security subsystem.
    """

    def __init__(
        self,
        security_manager: SecurityManager,
    ) -> None:
        self._manager = security_manager

    @property
    def name(self) -> str:
        return "security"

    def execute(
        self,
        request: QueryRequest,
        context: ExecutionContext,
    ) -> SecurityResult:
        result = self._manager.authorize(request)
        context.set(ContextKeys.SECURITY_RESULT, result)
        return result
