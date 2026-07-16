"""
===============================================================================
Module: query.query_engine

Governance Query Execution Engine.

Coordinates execution of governance queries through a configurable
pipeline and routes requests to the appropriate execution handler.

The QueryEngine contains no business logic.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .query_request import QueryRequest
from .query_response import QueryResponse
from .query_router import QueryRouter


class QueryEngine:
    """
    Governance Query Engine.

    Responsibilities
    ----------------
    • Owns the execution pipeline.
    • Delegates routing.
    • Returns QueryResponse objects.

    It intentionally does not perform analytics,
    retrieval, monitoring, evaluation or learning.
    """

    def __init__(
        self,
        router: QueryRouter,
    ) -> None:

        self._router = router

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def router(self) -> QueryRouter:
        """
        Return the configured router.
        """
        return self._router

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(
        self,
        request: QueryRequest,
    ) -> QueryResponse:
        """
        Execute a query.

        Current implementation delegates directly
        to the router.

        Future versions will execute a configurable
        execution pipeline before routing.
        TODO: Inject ExecutionPipeline and call:
              context = ExecutionContext()
              response = self.pipeline.execute(request, context=context)
              # inspect context for auditing, logging, etc.
              return self._router.route(response)  # or similar
        """

        return self._router.route(request)
