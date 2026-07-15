"""
===============================================================================
Module: context.context_validator

Validation for governance contexts.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from typing import List

from .context import GovernanceContext


class ContextValidator:
    """
    Validates GovernanceContext objects.

    Validation never mutates the supplied context.
    """

    VALID_EXECUTION_MODES = {
        "Human",
        "AI",
        "Human-AI",
        "Autonomous",
    }

    def validate(
        self,
        context: GovernanceContext,
    ) -> list[str]:
        """
        Return a list of validation errors.

        Empty list means the context is valid.
        """

        errors: list[str] = []

        # ---------------------------------------------------
        # Spatial
        # ---------------------------------------------------

        spatial = context.spatial

        if spatial.latitude is not None:
            if not (-90 <= spatial.latitude <= 90):
                errors.append("Latitude must be between -90 and 90.")

        if spatial.longitude is not None:
            if not (-180 <= spatial.longitude <= 180):
                errors.append("Longitude must be between -180 and 180.")

        if spatial.bounding_box is not None:
            west, south, east, north = spatial.bounding_box

            if west >= east:
                errors.append("Bounding box west must be less than east.")

            if south >= north:
                errors.append("Bounding box south must be less than north.")

        # ---------------------------------------------------
        # Temporal
        # ---------------------------------------------------

        temporal = context.temporal

        if (
            temporal.start_time is not None
            and temporal.end_time is not None
            and temporal.start_time > temporal.end_time
        ):
            errors.append("Start time must precede end time.")

        if temporal.revision < 1:
            errors.append("Revision must be at least 1.")

        # ---------------------------------------------------
        # Operational
        # ---------------------------------------------------

        operational = context.operational

        if (
            operational.execution_mode is not None
            and operational.execution_mode
            not in self.VALID_EXECUTION_MODES
        ):
            errors.append(
                f"Invalid execution mode: {operational.execution_mode}"
            )

        return errors

    def is_valid(
        self,
        context: GovernanceContext,
    ) -> bool:
        """
        Convenience boolean validation.
        """
        return len(self.validate(context)) == 0
