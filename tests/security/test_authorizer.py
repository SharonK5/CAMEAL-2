"""
===============================================================================
Integration tests for security.authorizer
===============================================================================
"""

from security.authorizer import Authorizer
from security.authorization_request import AuthorizationRequest
from security.permissions import Permission
from security.roles import Role
from security.user import User


def test_system_admin_allowed():

    user = User(
        username="admin",
        roles=frozenset({Role.SYSTEM_ADMIN}),
    )

    request = AuthorizationRequest(
        user=user,
        permission=Permission.DELETE,
    )

    result = Authorizer().authorize(request)

    assert result.success


def test_researcher_allowed():

    user = User(
        username="researcher",
        roles=frozenset({Role.RESEARCHER}),
    )

    request = AuthorizationRequest(
        user=user,
        permission=Permission.ANALYZE,
    )

    result = Authorizer().authorize(request)

    assert result.success


def test_guest_denied_delete():

    user = User(
        username="guest",
        roles=frozenset({Role.GUEST}),
    )

    request = AuthorizationRequest(
        user=user,
        permission=Permission.DELETE,
    )

    result = Authorizer().authorize(request)

    assert not result.success


def test_api_client_denied_configure():

    user = User(
        username="api",
        roles=frozenset({Role.API_CLIENT}),
    )

    request = AuthorizationRequest(
        user=user,
        permission=Permission.CONFIGURE,
    )

    result = Authorizer().authorize(request)

    assert not result.success


def test_inactive_user_denied():

    user = User(
        username="disabled",
        roles=frozenset({Role.SYSTEM_ADMIN}),
        active=False,
    )

    request = AuthorizationRequest(
        user=user,
        permission=Permission.ADMIN,
    )

    result = Authorizer().authorize(request)

    assert not result.success
