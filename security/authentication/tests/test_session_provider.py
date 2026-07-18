# security/authentication/tests/test_session_provider.py
import pytest
from datetime import datetime, timezone, timedelta
from uuid import uuid4

from security.authentication.models import Identity, IdentityType, Session, Credentials, CredentialType
from security.authentication.session_provider import DefaultSessionProvider


def test_session_provider_requires_session():
    provider = DefaultSessionProvider()
    creds = Credentials(credential_type=CredentialType.PASSWORD, value="secret")
    assert provider.requires_session(creds) is True


def test_session_provider_create_get():
    provider = DefaultSessionProvider()
    identity = Identity(
        identity_id=uuid4(),
        username="alice",
        identity_type=IdentityType.USER,
    )
    session = provider.create_session(identity, ttl_seconds=60)
    assert session.identity_id == identity.identity_id
    assert session.expires_at > session.created_at
    assert (session.expires_at - session.created_at).seconds <= 60

    got = provider.get_session(str(session.session_id))
    assert got == session


def test_session_provider_refresh():
    provider = DefaultSessionProvider()
    identity = Identity(
        identity_id=uuid4(),
        username="alice",
        identity_type=IdentityType.USER,
    )
    session = provider.create_session(identity, ttl_seconds=60)
    old_expires = session.expires_at
    refreshed = provider.refresh_session(str(session.session_id))
    assert refreshed is not None
    assert refreshed.expires_at > old_expires
    stored = provider.get_session(str(session.session_id))
    assert stored.expires_at > old_expires


def test_session_provider_revoke():
    provider = DefaultSessionProvider()
    identity = Identity(
        identity_id=uuid4(),
        username="alice",
        identity_type=IdentityType.USER,
    )
    session = provider.create_session(identity)
    assert provider.revoke_session(str(session.session_id)) is True
    revoked = provider.get_session(str(session.session_id))
    assert revoked.is_revoked is True


def test_session_provider_refresh_expired():
    provider = DefaultSessionProvider()
    identity = Identity(
        identity_id=uuid4(),
        username="alice",
        identity_type=IdentityType.USER,
    )
    now = datetime.now(timezone.utc)
    # Create a session that is already expired
    expired_session = Session(
        session_id=uuid4(),
        identity_id=identity.identity_id,
        created_at=now - timedelta(seconds=10),
        expires_at=now - timedelta(seconds=5),
        last_activity=now - timedelta(seconds=10),
    )
    # Manually store it in the provider's internal dictionary
    provider._sessions[str(expired_session.session_id)] = expired_session

    refreshed = provider.refresh_session(str(expired_session.session_id))
    assert refreshed is None
