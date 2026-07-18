# security/authentication/tests/test_identity_provider.py
import pytest
from uuid import uuid4
from security.authentication.models import Identity, IdentityType
from security.authentication.identity_provider import DefaultIdentityProvider


def test_identity_provider_add_get():
    provider = DefaultIdentityProvider()
    identity = Identity(
        identity_id=uuid4(),
        username="alice",
        identity_type=IdentityType.USER,
    )
    provider.add_identity(identity)

    got = provider.get_identity_by_username("alice")
    assert got == identity

    got2 = provider.get_identity(str(identity.identity_id))
    assert got2 == identity


def test_identity_provider_get_by_system_id():
    provider = DefaultIdentityProvider()
    identity = Identity(
        identity_id=uuid4(),
        username="system1",
        identity_type=IdentityType.SYSTEM,
        system_id="sys_123",
    )
    provider.add_identity(identity)
    got = provider.get_identity_by_system_id("sys_123")
    assert got == identity


def test_identity_provider_missing():
    provider = DefaultIdentityProvider()
    assert provider.get_identity_by_username("unknown") is None
    assert provider.get_identity_by_system_id("unknown") is None
