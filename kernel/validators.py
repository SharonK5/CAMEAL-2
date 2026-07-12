"""
===============================================================================
Module: kernel.validators

Kernel request validation.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .request import Request


class RequestValidator:
    """
    Kernel request validator.
    """

    def validate(self, request: Request) -> None:

        self._validate_action(request)

        self._validate_payload(request)

        self._validate_metadata(request)

        self._validate_priority(request)

        self._validate_workflow(request)

    @staticmethod
    def _validate_action(request: Request) -> None:

        if not request.action.strip():

            raise ValueError("Action cannot be empty.")

    @staticmethod
    def _validate_payload(request: Request) -> None:

        if not isinstance(request.payload, dict):

            raise TypeError("Payload must be a dictionary.")

    @staticmethod
    def _validate_metadata(request: Request) -> None:

        if not isinstance(request.metadata, dict):

            raise TypeError("Metadata must be a dictionary.")

    @staticmethod
    def _validate_priority(request: Request) -> None:

        if request.priority < 0:

            raise ValueError("Priority cannot be negative.")

    @staticmethod
    def _validate_workflow(request: Request) -> None:

        if (
            request.workflow is not None
            and not request.workflow.strip()
        ):

            raise ValueError("Workflow cannot be empty.")
