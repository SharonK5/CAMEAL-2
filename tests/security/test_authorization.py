"""
===============================================================================
Unit tests for security.authorization
===============================================================================
"""

from security.authorization import Authorizer
from security.authorization_request import AuthorizationRequest
from security.permissions import Permission
from security.roles import Role
from security.user import User


def create_authorizer() -> Authorizer:
    """
    Create a simple RBAC configuration.
    """

    return Authorizer(
        role_permissions={
            Role.SYSTEM_ADMIN: {
                Permission.READ,
                Permission.WRITE,
                Permission.DELETE,
                Permission.REVIEW,          # replaced APPROVE with REVIEW
            },
            Role.ANALYST: {
                Permission.READ,
                Permission.WRITE,
            },
            Role.GUEST: {                   # formerly VIEWER
                Permission.READ,
            },
        }
    )


def test_admin_allowed():

    authorizer = create_authorizer()

    user = User(
        username="admin",
        roles=frozenset({Role.SYSTEM_ADMIN}),   # ADMIN → SYSTEM_ADMIN
    )

    request = AuthorizationRequest(
        user=user,
        permission=Permission.DELETE,
    )

    result = authorizer.authorize(request)

    assert result.allowed


def test_analyst_allowed():

    authorizer = create_authorizer()

    user = User(
        username="analyst",
        roles=frozenset({Role.ANALYST}),
    )

    request = AuthorizationRequest(
        user=user,
        permission=Permission.WRITE,
    )

    result = authorizer.authorize(request)

    assert result.allowed


def test_guest_denied():   # renamed from test_viewer_denied to match new role

    authorizer = create_authorizer()

    user = User(
        username="guest",   # was "viewer"
        roles=frozenset({Role.GUEST}),      # VIEWER → GUEST
    )

    request = AuthorizationRequest(
        user=user,
        permission=Permission.DELETE,
    )

    result = authorizer.authorize(request)

    assert not result.allowed


def test_multiple_roles_union_permissions():

    authorizer = create_authorizer()

    user = User(
        username="hybrid",
        roles=frozenset(
            {
                Role.GUEST,                # VIEWER → GUEST
                Role.ANALYST,
            }
        ),
    )

    request = AuthorizationRequest(
        user=user,
        permission=Permission.WRITE,
    )

    result = authorizer.authorize(request)

    assert result.allowed


def test_user_without_roles_denied():

    authorizer = create_authorizer()

    user = User(
        username="guest",
        roles=frozenset(),
    )

    request = AuthorizationRequest(
        user=user,
        permission=Permission.READ,
    )

    result = authorizer.authorize(request)

    assert not result.allowed


def test_duplicate_permissions_are_ignored():

    authorizer = create_authorizer()

    user = User(
        username="multi",
        roles=frozenset(
            {
                Role.SYSTEM_ADMIN,          # ADMIN → SYSTEM_ADMIN
                Role.ANALYST,
            }
        ),
    )

    request = AuthorizationRequest(
        user=user,
        permission=Permission.WRITE,
    )

    result = authorizer.authorize(request)

    assert result.allowed


def test_unknown_permission_denied():

    authorizer = create_authorizer()

    user = User(
        username="guest",   # was "viewer"
        roles=frozenset({Role.GUEST}),      # VIEWER → GUEST
    )

    request = AuthorizationRequest(
        user=user,
        permission=Permission.REVIEW,       # APPROVE → REVIEW
    )

    result = authorizer.authorize(request)

    assert not result.allowed
