"""
Tests for the DecisionEngine.

These tests verify that the engine correctly orchestrates authorization
and policy evaluation, and returns an immutable Decision with all required
fields.
"""

import pytest
from unittest.mock import Mock

from security.authorization_request import AuthorizationRequest
from security.authorizer import Authorizer
from security.decision import Decision
from security.decision_engine import DecisionEngine, PolicyEvaluator
from security.policy import Policy
from security.permissions import Permission
from security.roles import Role
from security.user import User


def make_request(
    role: Role,
    permission: Permission,
    *,
    active: bool = True,
) -> AuthorizationRequest:
    """Helper to create a realistic AuthorizationRequest for tests."""
    user = User(
        username="alice",
        roles=frozenset({role}),
        active=active,
    )
    return AuthorizationRequest(
        user=user,
        permission=permission,
    )


class TestDecisionEngine:
    """Test suite for DecisionEngine."""

    def test_policy_allows_request(self) -> None:
        """Authorized request with matching policy => permitted True."""
        # Arrange
        request = make_request(Role.RESEARCHER, Permission.READ)
        authorizer = Mock(Authorizer)
        authorizer.authorize.return_value = Mock(success=True, message="Authorized")

        policy = Mock(spec=Policy)
        policy.policy_id = "POL-123"
        evaluator = Mock(PolicyEvaluator)
        evaluator.evaluate.return_value = policy

        engine = DecisionEngine(authorizer, evaluator)

        # Act
        decision = engine.evaluate(request)

        # Assert
        assert decision.permitted is True
        assert decision.reason == "Policy matched."
        assert decision.policy_id == "POL-123"
        assert decision.timestamp is not None

    def test_authorization_denied(self) -> None:
        """Authorization failure => permitted False with reason."""
        # Arrange
        request = make_request(Role.RESEARCHER, Permission.READ)
        authorizer = Mock(Authorizer)
        authorizer.authorize.return_value = Mock(
            success=False,
            message="User not found",
        )

        evaluator = Mock(PolicyEvaluator)  # not called
        engine = DecisionEngine(authorizer, evaluator)

        # Act
        decision = engine.evaluate(request)

        # Assert
        assert decision.permitted is False
        assert decision.reason == "User not found"
        assert decision.policy_id is None

        # Evaluator was never called
        evaluator.evaluate.assert_not_called()

    def test_no_policy(self) -> None:
        """Authorized but no matching policy => permitted False."""
        # Arrange
        request = make_request(Role.RESEARCHER, Permission.READ)
        authorizer = Mock(Authorizer)
        authorizer.authorize.return_value = Mock(success=True, message="Authorized")

        evaluator = Mock(PolicyEvaluator)
        evaluator.evaluate.return_value = None  # no policy

        engine = DecisionEngine(authorizer, evaluator)

        # Act
        decision = engine.evaluate(request)

        # Assert
        assert decision.permitted is False
        assert decision.reason == "No matching policy."
        assert decision.policy_id is None

    def test_policy_id_propagated(self) -> None:
        """When policy matches, its ID is propagated to the Decision."""
        # Arrange
        request = make_request(Role.RESEARCHER, Permission.READ)
        authorizer = Mock(Authorizer)
        authorizer.authorize.return_value = Mock(success=True, message="Authorized")

        policy = Mock(spec=Policy)
        policy.policy_id = "POL-789"
        evaluator = Mock(PolicyEvaluator)
        evaluator.evaluate.return_value = policy

        engine = DecisionEngine(authorizer, evaluator)

        # Act
        decision = engine.evaluate(request)

        # Assert
        assert decision.policy_id == "POL-789"

    def test_decision_contains_reason(self) -> None:
        """Every decision includes a human‑readable reason."""
        request = make_request(Role.RESEARCHER, Permission.READ)
        authorizer = Mock(Authorizer)
        authorizer.authorize.return_value = Mock(success=True, message="Authorized")

        evaluator = Mock(PolicyEvaluator)

        # Authorized + policy match
        policy = Mock(spec=Policy)
        policy.policy_id = "P-1"
        evaluator.evaluate.return_value = policy
        engine = DecisionEngine(authorizer, evaluator)
        decision = engine.evaluate(request)
        assert decision.reason == "Policy matched."

        # Authorized but no policy
        evaluator.evaluate.return_value = None
        decision2 = engine.evaluate(request)
        assert decision2.reason == "No matching policy."

        # Authorization denied
        authorizer.authorize.return_value = Mock(success=False, message="Denied")
        decision3 = engine.evaluate(request)
        assert decision3.reason == "Denied"

    def test_decision_timestamp_exists(self) -> None:
        """Decision always has a timestamp (set at construction)."""
        request = make_request(Role.RESEARCHER, Permission.READ)
        authorizer = Mock(Authorizer)
        authorizer.authorize.return_value = Mock(success=True, message="Authorized")

        policy = Mock(spec=Policy)
        policy.policy_id = "P-1"
        evaluator = Mock(PolicyEvaluator)
        evaluator.evaluate.return_value = policy

        engine = DecisionEngine(authorizer, evaluator)
        decision = engine.evaluate(request)
        assert decision.timestamp is not None

        # Even for denied decisions
        authorizer.authorize.return_value = Mock(success=False, message="Denied")
        decision2 = engine.evaluate(request)
        assert decision2.timestamp is not None

    def test_decision_immutable(self) -> None:
        """Decision objects are immutable; attributes cannot be reassigned."""
        request = make_request(Role.RESEARCHER, Permission.READ)
        authorizer = Mock(Authorizer)
        authorizer.authorize.return_value = Mock(success=True, message="Authorized")

        policy = Mock(spec=Policy)
        policy.policy_id = "P-1"
        evaluator = Mock(PolicyEvaluator)
        evaluator.evaluate.return_value = policy

        engine = DecisionEngine(authorizer, evaluator)
        decision = engine.evaluate(request)

        # Attempt to mutate – should raise AttributeError (frozen dataclass)
        with pytest.raises(AttributeError):
            decision.reason = "changed"  # type: ignore
        with pytest.raises(AttributeError):
            decision.policy_id = "NEW"  # type: ignore
        with pytest.raises(AttributeError):
            decision.timestamp = None  # type: ignore
