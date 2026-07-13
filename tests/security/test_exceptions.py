import pytest

from security.exceptions import (
    AuthenticationError,
    AuthorizationError,
    InvalidCredentialsError,
    SecurityError,
)


def test_exception_hierarchy():

    assert issubclass(AuthenticationError, SecurityError)

    assert issubclass(AuthorizationError, SecurityError)

    assert issubclass(
        InvalidCredentialsError,
        AuthenticationError,
    )


def test_raise_security_exception():

    with pytest.raises(AuthenticationError):

        raise AuthenticationError("Authentication failed")
