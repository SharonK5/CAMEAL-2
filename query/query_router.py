"""
===============================================================================
Module: query.query_router

Intent-based router for CAMEAL.

Routes QueryRequests to registered execution handlers.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from collections.abc import Callable

from .query_intent import QueryIntent
from .query_request import QueryRequest
from .query_response import QueryResponse


QueryHandler = Callable[[QueryRequest], QueryResponse]


class QueryRouter:
    """
    Routes QueryRequests according to QueryIntent.
    """

    def __init__(self) -> None:

        self._handlers: dict[
            QueryIntent,
            QueryHandler,
        ] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(

        self,

        intent: QueryIntent,

        handler: QueryHandler,

    ) -> None:

        if intent in self._handlers:

            raise ValueError(
                f"Handler already registered for '{intent.name}'."
            )

        self._handlers[intent] = handler

    # ------------------------------------------------------------------
    # Removal
    # ------------------------------------------------------------------

    def unregister(

        self,

        intent: QueryIntent,

    ) -> None:

        self._handlers.pop(
            intent,
            None,
        )

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def contains(

        self,

        intent: QueryIntent,

    ) -> bool:

        return intent in self._handlers

    def handler(

        self,

        intent: QueryIntent,

    ) -> QueryHandler | None:

        return self._handlers.get(intent)

    # ------------------------------------------------------------------
    # Routing
    # ------------------------------------------------------------------

    def route(

        self,

        request: QueryRequest,

    ) -> QueryResponse:

        handler = self.handler(
            request.intent
        )

        if handler is None:

            raise KeyError(
                f"No handler registered for '{request.intent.name}'."
            )

        return handler(request)

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def clear(self) -> None:

        self._handlers.clear()

    def intents(
        self,
    ) -> tuple[QueryIntent, ...]:

        return tuple(
            sorted(
                self._handlers.keys(),
                key=lambda x: x.name,
            )
        )

    def count(
        self,
    ) -> int:

        return len(self._handlers)

    def __len__(self) -> int:

        return len(self._handlers)
