"""
===============================================================================
Integration tests for security.authenticator
===============================================================================
"""

from datetime import datetime, UTC

from security.identity.authentication_request import AuthenticationRequest
from security.identity.authenticator import Authenticator
from security.integrity.hashing import HashingService
from security.identity.identity_record import IdentityRecord
from security.identity.memory_provider import MemoryIdentityProvider
from security.identity.user import User


def create_provider():
    """
    Create an in-memory provider populated with one test user.
    """
    provider = MemoryIdentityProvider()
    hashing = HashingService()

    user = User(username="sharon")
    identity = IdentityRecord(
        user=user,
        password_hash=hashing.hash_password("secret123"),
    )
    provider.save(identity)

    return provider, hashing


def test_authenticate_success():
    provider, hashing = create_provider()

    authenticator = Authenticator(
        provider=provider,
        hashing=hashing,
    )

    request = AuthenticationRequest(
        username="sharon",
        password="secret123",
    )

    result = authenticator.authenticate(request)

    # Check behaviour, not hard‑coded messages.
    assert result.success
    assert result.user is not None
    assert result.user.username == "sharon"

    identity = provider.get("sharon")
    assert identity.failed_attempts == 0
    # last_login is tested in its own dedicated test


def test_authenticate_invalid_password():
    provider, hashing = create_provider()

    identity_before = provider.get("sharon")
    before_login = identity_before.last_login

    authenticator = Authenticator(
        provider,
        hashing,
    )

    request = AuthenticationRequest(
        username="sharon",
        password="wrong-password",
    )

    result = authenticator.authenticate(request)

    assert not result.success
    assert result.user is None

    # State changes: failed_attempts increments, but last_login stays unchanged
    identity_after = provider.get("sharon")
    assert identity_after.failed_attempts == 1
    assert identity_after.last_login == before_login


def test_unknown_user():
    provider, hashing = create_provider()

    authenticator = Authenticator(
        provider,
        hashing,
    )

    request = AuthenticationRequest(
        username="unknown",
        password="password",
    )

    result = authenticator.authenticate(request)

    assert not result.success
    assert result.user is None


def test_disabled_account():
    provider, hashing = create_provider()

    identity = provider.get("sharon")
    identity.enabled = False
    provider.save(identity)

    authenticator = Authenticator(
        provider,
        hashing,
    )

    request = AuthenticationRequest(
        username="sharon",
        password="secret123",
    )

    result = authenticator.authenticate(request)

    assert not result.success
    # Keep message assertion if it's part of the API
    assert result.message == "Account disabled."


def test_locked_account():
    provider, hashing = create_provider()

    identity = provider.get("sharon")
    identity.locked = True
    provider.save(identity)

    authenticator = Authenticator(
        provider,
        hashing,
    )

    request = AuthenticationRequest(
        username="sharon",
        password="secret123",
    )

    result = authenticator.authenticate(request)

    assert not result.success
    assert result.message == "Account locked."


def test_failed_attempts_reset_after_success():
    provider, hashing = create_provider()

    identity = provider.get("sharon")
    identity.failed_attempts = 4
    provider.save(identity)

    authenticator = Authenticator(
        provider,
        hashing,
    )

    request = AuthenticationRequest(
        username="sharon",
        password="secret123",
    )

    result = authenticator.authenticate(request)

    assert result.success

    identity = provider.get("sharon")
    assert identity.failed_attempts == 0


def test_last_login_updated():
    """
    Verify that last_login is updated to a time >= the authentication time.
    Uses timezone-aware UTC to match the security package.
    """
    provider, hashing = create_provider()

    # Record time just before authentication (UTC)
    before = datetime.now(UTC)

    authenticator = Authenticator(
        provider,
        hashing,
    )

    request = AuthenticationRequest(
        username="sharon",
        password="secret123",
    )

    authenticator.authenticate(request)

    identity = provider.get("sharon")
    after_login = identity.last_login

    assert after_login is not None
    assert after_login >= before   # proves it was written during this call


def test_account_locks_after_max_failures():
    """
    Security-critical: repeated failed authentication attempts lock the account.
    Assumes max_failures = 5 (adjust if different in your implementation).
    """
    provider, hashing = create_provider()

    authenticator = Authenticator(
        provider,
        hashing,
    )

    request = AuthenticationRequest(
        username="sharon",
        password="wrong",
    )

    # Simulate 5 failed attempts
    for _ in range(5):
        authenticator.authenticate(request)

    identity = provider.get("sharon")
    assert identity.locked is True
