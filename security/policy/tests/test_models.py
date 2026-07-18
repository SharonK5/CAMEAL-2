# security/policy/tests/test_models.py
import pytest
from datetime import datetime, timezone
from uuid import UUID, uuid4

from security.core.exceptions import SecurityValidationError
from security.policy.models import (
    PolicyDecisionType,
    PolicyEffect,
    PolicyTargetType,
    PolicyStatus,
    PolicyType,
    PolicyVersion,
    PolicyCondition,
    PolicyRule,
    Policy,
    PolicyRequest,
    PolicyEvidence,
    PolicyResult,
)


# ------------------------------------------------------------------
# PolicyVersion
# ------------------------------------------------------------------

def test_policy_version_creation():
    v = PolicyVersion(1, 2, 3)
    assert v.major == 1
    assert v.minor == 2
    assert v.patch == 3
    assert str(v) == "1.2.3"


def test_policy_version_negative():
    with pytest.raises(SecurityValidationError, match="non-negative"):
        PolicyVersion(-1, 0, 0)


def test_policy_version_to_dict():
    v = PolicyVersion(1, 2, 3)
    d = v.to_dict()
    assert d == {"major": 1, "minor": 2, "patch": 3}


# ------------------------------------------------------------------
# PolicyCondition
# ------------------------------------------------------------------

def test_condition_creation():
    c = PolicyCondition(
        name="time_check",
        expression="time.now < 18:00",
        description="Afternoon only",
    )
    assert c.name == "time_check"
    assert c.expression == "time.now < 18:00"
    assert c.description == "Afternoon only"
    assert c.metadata == {}


def test_condition_name_empty():
    with pytest.raises(SecurityValidationError, match="name cannot be empty"):
        PolicyCondition(name="", expression="expr")


def test_condition_expression_empty():
    with pytest.raises(SecurityValidationError, match="expression cannot be empty"):
        PolicyCondition(name="c", expression="")


def test_condition_to_dict():
    c = PolicyCondition(name="c", expression="expr")
    d = c.to_dict()
    assert d["name"] == "c"
    assert d["expression"] == "expr"


# ------------------------------------------------------------------
# PolicyRule
# ------------------------------------------------------------------

def test_rule_creation():
    cond = PolicyCondition(name="c", expression="x")
    rule = PolicyRule(
        name="allow_read",
        effect=PolicyEffect.PERMIT,
        conditions=(cond,),
        priority=10,
    )
    assert isinstance(rule.rule_id, UUID)
    assert rule.name == "allow_read"
    assert rule.effect == PolicyEffect.PERMIT
    assert rule.conditions == (cond,)
    assert rule.priority == 10
    assert rule.metadata == {}


def test_rule_name_empty():
    with pytest.raises(SecurityValidationError, match="name cannot be empty"):
        PolicyRule(name="", effect=PolicyEffect.PERMIT)


def test_rule_invalid_effect():
    with pytest.raises(SecurityValidationError, match="effect must be a PolicyEffect"):
        PolicyRule(name="r", effect="PERMIT")  # type: ignore


def test_rule_invalid_condition():
    with pytest.raises(SecurityValidationError, match="All conditions must be PolicyCondition"):
        PolicyRule(
            name="r",
            effect=PolicyEffect.PERMIT,
            conditions=("not a condition",),  # type: ignore
        )


def test_rule_to_dict():
    rule = PolicyRule(name="r", effect=PolicyEffect.PERMIT)
    d = rule.to_dict()
    assert "rule_id" in d
    assert d["name"] == "r"
    assert d["effect"] == "PERMIT"


# ------------------------------------------------------------------
# Policy
# ------------------------------------------------------------------

def test_policy_creation():
    rule = PolicyRule(name="r", effect=PolicyEffect.PERMIT)
    version = PolicyVersion(1, 0, 0)
    policy = Policy(
        name="test_policy",
        policy_type=PolicyType.RULE,
        status=PolicyStatus.ACTIVE,
        version=version,
        rules=(rule,),
        target_type=PolicyTargetType.RESOURCE,
        target_value="/doc/*",
        description="Test policy",
    )
    assert isinstance(policy.policy_id, UUID)
    assert policy.name == "test_policy"
    assert policy.policy_type == PolicyType.RULE
    assert policy.status == PolicyStatus.ACTIVE
    assert policy.version == version
    assert policy.rules == (rule,)
    assert policy.target_type == PolicyTargetType.RESOURCE
    assert policy.target_value == "/doc/*"
    assert policy.description == "Test policy"


def test_policy_name_empty():
    with pytest.raises(SecurityValidationError, match="name cannot be empty"):
        Policy(name="", rules=())


def test_policy_invalid_type():
    with pytest.raises(SecurityValidationError, match="policy_type must be a PolicyType"):
        Policy(name="p", policy_type="RBAC")  # type: ignore


def test_policy_invalid_status():
    with pytest.raises(SecurityValidationError, match="status must be a PolicyStatus"):
        Policy(name="p", status="ACTIVE")  # type: ignore


def test_policy_invalid_version():
    with pytest.raises(SecurityValidationError, match="version must be a PolicyVersion"):
        Policy(name="p", version="1.0.0")  # type: ignore


def test_policy_invalid_rule():
    with pytest.raises(SecurityValidationError, match="All rules must be PolicyRule"):
        Policy(name="p", rules=("not a rule",))  # type: ignore


def test_policy_to_dict():
    rule = PolicyRule(name="r", effect=PolicyEffect.PERMIT)
    policy = Policy(name="test", rules=(rule,), version=PolicyVersion(1, 0, 0))
    d = policy.to_dict()
    assert "policy_id" in d
    assert d["name"] == "test"
    assert d["policy_type"] == "RULE"
    assert d["status"] == "ACTIVE"
    assert d["version"] == {"major": 1, "minor": 0, "patch": 0}
    assert len(d["rules"]) == 1


# ------------------------------------------------------------------
# PolicyRequest
# ------------------------------------------------------------------

def test_policy_request_creation():
    req = PolicyRequest(
        identity="alice",
        resource="/doc/1",
        operation="read",
        resource_type="document",
        resource_id="doc_123",
        permissions=("read",),
        roles=("user",),
        environment={"ip": "127.0.0.1"},
        metadata={"source": "web"},
    )
    assert req.identity == "alice"
    assert req.resource == "/doc/1"
    assert req.operation == "read"
    assert isinstance(req.request_id, UUID)
    assert req.resource_type == "document"
    assert req.resource_id == "doc_123"
    assert req.permissions == ("read",)
    assert req.roles == ("user",)
    assert req.environment["ip"] == "127.0.0.1"
    assert req.metadata["source"] == "web"


def test_policy_request_identity_empty():
    with pytest.raises(SecurityValidationError, match="Identity cannot be empty"):
        PolicyRequest(identity="", resource="/r", operation="op")


def test_policy_request_resource_empty():
    with pytest.raises(SecurityValidationError, match="Resource cannot be empty"):
        PolicyRequest(identity="i", resource="", operation="op")


def test_policy_request_operation_empty():
    with pytest.raises(SecurityValidationError, match="Operation cannot be empty"):
        PolicyRequest(identity="i", resource="/r", operation="")


def test_policy_request_invalid_request_id():
    with pytest.raises(SecurityValidationError, match="request_id must be a UUID"):
        PolicyRequest(
            identity="i",
            resource="/r",
            operation="op",
            request_id="not-uuid",  # type: ignore
        )


def test_policy_request_to_dict():
    req = PolicyRequest(identity="alice", resource="/r", operation="read")
    d = req.to_dict()
    assert d["identity"] == "alice"
    assert d["resource"] == "/r"
    assert d["operation"] == "read"
    assert "request_id" in d
    assert d["permissions"] == []
    assert d["environment"] == {}
    assert d["metadata"] == {}


# ------------------------------------------------------------------
# PolicyEvidence
# ------------------------------------------------------------------

def test_evidence_creation():
    ev = PolicyEvidence(
        source="test_engine",
        description="Test evidence",
        details={"key": "value"},
    )
    assert ev.source == "test_engine"
    assert ev.description == "Test evidence"
    assert ev.details["key"] == "value"
    assert ev.timestamp.tzinfo == timezone.utc


def test_evidence_source_empty():
    with pytest.raises(SecurityValidationError, match="source cannot be empty"):
        PolicyEvidence(source="", description="desc")


def test_evidence_description_empty():
    with pytest.raises(SecurityValidationError, match="description cannot be empty"):
        PolicyEvidence(source="s", description="")


def test_evidence_timestamp_naive():
    naive = datetime.now()
    with pytest.raises(SecurityValidationError, match="timestamp must be timezone-aware"):
        PolicyEvidence(source="s", description="d", timestamp=naive)


def test_evidence_to_dict():
    ev = PolicyEvidence(source="s", description="d")
    d = ev.to_dict()
    assert d["source"] == "s"
    assert d["description"] == "d"
    assert "timestamp" in d
    assert d["details"] == {}


# ------------------------------------------------------------------
# PolicyResult
# ------------------------------------------------------------------

def test_result_creation():
    rule = PolicyRule(name="r", effect=PolicyEffect.PERMIT)
    policy = Policy(name="p", rules=(rule,), version=PolicyVersion(1, 0, 0))
    evidence = PolicyEvidence(source="s", description="d")
    result = PolicyResult(
        decision=PolicyDecisionType.ALLOW,
        confidence=0.95,
        rationale="Allowed by policy",
        execution_time_ms=12.5,
        policies_applied=(policy,),
        rules_applied=(rule,),
        evidence=(evidence,),
    )
    assert result.decision == PolicyDecisionType.ALLOW
    assert result.confidence == 0.95
    assert result.rationale == "Allowed by policy"
    assert result.execution_time_ms == 12.5
    assert result.policies_applied == (policy,)
    assert result.rules_applied == (rule,)
    assert result.evidence == (evidence,)
    assert isinstance(result.request_id, UUID)
    assert result.created_at.tzinfo == timezone.utc


def test_result_invalid_decision():
    with pytest.raises(SecurityValidationError, match="decision must be a PolicyDecisionType"):
        PolicyResult(decision="ALLOW")  # type: ignore


def test_result_confidence_out_of_range():
    with pytest.raises(SecurityValidationError, match="confidence must be between 0 and 1"):
        PolicyResult(decision=PolicyDecisionType.ALLOW, confidence=1.5)


def test_result_invalid_request_id():
    with pytest.raises(SecurityValidationError, match="request_id must be a UUID"):
        PolicyResult(decision=PolicyDecisionType.ALLOW, request_id="not-uuid")  # type: ignore


def test_result_created_at_naive():
    naive = datetime.now()
    with pytest.raises(SecurityValidationError, match="created_at must be timezone-aware"):
        PolicyResult(decision=PolicyDecisionType.ALLOW, created_at=naive)


def test_result_invalid_policy():
    with pytest.raises(SecurityValidationError, match="All policies_applied must be Policy"):
        PolicyResult(
            decision=PolicyDecisionType.ALLOW,
            policies_applied=("not a policy",),  # type: ignore
        )


def test_result_invalid_rule():
    with pytest.raises(SecurityValidationError, match="All rules_applied must be PolicyRule"):
        PolicyResult(
            decision=PolicyDecisionType.ALLOW,
            rules_applied=("not a rule",),  # type: ignore
        )


def test_result_invalid_evidence():
    with pytest.raises(SecurityValidationError, match="All evidence items must be PolicyEvidence"):
        PolicyResult(
            decision=PolicyDecisionType.ALLOW,
            evidence=("not evidence",),  # type: ignore
        )


def test_result_properties():
    result = PolicyResult(decision=PolicyDecisionType.ALLOW)
    assert result.allowed is True
    assert result.denied is False
    assert result.not_applicable is False
    assert result.applicable is True

    result2 = PolicyResult(decision=PolicyDecisionType.NOT_APPLICABLE)
    assert result2.applicable is False


def test_result_names():
    rule = PolicyRule(name="rule1", effect=PolicyEffect.PERMIT)
    policy = Policy(name="policy1", rules=(rule,), version=PolicyVersion(1, 0, 0))
    result = PolicyResult(
        decision=PolicyDecisionType.ALLOW,
        policies_applied=(policy,),
        rules_applied=(rule,),
    )
    assert result.policy_names == frozenset({"policy1"})
    assert result.rule_names == frozenset({"rule1"})


def test_result_to_dict():
    rule = PolicyRule(name="r", effect=PolicyEffect.PERMIT)
    policy = Policy(name="p", rules=(rule,), version=PolicyVersion(1, 0, 0))
    evidence = PolicyEvidence(source="s", description="d")
    result = PolicyResult(
        decision=PolicyDecisionType.ALLOW,
        confidence=0.9,
        rationale="Test",
        execution_time_ms=5.0,
        policies_applied=(policy,),
        rules_applied=(rule,),
        evidence=(evidence,),
    )
    d = result.to_dict()
    assert d["decision"] == "ALLOW"
    assert d["confidence"] == 0.9
    assert d["rationale"] == "Test"
    assert d["execution_time_ms"] == 5.0
    assert len(d["policies_applied"]) == 1
    assert len(d["rules_applied"]) == 1
    assert len(d["evidence"]) == 1
    assert "request_id" in d
    assert "created_at" in d
