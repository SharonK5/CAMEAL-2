# tests/security/test_risk_engine.py
"""
===============================================================================
Tests for security.risk_engine
===============================================================================
"""

from security.authorization_request import AuthorizationRequest
from context.context import GovernanceContext  # <-- changed from Context
from security.permissions import Permission
from security.policy import Policy
from security.risk_engine import RiskEngine
from security.risk_level import RiskLevel
from security.roles import Role
from security.user import User


def make_user():
    return User(
        username="alice",
        roles=frozenset({Role.RESEARCHER}),
    )


def make_context(**kwargs):
    """
    Build a GovernanceContext with sensible defaults.
    Any extra keyword arguments are placed into the metadata mapping.
    """
    # Pop 'metadata' if passed explicitly; otherwise start empty
    metadata = kwargs.pop("metadata", {})

    # Defaults for the dataclass fields
    defaults = {
        "jurisdiction": "Kenya",
        "metadata": metadata,
    }
    # Update with any remaining kwargs (these are dataclass fields)
    defaults.update(kwargs)

    return GovernanceContext(**defaults)


def make_policy():
    # Fixed: policy_id was removed, roles must be provided (empty frozenset is fine)
    return Policy(
        name="Default",
        description="Default policy",
        roles=frozenset(),                     # no roles needed for these tests
        permissions=frozenset({Permission.READ}),
        # enabled defaults to True, so we omit it
    )


def test_missing_policy_is_high():
    engine = RiskEngine()

    request = AuthorizationRequest(
        user=make_user(),
        permission=Permission.READ,
    )

    risk = engine.classify(
        request=request,
        policy=None,
        context=make_context(),
    )

    assert risk == RiskLevel.HIGH


def test_admin_is_critical():
    engine = RiskEngine()

    request = AuthorizationRequest(
        user=make_user(),
        permission=Permission.ADMIN,
    )

    risk = engine.classify(
        request=request,
        policy=make_policy(),
        context=make_context(),
    )

    assert risk == RiskLevel.CRITICAL


def test_govern_is_high():
    engine = RiskEngine()

    request = AuthorizationRequest(
        user=make_user(),
        permission=Permission.GOVERN,
    )

    risk = engine.classify(
        request=request,
        policy=make_policy(),
        context=make_context(),
    )

    assert risk == RiskLevel.HIGH


def test_high_sensitivity_is_high():
    engine = RiskEngine()

    request = AuthorizationRequest(
        user=make_user(),
        permission=Permission.READ,
    )

    # Sensitivity is now stored in metadata
    risk = engine.classify(
        request=request,
        policy=make_policy(),
        context=make_context(
            metadata={"sensitivity": "high"},
        ),
    )

    assert risk == RiskLevel.HIGH


def test_normal_request_is_low():
    engine = RiskEngine()

    request = AuthorizationRequest(
        user=make_user(),
        permission=Permission.READ,
    )

    risk = engine.classify(
        request=request,
        policy=make_policy(),
        context=make_context(),
    )

    assert risk == RiskLevel.LOW
