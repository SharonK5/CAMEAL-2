# security/services/authentication/tests/test_authentication_service.py
import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime, timezone

from security.services.authentication.default_authentication_service import (
    DefaultAuthenticationService,
)
from security.services.base.security_context import SecurityContext
from security.services.base.security_result import SecurityResult
from security.authentication.models import (
    Identity,
    IdentityType,
    AuthenticationResult,
    Session,
    Credentials,
    CredentialType,
)


@pytest.fixture
def mock_authenticator():
    return Mock()


@pytest.fixture
def mock_identity_provider():
    return Mock()


@pytest.fixture
def mock_session_provider():
    return Mock()


@pytest.fixture
def mock_audit_logger():
    return Mock()


@pytest.fixture
def service(
    mock_authenticator,
    mock_identity_provider,
    mock_session_provider,
    mock_audit_logger,
) -> DefaultAuthenticationService:
    return DefaultAuthenticationService(
        authenticator=mock_authenticator,
        identity_provider=mock_identity_provider,
        session_provider=mock_session_provider,
        audit_logger=mock_audit_logger,
    )


def test_authenticate_success(service, mock_authenticator, mock_session_provider, mock_audit_logger):
    identity = Identity(
        identity_id=uuid4(),
        username="alice",
        identity_type=IdentityType.USER,
    )
    domain_result = AuthenticationResult(
        success=True,
        identity=identity,
        message="Authenticated",
    )
    mock_authenticator.authenticate.return_value = domain_result
    mock_session_provider.requires_session.return_value = True
    session = Session(
        session_id=uuid4(),
        identity_id=identity.identity_id,
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc),
        last_activity=datetime.now(timezone.utc),
    )
    mock_session_provider.create_session.return_value = session

    context = SecurityContext(
        identity="alice",
        resource="/",
        operation="read",
        metadata={"credential_type": "password", "credential_value": "secret"},
    )

    result = service.authenticate(context)

    assert result.success is True
    assert result.message == "Authenticated"
    assert result.data == domain_result
    assert result.details["session_id"] == str(session.session_id)

    mock_authenticator.authenticate.assert_called_once()
    mock_audit_logger.log_authentication.assert_called_once()
    mock_session_provider.create_session.assert_called_once_with(identity)


def test_authenticate_failure(service, mock_authenticator, mock_session_provider, mock_audit_logger):
    domain_result = AuthenticationResult(
        success=False,
        message="Invalid password",
        error_code="INVALID_PASSWORD",
    )
    mock_authenticator.authenticate.return_value = domain_result

    context = SecurityContext(
        identity="alice",
        resource="/",
        operation="read",
        metadata={"credential_type": "password", "credential_value": "wrong"},
    )

    result = service.authenticate(context)

    assert result.success is False
    assert result.message == "Invalid password"
    assert result.error_code == "INVALID_PASSWORD"

    mock_audit_logger.log_authentication.assert_called_once()
    mock_session_provider.create_session.assert_not_called()


def test_authenticate_user_success(service, mock_authenticator, mock_session_provider, mock_audit_logger):
    identity = Identity(
        identity_id=uuid4(),
        username="alice",
        identity_type=IdentityType.USER,
    )
    domain_result = AuthenticationResult(
        success=True,
        identity=identity,
        message="User authenticated",
    )
    mock_authenticator.authenticate.return_value = domain_result
    mock_session_provider.requires_session.return_value = True
    session = Session(
        session_id=uuid4(),
        identity_id=identity.identity_id,
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc),
        last_activity=datetime.now(timezone.utc),
    )
    mock_session_provider.create_session.return_value = session

    result = service.authenticate_user("alice", "password")

    assert result.success is True
    assert result.message == "User authenticated"
    assert result.data == domain_result

    call_args = mock_authenticator.authenticate.call_args[0][0]
    assert call_args.credential_type == CredentialType.PASSWORD
    assert call_args.value == "password"


def test_verify_identity_found(service, mock_identity_provider):
    identity = Identity(
        identity_id=uuid4(),
        username="alice",
        identity_type=IdentityType.USER,
    )
    mock_identity_provider.get_identity_by_username.return_value = identity

    result = service.verify_identity("alice")

    assert result.success is True
    assert result.data == identity
    assert result.message == "Identity verified."


def test_verify_identity_not_found(service, mock_identity_provider):
    mock_identity_provider.get_identity_by_username.return_value = None
    mock_identity_provider.get_identity_by_system_id.return_value = None

    result = service.verify_identity("unknown")

    assert result.success is False
    assert result.error_code == "IDENTITY_NOT_FOUND"
    assert "unknown" in result.message


def test_logout_success(service, mock_session_provider):
    mock_session_provider.revoke_session.return_value = True
    result = service.logout("session123")
    assert result.success is True
    assert result.message == "Session terminated."


def test_logout_failure(service, mock_session_provider):
    mock_session_provider.revoke_session.return_value = False
    result = service.logout("session123")
    assert result.success is False
    assert result.error_code == "SESSION_NOT_FOUND"


def test_refresh_session_success(service, mock_session_provider):
    session = Session(
        session_id=uuid4(),
        identity_id=uuid4(),
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc),
        last_activity=datetime.now(timezone.utc),
    )
    mock_session_provider.refresh_session.return_value = session

    result = service.refresh_session("session123")
    assert result.success is True
    assert result.data["session_id"] == str(session.session_id)


def test_refresh_session_failure(service, mock_session_provider):
    mock_session_provider.refresh_session.return_value = None
    result = service.refresh_session("session123")
    assert result.success is False
    assert result.error_code == "SESSION_INVALID"
