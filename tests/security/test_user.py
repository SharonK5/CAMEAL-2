from security.roles import Role
from security.user import User


def test_create_user():

    user = User(
        username="sharon",
        roles=frozenset({Role.SYSTEM_ADMIN})
    )

    assert user.username == "sharon"
    assert user.active
    assert user.has_role(Role.SYSTEM_ADMIN)


def test_missing_role():

    user = User(
        username="guest",
        roles=frozenset({Role.GUEST})
    )

    assert not user.has_role(Role.SYSTEM_ADMIN)
