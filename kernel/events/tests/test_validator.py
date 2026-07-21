# kernel/events/tests/test_validator.py
import pytest
from datetime import datetime, timezone

from kernel.events.validator import EventValidator
from kernel.events.event import Event
from kernel.events.exceptions import EventValidationError


class TestValidator:
    def test_validate_valid_event(self):
        validator = EventValidator()
        event = Event(event_type="test")
        validator.validate(event)  # Should not raise

    def test_validate_empty_type(self):
        validator = EventValidator()
        with pytest.raises(EventValidationError, match="Event type cannot be empty"):
            validator.validate(Event(event_type=""))

    def test_validate_payload_schema(self):
        validator = EventValidator()
        payload = {"name": "alice", "age": 30}
        schema = {"name": str, "age": int}
        validator.validate_payload(payload, schema)  # Should not raise

    def test_validate_payload_missing_field(self):
        validator = EventValidator()
        payload = {"name": "alice"}
        schema = {"name": str, "age": int}
        with pytest.raises(EventValidationError, match="Missing required field"):
            validator.validate_payload(payload, schema)
