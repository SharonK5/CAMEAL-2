# security/services/policy/tests/test_policy_service.py
import pytest
from unittest.mock import Mock

from security.services.policy.default_policy_service import DefaultPolicyService
from security.services.base.security_context import SecurityContext
from security.services.base.lifecycle import ServiceState, HealthStatus
from security.policy.models import (
    PolicyRequest,
    PolicyResult,
    PolicyDecisionType,
    PolicyEvidence,
    Policy,
    PolicyRule,
    PolicyEffect,
    PolicyVersion,
)


@pytest.fixture
def mock_policy_engine():
    return Mock()


@pytest.fixture
def mock_policy_provider():
    return Mock()


@pytest.fixture
def mock_rule_provider():
    return Mock()


@pytest.fixture
def service(mock_policy_engine, mock_policy_provider, mock_rule_provider):
    mock_policy_engine.list_policies.return_value = ()
    return DefaultPolicyService(
        policy_engine=mock_policy_engine,
        policy_provider=mock_policy_provider,
        rule_provider=mock_rule_provider,
    )


def test_evaluate_allow(service, mock_policy_engine):
    rule = PolicyRule(name="r", effect=PolicyEffect.PERMIT)
    policy = Policy(name="p", rules=(rule,), version=PolicyVersion(1, 0, 0))
    domain_result = PolicyResult(
        decision=PolicyDecisionType.ALLOW,
        rationale="Policy allows",
        evidence=(PolicyEvidence(source="test", description="test"),),
        policies_applied=(policy,),
        rules_applied=(rule,),
    )
    mock_policy_engine.evaluate.return_value = domain_result

    context = SecurityContext(
        identity="alice",
        resource="/doc/1",
        operation="read",
    )

    decision = service.evaluate(context)

    assert decision.is_allowed is True
    assert decision.rationale == "Policy allows"
    assert decision.audit_metadata["policies_applied"] == ["p"]
    assert decision.audit_metadata["rules_applied"] == ["r"]
    mock_policy_engine.evaluate.assert_called_once()


def test_evaluate_deny(service, mock_policy_engine):
    domain_result = PolicyResult(
        decision=PolicyDecisionType.DENY,
        rationale="Policy denies",
        evidence=(PolicyEvidence(source="test", description="denied"),),
    )
    mock_policy_engine.evaluate.return_value = domain_result

    context = SecurityContext(
        identity="alice",
        resource="/doc/1",
        operation="write",
    )

    decision = service.evaluate(context)

    assert decision.is_denied is True
    assert decision.rationale == "Policy denies"


def test_evaluate_not_applicable(service, mock_policy_engine):
    domain_result = PolicyResult(
        decision=PolicyDecisionType.NOT_APPLICABLE,
        rationale="No policy applies",
        evidence=(PolicyEvidence(source="test", description="n/a"),),
    )
    mock_policy_engine.evaluate.return_value = domain_result

    context = SecurityContext(
        identity="alice",
        resource="/doc/1",
        operation="delete",
    )

    decision = service.evaluate(context)

    assert decision.is_abstained is True
    assert decision.rationale == "No policy applies"


def test_evaluate_evidence_default(service, mock_policy_engine):
    domain_result = PolicyResult(
        decision=PolicyDecisionType.ALLOW,
        rationale="Allowed",
    )
    mock_policy_engine.evaluate.return_value = domain_result

    context = SecurityContext(
        identity="alice",
        resource="/doc/1",
        operation="read",
    )

    decision = service.evaluate(context)
    assert len(decision.evidence) == 1
    assert decision.evidence[0].source == "policy_mapper"


def test_lifecycle(service):
    assert service.state == ServiceState.CREATED

    service.initialize()
    assert service.state == ServiceState.INITIALIZED

    service.validate()
    assert service.state == ServiceState.VALIDATED

    service.start()
    assert service.state == ServiceState.RUNNING

    service.shutdown()
    assert service.state == ServiceState.STOPPED

    service.dispose()
    assert service.state == ServiceState.DISPOSED


def test_health(service):
    mock_engine = Mock()
    mock_provider = Mock()
    mock_rule = Mock()

    mock_engine.health.return_value = True
    mock_provider.health.return_value = True
    mock_rule.health.return_value = True
    mock_engine.list_policies.return_value = ()

    service = DefaultPolicyService(
        policy_engine=mock_engine,
        policy_provider=mock_provider,
        rule_provider=mock_rule,
    )

    service.initialize()
    service.validate()
    service.start()

    assert service.health() == HealthStatus.HEALTHY

    mock_engine.health.return_value = False
    assert service.health() == HealthStatus.UNHEALTHY
