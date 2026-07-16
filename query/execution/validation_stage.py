"""
===============================================================================
Module: query.execution.validation_stage

Validation execution stage.

Validates incoming QueryRequest objects before execution proceeds.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from query.query_request import QueryRequest
from query.query_response import QueryResponse
from query.query_validator import QueryValidator

from .execution_context import ExecutionContext
from .stage import ExecutionStage


class ValidationStage(ExecutionStage):
    """
    Pipeline stage responsible for validating QueryRequest objects.
    """

    def __init__(
        self,
        validator: QueryValidator | None = None,
    ) -> None:

        self._validator = validator or QueryValidator()

    @property
    def name(self) -> str:
        return "validation"

    @property
    def validator(self) -> QueryValidator:
        return self._validator

    def execute(
        self,
        request: QueryRequest,
        context: ExecutionContext,
    ) -> QueryResponse | None:
        """
        Validate the request.

        On success the pipeline continues.
        """

        self._validator.validate(request)

        context.set(
            "validated",
            True,
        )

        return None
