from security.identity.identity_record import IdentityRecord
from security.identity.memory_provider import MemoryIdentityProvider
from security.identity.user import User


def test_save_identity():

    provider = MemoryIdentityProvider()

    identity = IdentityRecord(
        user=User(
            username="sharon",
            roles={"admin"},
        ),
        password_hash="hash",
    )

    provider.save(identity)

    assert provider.exists("sharon")


def test_get_identity():

    provider = MemoryIdentityProvider()

    identity = IdentityRecord(
        user=User(
            username="john",
            roles=set(),
        ),
        password_hash="hash",
    )

    provider.save(identity)

    assert provider.get("john") == identity


def test_unknown_user():

    provider = MemoryIdentityProvider()

    assert provider.get("missing") is None


def test_exists_false():

    provider = MemoryIdentityProvider()

    assert not provider.exists("nobody")
