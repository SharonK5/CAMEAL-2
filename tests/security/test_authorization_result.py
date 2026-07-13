"""
===============================================================================
Unit tests for security.authorization_result
===============================================================================
"""

from security.authorization_result import AuthorizationResult


def test_success():
    """Test that a successful authorization result can be created with allowed=True."""
    result = AuthorizationResult(
        allowed=True,
        message="Allowed",
    )
    assert result.allowed is True
    assert result.message == "Allowed"


def test_failure():
    """Test that a failed authorization result can be created with allowed=False."""
    result = AuthorizationResult(
        allowed=False,
        message="Denied",
    )
    assert result.allowed is False
    assert result.message == "Denied"
