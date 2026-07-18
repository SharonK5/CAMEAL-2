# security/authorization/tests/test_models.py
"""
Tests for authorization domain models.
"""

import pytest
from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid4

from security.core.exceptions import SecurityValidationError
from security.authorization.models import (
    AuthorizationDecisionType,
    AuthorizationReasonCode,
    ResourceType,
    Permission,
    Role,
    Constraint,
    Obligation,
    AuthorizationEvidence,
    AuthorizationRequest,
    AuthorizationResult,
)


# ------------------------------------------------------------------
# Permission tests
# ------------------------------------------------------------------

def test_permission_creation():
    perm = Permission(
        name="read",
        description="Read permission",
        resource_type=ResourceType.DOCUMENT,
        metadata={"scope": "global"},
    )
    assert perm.name == "read"
    assert perm.description == "Read permission"
    assert perm.resource_type == ResourceType.DOCUMENT
    assert perm.metadata["scope"] == "global"


def test_permission_name_empty():
    with pytest.raises(SecurityValidationError, match="Permission name cannot be empty"):
        Permission(name="")


def test_permission_invalid_resource_type():
    with pytest.raises(SecurityValidationError, match="resource_type must be a ResourceType"):
        Permission(name="read", resource_type="DOCUMENT")  # type: ignore


def test_permission_to_dict():
    perm = Permission(name="read", description="Read")
    d = perm.to_dict()
    assert d["name"] == "read"
    assert d["description"] == "Read"
    assert d["resource_type"] is None
    assert d["metadata"] == {}


# ------------------------------------------------------------------
# Role tests
# ------------------------------------------------------------------

def test_role_creation():
    p = Permission(name="read")
    role = Role(
        name="admin",
        permissions=(p,),
        description="Admin role",
        metadata={"level": 1},
    )
    assert role.name == "admin"
    assert role.permissions == (p,)
    assert role.has_permission("read") is True
    assert role.has_permission("write") is False
    assert role.permission_names == frozenset({"read"})


def test_role_name_empty():
    with pytest.raises(SecurityValidationError, match="Role name cannot be empty"):
        Role(name="")


def test_role_invalid_permission():
    with pytest.raises(SecurityValidationError, match="All permissions must be Permission instances"):
        Role(name="admin", permissions=("not a permission",))  # type: ignore


def test_role_to_dict():
    p = Permission(name="read")
    role = Role(name="admin", permissions=(p,))
    d = role.to_dict()
    assert d["name"] == "admin"
    assert len(d["permissions"]) == 1
    assert d["permissions"][0]["name"] == "read"


# ------------------------------------------------------------------
# Constraint tests
# ------------------------------------------------------------------

def test_constraint_creation():
    constr = Constraint(
        name="owner_match",
        expression="resource.owner == identity",
        description="Owner must match identity",
    )
    assert constr.name == "owner_match"
    assert constr.expression == "resource.owner == identity"
    assert constr.description == "Owner must match identity"


def test_constraint_name_empty():
    with pytest.raises(SecurityValidationError, match="Constraint name cannot be empty"):
        Constraint(name="", expression="expr")


def test_constraint_expression_empty():
    with pytest.raises(SecurityValidationError, match="Constraint expression cannot be empty"):
        Constraint(name="c", expression="")


# ------------------------------------------------------------------
# Obligation tests
# ------------------------------------------------------------------

def test_obligation_creation():
    ob = Obligation(
        name="audit_log",
        action="log",
        parameters={"level": "info"},
        metadata={"source": "policy"},
    )
    assert ob.name == "audit_log"
    assert ob.action == "log"
    assert ob.parameters["level"] == "info"
    assert ob.metadata["source"] == "policy"


def test_obligation_name_empty():
    with pytest.raises(SecurityValidationError, match="Obligation name cannot be empty"):
        Obligation(name="", action="log")


def test_obligation_action_empty():
    with pytest.raises(SecurityValidationError, match="Obligation action cannot be empty"):
        Obligation(name="audit", action="")


# ------------------------------------------------------------------
# AuthorizationEvidence tests
# ------------------------------------------------------------------

def test_evidence_creation():
    ev = AuthorizationEvidence(
        source="test_engine",
        description="Test evidence",
        attributes={"key": "value"},
    )
    assert ev.source == "test_engine"
    assert ev.description == "Test evidence"
    assert ev.attributes["key"] == "value"
    assert ev.timestamp.tzinfo == timezone.utc


def test_evidence_source_empty():
    with pytest.raises(SecurityValidationError, match="Evidence source cannot be empty"):
        AuthorizationEvidence(source="", description="desc")


def test_evidence_description_empty():
    with pytest.raises(SecurityValidationError, match="Evidence description cannot be empty"):
        AuthorizationEvidence(source="s", description="")


def test_evidence_timestamp_naive():
    naive = datetime.now()
    with pytest.raises(SecurityValidationError, match="Evidence timestamp must be timezone-aware"):
        AuthorizationEvidence(source="s", description="d", timestamp=naive)


# ------------------------------------------------------------------
# AuthorizationRequest tests
# ------------------------------------------------------------------

def test_request_creation():
    req = AuthorizationRequest(
        identity="alice",
        resource="/doc/1",
        operation="read",
        resource_type=ResourceType.DOCUMENT,
        resource_id="doc_123",
        permissions=("read",),
        roles=("user",),
        metadata={"ip": "127.0.0.1"},
    )
    assert req.identity == "alice"
    assert req.resource == "/doc/1"
    assert req.operation == "read"
    assert req.resource_type == ResourceType.DOCUMENT
    assert req.resource_id == "doc_123"
    assert req.permissions == ("read",)
    assert req.roles == ("user",)
    assert req.metadata["ip"] == "127.0.0.1"
    assert isinstance(req.request_id, UUID)


def test_request_identity_empty():
    with pytest.raises(SecurityValidationError, match="Identity cannot be empty"):
        AuthorizationRequest(identity="", resource="/r", operation="op")


def test_request_resource_empty():
    with pytest.raises(SecurityValidationError, match="Resource cannot be empty"):
        AuthorizationRequest(identity="i", resource="", operation="op")


def test_request_operation_empty():
    with pytest.raises(SecurityValidationError, match="Operation cannot be empty"):
        AuthorizationRequest(identity="i", resource="/r", operation="")


def test_request_invalid_resource_type():
    with pytest.raises(SecurityValidationError, match="resource_type must be a ResourceType"):
        AuthorizationRequest(
            identity="i", resource="/r", operation="op",
            resource_type="DOCUMENT"  # type: ignore
        )


def test_request_request_id_invalid():
    with pytest.raises(SecurityValidationError, match="request_id must be a UUID"):
        AuthorizationRequest(
            identity="i", resource="/r", operation="op",
            request_id="not-a-uuid"  # type: ignore
        )


def test_request_to_dict():
    req = AuthorizationRequest(
        identity="alice",
        resource="/doc/1",
        operation="read",
        permissions=("read",),
    )
    d = req.to_dict()
    assert d["identity"] == "alice"
    assert d["resource"] == "/doc/1"
    assert d["operation"] == "read"
    assert "request_id" in d
    assert d["permissions"] == ["read"]
    assert d["roles"] == []


# ------------------------------------------------------------------
# AuthorizationResult tests
# ------------------------------------------------------------------

def test_result_creation():
    perm = Permission(name="read")
    role = Role(name="user")
    constr = Constraint(name="c", expression="x")
    ob = Obligation(name="o", action="log")
    ev = AuthorizationEvidence(source="test", description="desc")

    result = AuthorizationResult(
        decision=AuthorizationDecisionType.ALLOW,
        confidence=0.95,
        rationale="All good",
        permissions=(perm,),
        roles=(role,),
        constraints=(constr,),
        obligations=(ob,),
        evidence=(ev,),
    )
    assert result.decision == AuthorizationDecisionType.ALLOW
    assert result.confidence == 0.95
    assert result.rationale == "All good"
    assert result.permissions == (perm,)
    assert result.roles == (role,)
    assert result.constraints == (constr,)
    assert result.obligations == (ob,)
    assert result.evidence == (ev,)
    assert isinstance(result.request_id, UUID)
    assert result.created_at.tzinfo == timezone.utc


def test_result_invalid_decision():
    with pytest.raises(SecurityValidationError, match="decision must be an AuthorizationDecisionType"):
        AuthorizationResult(decision="ALLOW")  # type: ignore


def test_result_confidence_out_of_range():
    with pytest.raises(SecurityValidationError, match="confidence must be between 0 and 1"):
        AuthorizationResult(decision=AuthorizationDecisionType.ALLOW, confidence=1.5)


def test_result_invalid_request_id():
    with pytest.raises(SecurityValidationError, match="request_id must be a UUID"):
        AuthorizationResult(decision=AuthorizationDecisionType.ALLOW, request_id="not-uuid")  # type: ignore


def test_result_created_at_naive():
    naive = datetime.now()
    with pytest.raises(SecurityValidationError, match="created_at must be timezone-aware"):
        AuthorizationResult(decision=AuthorizationDecisionType.ALLOW, created_at=naive)


def test_result_invalid_permission():
    with pytest.raises(SecurityValidationError, match="All permissions must be Permission instances"):
        AuthorizationResult(
            decision=AuthorizationDecisionType.ALLOW,
            permissions=("not a permission",),  # type: ignore
        )


def test_result_invalid_role():
    with pytest.raises(SecurityValidationError, match="All roles must be Role instances"):
        AuthorizationResult(
            decision=AuthorizationDecisionType.ALLOW,
            roles=("not a role",),  # type: ignore
        )


def test_result_invalid_constraint():
    with pytest.raises(SecurityValidationError, match="All constraints must be Constraint instances"):
        AuthorizationResult(
            decision=AuthorizationDecisionType.ALLOW,
            constraints=("not a constraint",),  # type: ignore
        )


def test_result_invalid_obligation():
    with pytest.raises(SecurityValidationError, match="All obligations must be Obligation instances"):
        AuthorizationResult(
            decision=AuthorizationDecisionType.ALLOW,
            obligations=("not an obligation",),  # type: ignore
        )


def test_result_invalid_evidence():
    with pytest.raises(SecurityValidationError, match="All evidence items must be AuthorizationEvidence instances"):
        AuthorizationResult(
            decision=AuthorizationDecisionType.ALLOW,
            evidence=("not evidence",),  # type: ignore
        )


def test_result_properties():
    result = AuthorizationResult(decision=AuthorizationDecisionType.ALLOW)
    assert result.allowed is True
    assert result.denied is False
    assert result.not_applicable is False

    result2 = AuthorizationResult(decision=AuthorizationDecisionType.DENY)
    assert result2.allowed is False
    assert result2.denied is True

    result3 = AuthorizationResult(decision=AuthorizationDecisionType.NOT_APPLICABLE)
    assert result3.not_applicable is True


def test_result_permission_names():
    p1 = Permission(name="read")
    p2 = Permission(name="write")
    result = AuthorizationResult(
        decision=AuthorizationDecisionType.ALLOW,
        permissions=(p1, p2),
    )
    assert result.permission_names == frozenset({"read", "write"})


def test_result_role_names():
    r1 = Role(name="admin")
    r2 = Role(name="user")
    result = AuthorizationResult(
        decision=AuthorizationDecisionType.ALLOW,
        roles=(r1, r2),
    )
    assert result.role_names == frozenset({"admin", "user"})


def test_result_to_dict():
    p = Permission(name="read")
    r = Role(name="user")
    ev = AuthorizationEvidence(source="test", description="desc")
    result = AuthorizationResult(
        decision=AuthorizationDecisionType.ALLOW,
        confidence=0.9,
        rationale="Test",
        permissions=(p,),
        roles=(r,),
        evidence=(ev,),
    )
    d = result.to_dict()
    assert d["decision"] == "ALLOW"
    assert d["confidence"] == 0.9
    assert d["rationale"] == "Test"
    assert len(d["permissions"]) == 1
    assert len(d["roles"]) == 1
    assert len(d["evidence"]) == 1
    assert "request_id" in d
    assert "created_at" in d
