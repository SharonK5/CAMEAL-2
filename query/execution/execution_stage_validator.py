"""
===============================================================================
Module: query.execution.stage_validator

Execution Stage Validator.

Validates execution stage implementations before registration.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .stage import Stage


class ExecutionStageValidator:
    """
    Validates Stage implementations.

    This validator checks only the structural contract of a stage.
    It never executes the stage.
    """

    def validate(
        self,
        stage: Stage,
    ) -> None:
        """
        Validate a Stage.

        Raises
        ------
        TypeError
            If the object is not a Stage.

        ValueError
            If the stage violates the execution contract.
        """

        if not isinstance(stage, Stage):
            raise TypeError(
                "stage must be a Stage."
            )

        name = stage.name

        if not isinstance(name, str):
            raise ValueError(
                "stage name must be a string."
            )

        if not name.strip():
            raise ValueError(
                "stage name cannot be empty."
            )

        execute = getattr(stage, "execute", None)

        if execute is None:
            raise ValueError(
                "stage must define execute()."
            )

        if not callable(execute):
            raise ValueError(
                "execute must be callable."
            )

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def is_valid(
        self,
        stage: Stage,
    ) -> bool:
        """
        Return True if the stage satisfies the execution contract.
        """

        try:

            self.validate(stage)

            return True

        except (TypeError, ValueError):

            return False
