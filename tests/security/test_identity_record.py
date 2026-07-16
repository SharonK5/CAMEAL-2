from security.identity.identity_record import IdentityRecord
from security.identity.user import User


def test_create_identity():

    user = User(
        username="sharon",
        roles={"admin"},
    )

    identity = IdentityRecord(
        user=user,
        password_hash="hash",
    )

    assert identity.user.username == "sharon"

    assert identity.enabled

    assert identity.failed_attempts == 0


def test_defaults():

    user = User(
        username="john",
        roles=set(),
    )

    identity = IdentityRecord(
        user=user,
        password_hash="abc",
    )

    assert identity.locked is False

    assert identity.last_login is None
