# security/policy/tests/test_policy_engine.py
import pytest
from uuid import uuid4

from security.policy.default_policy_engine import DefaultPolicyEngine
from security.policy.models import PolicyRequest, PolicyDecisionType, Policy, PolicyRule, PolicyEffect, PolicyVersion


def test_default_policy_engine_evaluate():
    engine = DefaultPolicyEngine()
    request = PolicyRequest(
        identity="alice",
        resource="/doc/1",
        operation="read",
    )
    result = engine.evaluate(request)

    assert result.decision == PolicyDecisionType.ALLOW
    assert result.confidence == 1.0
    assert result.rationale == "Policy allowed by default engine."
    assert len(result.evidence) == 1
    evidence = result.evidence[0]
    assert evidence.source == "DefaultPolicyEngine"
    assert evidence.details["engine_version"] == "1.0.0"
    assert evidence.details["request_identity"] == "alice"
    assert evidence.details["request_resource"] == "/doc/1"
    assert evidence.details["request_operation"] == "read"


def test_default_policy_engine_load_list_get():
    engine = DefaultPolicyEngine()
    rule = PolicyRule(name="rule1", effect=PolicyEffect.PERMIT)
    policy = Policy(name="policy1", rules=(rule,), version=PolicyVersion(1, 0, 0))
    engine.load((policy,))

    policies = engine.list_policies()
    assert len(policies) == 1
    assert policies[0].name == "policy1"

    got = engine.get_policy(str(policy.policy_id))
    assert got == policy

    with pytest.raises(ValueError, match="not found"):
        engine.get_policy("not-exist")


def test_default_policy_engine_health():
    engine = DefaultPolicyEngine()
    assert engine.health() is True


def test_default_policy_engine_reload():
    engine = DefaultPolicyEngine()
    # Should not raise
    engine.reload()


def test_default_policy_engine_clear_cache():
    engine = DefaultPolicyEngine()
    # Should not raise
    engine.clear_cache()
