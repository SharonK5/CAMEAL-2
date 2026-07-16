"""
===============================================================================
Unit tests for security.policy
===============================================================================
"""

from security.identity.permissions import Permission
from security.governance.policy import Policy
from security.identity.roles import Role


def test_policy_creation():

    policy = Policy(
        name="Research Policy",
        roles=frozenset({Role.RESEARCHER}),
        permissions=frozenset({
            Permission.READ,
            Permission.QUERY,
            Permission.ANALYZE,
        }),
        description="Research access.",
    )

    assert policy.name == "Research Policy"
    assert policy.enabled


def test_allows_role():

    policy = Policy(
        name="Research",
        roles=frozenset({Role.RESEARCHER}),
        permissions=frozenset(),
    )

    assert policy.allows_role(Role.RESEARCHER)
    assert not policy.allows_role(Role.GUEST)


def test_allows_permission():

    policy = Policy(
        name="Research",
        roles=frozenset(),
        permissions=frozenset({
            Permission.ANALYZE,
        }),
    )

    assert policy.allows_permission(
        Permission.ANALYZE
    )

    assert not policy.allows_permission(
        Permission.DELETE
    )


def test_disabled_policy():

    policy = Policy(
        name="Disabled",
        roles=frozenset({Role.SYSTEM_ADMIN}),
        permissions=frozenset({Permission.ADMIN}),
        enabled=False,
    )

    assert not policy.enabled
