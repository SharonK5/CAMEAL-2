"""
===============================================================================
Unit tests for security.policy_engine
===============================================================================
"""

from security.permissions import Permission
from security.policy import Policy
from security.policy_engine import PolicyEngine
from security.roles import Role


def create_policy():

    return Policy(
        name="Research",
        roles=frozenset({
            Role.RESEARCHER,
        }),
        permissions=frozenset({
            Permission.READ,
            Permission.QUERY,
            Permission.ANALYZE,
        }),
    )


def test_policy_allows_permission():

    engine = PolicyEngine()

    assert engine.evaluate(
        create_policy(),
        Role.RESEARCHER,
        Permission.ANALYZE,
    )


def test_wrong_role_denied():

    engine = PolicyEngine()

    assert not engine.evaluate(
        create_policy(),
        Role.GUEST,
        Permission.ANALYZE,
    )


def test_wrong_permission_denied():

    engine = PolicyEngine()

    assert not engine.evaluate(
        create_policy(),
        Role.RESEARCHER,
        Permission.DELETE,
    )


def test_disabled_policy_denied():

    engine = PolicyEngine()

    policy = Policy(
        name="Disabled",
        roles=frozenset({
            Role.SYSTEM_ADMIN,
        }),
        permissions=frozenset({
            Permission.ADMIN,
        }),
        enabled=False,
    )

    assert not engine.evaluate(
        policy,
        Role.SYSTEM_ADMIN,
        Permission.ADMIN,
    )


def test_multiple_roles_supported():

    engine = PolicyEngine()

    policy = Policy(
        name="Operations",
        roles=frozenset({
            Role.OPERATOR,
            Role.SYSTEM_ADMIN,
        }),
        permissions=frozenset({
            Permission.WRITE,
        }),
    )

    assert engine.evaluate(
        policy,
        Role.OPERATOR,
        Permission.WRITE,
    )

    assert engine.evaluate(
        policy,
        Role.SYSTEM_ADMIN,
        Permission.WRITE,
    )
