import pytest

from kernel.request import Request
from kernel.validators import RequestValidator


def test_valid_request():
    """A valid request should not raise an exception."""

    validator = RequestValidator()

    request = Request(
        action="query",
        payload={},
    )

    validator.validate(request)


def test_invalid_action():
    """An empty action should raise ValueError."""

    validator = RequestValidator()

    request = Request(
        action="",
        payload={},
    )

    with pytest.raises(ValueError):
        validator.validate(request)
