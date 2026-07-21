# kernel/events/validator.py
"""
Event validator.

Validates event structure, content, and schema.
"""

from typing import Any, Dict, Optional

from .event import Event
from .exceptions import EventValidationError


class EventValidator:
    """
    Validates event structure and content.
    """

    def validate(self, event: Event) -> None:
        """
        Validate an event.

        Checks:
            - Event type is non-empty.
            - Payload is a dictionary.
            - Metadata is a dictionary.
            - Provenance is a dictionary.
            - Timestamp is timezone-aware.
        """
        if not event.event_type:
            raise EventValidationError("Event type cannot be empty")
        if not isinstance(event.payload, dict):
            raise EventValidationError("Event payload must be a dictionary")
        if not isinstance(event.metadata, dict):
            raise EventValidationError("Event metadata must be a dictionary")
        if not isinstance(event.provenance, dict):
            raise EventValidationError("Event provenance must be a dictionary")
        if event.timestamp.tzinfo is None:
            raise EventValidationError("Event timestamp must be timezone-aware")

        # Validate schema version format (optional)
        if not event.schema_version:
            raise EventValidationError("Event schema version cannot be empty")

    def validate_payload(self, payload: Dict[str, Any], schema: Dict[str, type]) -> None:
        """
        Validate event payload against a schema.

        Args:
            payload: The payload to validate.
            schema: A dict mapping field names to expected types.

        Raises:
            EventValidationError: If validation fails.
        """
        for field, expected_type in schema.items():
            if field not in payload:
                raise EventValidationError(f"Missing required field: {field}")
            if not isinstance(payload[field], expected_type):
                raise EventValidationError(
                    f"Field '{field}' expected {expected_type.__name__}, got {type(payload[field]).__name__}"
                )

    def validate_schema_version(self, version: str) -> bool:
        """
        Validate a schema version string.

        Returns True if valid, False otherwise.
        """
        import re
        return bool(re.match(r"^\d+\.\d+$", version))
