# security/authentication/tests/test_authenticator.py
import pytest
from security.authentication.models import Credentials, CredentialType
from security.authentication.authenticator import DefaultAuthenticator

# ... tests


def test_default_authenticator_password_success():
    auth = DefaultAuthenticator()
    creds = Credentials(
        credential_type=CredentialType.PASSWORD,
        value="password",
    )
    result = auth.authenticate(creds)
    assert result.success is True
    assert result.identity is not None
    assert result.identity.username == "testuser"
    assert result.message == "Authentication successful (stub)."


def test_default_authenticator_password_short_fail():
    auth = DefaultAuthenticator()
    creds = Credentials(
        credential_type=CredentialType.PASSWORD,
        value="ab",
    )
    result = auth.authenticate(creds)
    assert result.success is False
    assert result.identity is None
    assert result.error_code == "INVALID_CREDENTIALS"


def test_default_authenticator_other_types():
    auth = DefaultAuthenticator()
    creds = Credentials(
        credential_type=CredentialType.API_KEY,
        value="any_key",
    )
    result = auth.authenticate(creds)
    assert result.success is True
    assert result.identity is not None
    assert result.identity.username == "system"
