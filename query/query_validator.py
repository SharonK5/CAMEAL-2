"""
===============================================================================
Module: query.query_validator

Validation for QueryRequest objects.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .query_intent import QueryIntent
from .query_request import QueryRequest


class QueryValidator:
    """
    Validates QueryRequest instances.

    This validator checks only the structural integrity of a request.
    It does not execute queries or verify repository availability.
    """

    def validate(
        self,
        request: QueryRequest,
    ) -> None:
        """
        Validate a QueryRequest.

        Raises
        ------
        TypeError
            If the object is not a QueryRequest.

        ValueError
            If the request violates the query contract.
        """

        if not isinstance(request, QueryRequest):
            raise TypeError(
                "request must be a QueryRequest."
            )

        if not request.identifier.strip():
            raise ValueError(
                "identifier cannot be empty."
            )

        if not request.query.strip():
            raise ValueError(
                "query cannot be empty."
            )

        if not isinstance(request.intent, QueryIntent):
            raise ValueError(
                "intent must be a QueryIntent."
            )

        if request.priority < 0:
            raise ValueError(
                "priority cannot be negative."
            )

        for repository in request.repositories:

            if not repository.strip():
                raise ValueError(
                    "repository names cannot be empty."
                )

        for key, _ in request.parameters:

            if not str(key).strip():
                raise ValueError(
                    "parameter names cannot be empty."
                )

        for key, _ in request.metadata:

            if not str(key).strip():
                raise ValueError(
                    "metadata names cannot be empty."
                )

    def is_valid(
        self,
        request: QueryRequest,
    ) -> bool:
        """
        Return True if the request is valid.
        """

        try:

            self.validate(request)

            return True

        except (TypeError, ValueError):

            return False
