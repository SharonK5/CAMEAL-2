# security/audit/tests/test_audit_models.py
import pytest
from datetime import datetime, timezone
from uuid import UUID, uuid4

from security.core.exceptions import SecurityValidationError
from security.audit.models import (
    AuditSeverity,
    AuditCategory,
    AuditOutcome,
    AuditRequest,
    AuditEvidence,
    AuditEvent,
    AuditResult,
)


def test_audit_request_creation():
    req = AuditRequest(
        identity="alice",
        resource="/doc/1",
        operation="read",
        category=AuditCategory.DATA_ACCESS,
        metadata={"ip": "127.0.0.1"},
    )
    assert req.identity == "alice"
    assert req.resource == "/doc/1"
    assert req.operation == "read"
    assert req.category == AuditCategory.DATA_ACCESS
    assert req.metadata["ip"] == "127.0.0.1"


def test_audit_request_identity_empty():
    with pytest.raises(SecurityValidationError, match="Identity cannot be empty"):
        AuditRequest(identity="", resource="/r", operation="op", category=AuditCategory.SYSTEM)


def test_audit_request_resource_empty():
    with pytest.raises(SecurityValidationError, match="Resource cannot be empty"):
        AuditRequest(identity="i", resource="", operation="op", category=AuditCategory.SYSTEM)


def test_audit_request_operation_empty():
    with pytest.raises(SecurityValidationError, match="Operation cannot be empty"):
        AuditRequest(identity="i", resource="/r", operation="", category=AuditCategory.SYSTEM)


def test_audit_request_invalid_category():
    with pytest.raises(SecurityValidationError, match="category must be an AuditCategory"):
        AuditRequest(identity="i", resource="/r", operation="op", category="SYSTEM")  # type: ignore


def test_audit_request_to_dict():
    req = AuditRequest(
        identity="alice",
        resource="/doc/1",
        operation="read",
        category=AuditCategory.DATA_ACCESS,
        metadata={"ip": "127.0.0.1"},
    )
    d = req.to_dict()
    assert d["identity"] == "alice"
    assert d["resource"] == "/doc/1"
    assert d["operation"] == "read"
    assert d["category"] == "DATA_ACCESS"
    assert d["metadata"] == {"ip": "127.0.0.1"}


def test_audit_evidence_creation():
    ev = AuditEvidence(source="test", description="desc")
    assert ev.source == "test"
    assert ev.description == "desc"
    assert ev.timestamp.tzinfo == timezone.utc


def test_audit_evidence_source_empty():
    with pytest.raises(SecurityValidationError, match="Evidence source cannot be empty"):
        AuditEvidence(source="", description="desc")


def test_audit_evidence_description_empty():
    with pytest.raises(SecurityValidationError, match="Evidence description cannot be empty"):
        AuditEvidence(source="s", description="")


def test_audit_evidence_timestamp_naive():
    naive = datetime.now()
    with pytest.raises(SecurityValidationError, match="timestamp must be timezone-aware"):
        AuditEvidence(source="s", description="d", timestamp=naive)


def test_audit_evidence_to_dict():
    ev = AuditEvidence(source="s", description="d")
    d = ev.to_dict()
    assert d["source"] == "s"
    assert d["description"] == "d"
    assert "timestamp" in d
    assert d["attributes"] == {}


def test_audit_event_creation():
    req_id = uuid4()
    event = AuditEvent(
        request_id=req_id,
        category=AuditCategory.AUTHENTICATION,
        severity=AuditSeverity.INFO,
        outcome=AuditOutcome.SUCCESS,
        identity="alice",
        resource="/doc/1",
        operation="read",
        details={"key": "value"},
        correlation_id="corr-123",
    )
    assert isinstance(event.event_id, UUID)
    assert event.request_id == req_id
    assert event.category == AuditCategory.AUTHENTICATION
    assert event.severity == AuditSeverity.INFO
    assert event.outcome == AuditOutcome.SUCCESS
    assert event.identity == "alice"
    assert event.resource == "/doc/1"
    assert event.operation == "read"
    assert event.details["key"] == "value"
    assert event.correlation_id == "corr-123"
    assert event.timestamp.tzinfo == timezone.utc


def test_audit_event_invalid_category():
    with pytest.raises(SecurityValidationError, match="category must be an AuditCategory"):
        AuditEvent(
            request_id=uuid4(),
            category="SYSTEM",  # type: ignore
            severity=AuditSeverity.INFO,
            outcome=AuditOutcome.SUCCESS,
            identity="i",
            resource="/r",
            operation="op",
        )


def test_audit_event_invalid_severity():
    with pytest.raises(SecurityValidationError, match="severity must be an AuditSeverity"):
        AuditEvent(
            request_id=uuid4(),
            category=AuditCategory.SYSTEM,
            severity="INFO",  # type: ignore
            outcome=AuditOutcome.SUCCESS,
            identity="i",
            resource="/r",
            operation="op",
        )


def test_audit_event_invalid_outcome():
    with pytest.raises(SecurityValidationError, match="outcome must be an AuditOutcome"):
        AuditEvent(
            request_id=uuid4(),
            category=AuditCategory.SYSTEM,
            severity=AuditSeverity.INFO,
            outcome="SUCCESS",  # type: ignore
            identity="i",
            resource="/r",
            operation="op",
        )


def test_audit_event_identity_empty():
    with pytest.raises(SecurityValidationError, match="Identity cannot be empty"):
        AuditEvent(
            request_id=uuid4(),
            category=AuditCategory.SYSTEM,
            severity=AuditSeverity.INFO,
            outcome=AuditOutcome.SUCCESS,
            identity="",
            resource="/r",
            operation="op",
        )


def test_audit_event_resource_empty():
    with pytest.raises(SecurityValidationError, match="Resource cannot be empty"):
        AuditEvent(
            request_id=uuid4(),
            category=AuditCategory.SYSTEM,
            severity=AuditSeverity.INFO,
            outcome=AuditOutcome.SUCCESS,
            identity="i",
            resource="",
            operation="op",
        )


def test_audit_event_operation_empty():
    with pytest.raises(SecurityValidationError, match="Operation cannot be empty"):
        AuditEvent(
            request_id=uuid4(),
            category=AuditCategory.SYSTEM,
            severity=AuditSeverity.INFO,
            outcome=AuditOutcome.SUCCESS,
            identity="i",
            resource="/r",
            operation="",
        )


def test_audit_event_to_dict():
    req_id = uuid4()
    event = AuditEvent(
        request_id=req_id,
        category=AuditCategory.AUTHENTICATION,
        severity=AuditSeverity.INFO,
        outcome=AuditOutcome.SUCCESS,
        identity="alice",
        resource="/doc/1",
        operation="read",
        details={"key": "value"},
        correlation_id="corr-123",
    )
    d = event.to_dict()
    assert "event_id" in d
    assert d["request_id"] == str(req_id)
    assert d["category"] == "AUTHENTICATION"
    assert d["severity"] == "INFO"
    assert d["outcome"] == "SUCCESS"
    assert d["identity"] == "alice"
    assert d["resource"] == "/doc/1"
    assert d["operation"] == "read"
    assert d["details"] == {"key": "value"}
    assert d["correlation_id"] == "corr-123"


def test_audit_result_creation():
    ev = AuditEvidence(source="test", description="desc")
    event_id = uuid4()
    result = AuditResult(
        success=True,
        event_id=event_id,
        message="Logged",
        evidence=(ev,),
    )
    assert result.success is True
    assert result.event_id == event_id
    assert result.message == "Logged"
    assert result.evidence == (ev,)
    assert isinstance(result.request_id, UUID)
    assert result.created_at.tzinfo == timezone.utc


def test_audit_result_invalid_event_id():
    with pytest.raises(SecurityValidationError, match="event_id must be a UUID"):
        AuditResult(success=True, event_id="not-uuid")  # type: ignore


def test_audit_result_created_at_naive():
    naive = datetime.now()
    with pytest.raises(SecurityValidationError, match="created_at must be timezone-aware"):
        AuditResult(success=True, created_at=naive)


def test_audit_result_invalid_evidence():
    with pytest.raises(SecurityValidationError, match="All evidence items must be AuditEvidence instances"):
        AuditResult(success=True, evidence=("not evidence",))  # type: ignore


def test_audit_result_to_dict():
    ev = AuditEvidence(source="s", description="d")
    event_id = uuid4()
    result = AuditResult(success=True, event_id=event_id, evidence=(ev,))
    d = result.to_dict()
    assert d["success"] is True
    assert d["event_id"] == str(event_id)
    assert "request_id" in d
    assert "created_at" in d
    assert len(d["evidence"]) == 1
    assert d["evidence"][0]["source"] == "s"
