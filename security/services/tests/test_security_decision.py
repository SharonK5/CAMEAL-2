# security/services/tests/test_security_decision.py
import pytest
from datetime import datetime, timezone
from uuid import UUID

from security.services.base.exceptions import ServiceValidationError
from security.services.base.security_decision import (
    DecisionType,
    Evidence,
    SecurityDecision,
)
from security.services.base.security_result import SecurityResult


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

@pytest.fixture
def sample_evidence() -> Evidence:
    return Evidence(
        source="PolicyEngine",
        data={"rule": "allow_admin", "matched": True},
    )


@pytest.fixture
def sample_decision() -> SecurityDecision:
    evidence = Evidence(source="AuthZ", data={"policy": "read"})
    return SecurityDecision(
        decision=DecisionType.ALLOW,
        confidence=0.95,
        rationale="User has read permission.",
        evidence=(evidence,),
        recommendations=("audit",),
        applied_policies=("POL-001",),
        applied_rules=("RULE-42",),
        execution_time_ms=12,
        audit_metadata={"reviewer": "system"},
    )


@pytest.fixture
def sample_result() -> SecurityResult:
    return SecurityResult.ok(
        data={"processed": True},
        message="Operation successful",
        details={"duration_ms": 42},
    )


# ------------------------------------------------------------------
# Tests for Evidence
# ------------------------------------------------------------------

class TestEvidence:
    def test_evidence_creation(self, sample_evidence):
        assert sample_evidence.source == "PolicyEngine"
        assert sample_evidence.data["rule"] == "allow_admin"
        assert sample_evidence.timestamp.tzinfo == timezone.utc
        assert isinstance(sample_evidence.evidence_id, UUID)

    def test_evidence_default_data(self):
        e = Evidence(source="Test")
        assert e.data == {}
        assert e.timestamp.tzinfo == timezone.utc

    def test_evidence_empty_source(self):
        with pytest.raises(ServiceValidationError, match="evidence source cannot be empty"):
            Evidence(source="")

    def test_evidence_data_must_be_mapping(self):
        with pytest.raises(ServiceValidationError, match="evidence data must be a Mapping"):
            Evidence(source="Test", data=123)  # type: ignore

    def test_evidence_timestamp_must_be_aware(self):
        naive = datetime.now()
        with pytest.raises(ServiceValidationError, match="timestamp must be timezone-aware"):
            Evidence(source="Test", timestamp=naive)

    def test_evidence_immutable_data(self):
        e = Evidence(source="Test", data={"key": "value"})
        with pytest.raises(TypeError):
            e.data["key"] = "changed"  # type: ignore

    def test_evidence_hash_consistency(self):
        e = Evidence(source="A", data={"x": 1})
        h = hash(e)
        assert h == hash(e)  # same object, same hash
        # Two objects with same content but different ID have different hashes
        e2 = Evidence(source="A", data={"x": 1})
        assert hash(e) != hash(e2)  # because evidence_id differs

    def test_evidence_to_dict(self, sample_evidence):
        d = sample_evidence.to_dict()
        assert d["source"] == sample_evidence.source
        assert d["data"] == sample_evidence.data
        assert "timestamp" in d
        assert "evidence_id" in d

    def test_evidence_from_dict(self, sample_evidence):
        d = sample_evidence.to_dict()
        e2 = Evidence.from_dict(d)
        assert e2.source == sample_evidence.source
        assert e2.data == sample_evidence.data
        assert e2.evidence_id == sample_evidence.evidence_id
        assert e2.timestamp == sample_evidence.timestamp

    def test_evidence_from_dict_invalid_timestamp(self):
        d = {"source": "Test", "timestamp": "2021-01-01T00:00:00"}  # naive
        with pytest.raises(ServiceValidationError, match="timestamp must be timezone-aware"):
            Evidence.from_dict(d)

    def test_evidence_repr(self, sample_evidence):
        assert "Evidence" in repr(sample_evidence)
        assert sample_evidence.source in repr(sample_evidence)


# ------------------------------------------------------------------
# Tests for SecurityDecision
# ------------------------------------------------------------------

class TestSecurityDecision:
    def test_decision_creation(self, sample_decision):
        assert sample_decision.decision == DecisionType.ALLOW
        assert sample_decision.confidence == 0.95
        assert sample_decision.rationale == "User has read permission."
        assert len(sample_decision.evidence) == 1
        assert isinstance(sample_decision.evidence[0], Evidence)
        assert sample_decision.recommendations == ("audit",)
        assert sample_decision.applied_policies == ("POL-001",)
        assert sample_decision.applied_rules == ("RULE-42",)
        assert sample_decision.execution_time_ms == 12
        assert sample_decision.audit_metadata["reviewer"] == "system"
        assert sample_decision.created_at.tzinfo == timezone.utc
        assert isinstance(sample_decision.decision_id, UUID)

    def test_decision_required_fields(self):
        with pytest.raises(ServiceValidationError, match="confidence must be between"):
            SecurityDecision(decision=DecisionType.ALLOW, confidence=1.5, rationale="test")
        with pytest.raises(ServiceValidationError, match="rationale cannot be empty"):
            SecurityDecision(decision=DecisionType.ALLOW, confidence=0.5, rationale="")
        with pytest.raises(ServiceValidationError, match="evidence must be provided"):
            SecurityDecision(decision=DecisionType.ALLOW, confidence=0.5, rationale="test")

    def test_decision_evidence_type_validation(self):
        with pytest.raises(ServiceValidationError, match="all evidence items must be Evidence instances"):
            SecurityDecision(
                decision=DecisionType.ALLOW,
                confidence=0.5,
                rationale="test",
                evidence=("not evidence",),  # type: ignore
            )

    def test_decision_recommendation_type_validation(self):
        with pytest.raises(ServiceValidationError, match="recommendations must contain strings"):
            SecurityDecision(
                decision=DecisionType.ALLOW,
                confidence=0.5,
                rationale="test",
                evidence=(Evidence(source="dummy"),),
                recommendations=(123,),  # type: ignore
            )

    def test_decision_policies_type_validation(self):
        with pytest.raises(ServiceValidationError, match="applied_policies must contain strings"):
            SecurityDecision(
                decision=DecisionType.ALLOW,
                confidence=0.5,
                rationale="test",
                evidence=(Evidence(source="dummy"),),
                applied_policies=(123,),  # type: ignore
            )

    def test_decision_rules_type_validation(self):
        with pytest.raises(ServiceValidationError, match="applied_rules must contain strings"):
            SecurityDecision(
                decision=DecisionType.ALLOW,
                confidence=0.5,
                rationale="test",
                evidence=(Evidence(source="dummy"),),
                applied_rules=(123,),  # type: ignore
            )

    def test_decision_timestamp_must_be_aware(self):
        naive = datetime.now()
        with pytest.raises(ServiceValidationError, match="created_at must be timezone-aware"):
            SecurityDecision(
                decision=DecisionType.ALLOW,
                confidence=0.5,
                rationale="test",
                evidence=(Evidence(source="dummy"),),
                created_at=naive,
            )

    def test_decision_immutable_audit_metadata(self):
        d = SecurityDecision(
            decision=DecisionType.ALLOW,
            confidence=0.5,
            rationale="test",
            evidence=(Evidence(source="dummy"),),
            audit_metadata={"key": "value"},
        )
        with pytest.raises(TypeError):
            d.audit_metadata["key"] = "changed"  # type: ignore

    def test_decision_convenience_properties(self, sample_decision):
        assert sample_decision.is_allowed is True
        assert sample_decision.is_denied is False
        assert sample_decision.is_abstained is False
        # 0.95 > 0.75 and < 1.0 => VERY_HIGH
        assert sample_decision.confidence_level == "VERY_HIGH"
        assert sample_decision.evidence_count == 1
        assert sample_decision.has_recommendations is True
        assert sample_decision.evidence_sources == {"AuthZ"}

    def test_decision_add_recommendation(self, sample_decision):
        new_dec = sample_decision.add_recommendation("another")
        assert new_dec.recommendations == ("audit", "another")
        assert sample_decision.recommendations == ("audit",)

    def test_decision_add_recommendation_invalid(self):
        dec = SecurityDecision(
            decision=DecisionType.ALLOW,
            confidence=0.5,
            rationale="test",
            evidence=(Evidence(source="dummy"),),
        )
        with pytest.raises(ServiceValidationError, match="recommendation must be a non-empty string"):
            dec.add_recommendation("")

    def test_decision_add_evidence(self, sample_decision):
        new_ev = Evidence(source="NewSource")
        new_dec = sample_decision.add_evidence(new_ev)
        assert len(new_dec.evidence) == 2
        assert new_dec.evidence[-1].source == "NewSource"
        assert len(sample_decision.evidence) == 1

    def test_decision_add_evidence_invalid(self):
        dec = SecurityDecision(
            decision=DecisionType.ALLOW,
            confidence=0.5,
            rationale="test",
            evidence=(Evidence(source="dummy"),),
        )
        with pytest.raises(ServiceValidationError, match="evidence must be an Evidence instance"):
            dec.add_evidence("not evidence")  # type: ignore

    def test_decision_hash_consistency(self, sample_decision):
        h = hash(sample_decision)
        assert h == hash(sample_decision)  # same object, same hash
        # Different objects with same content but different decision_id should have different hashes
        dec2 = SecurityDecision(
            decision=DecisionType.ALLOW,
            confidence=0.95,
            rationale="User has read permission.",
            evidence=(Evidence(source="AuthZ", data={"policy": "read"}),),
            recommendations=("audit",),
            applied_policies=("POL-001",),
            applied_rules=("RULE-42",),
            execution_time_ms=12,
            audit_metadata={"reviewer": "system"},
        )
        # Since decision_id is different, hashes differ
        assert hash(sample_decision) != hash(dec2)

    def test_decision_to_dict(self, sample_decision):
        d = sample_decision.to_dict()
        assert d["decision"] == "ALLOW"
        assert d["confidence"] == 0.95
        assert d["confidence_level"] == "VERY_HIGH"
        assert d["rationale"] == sample_decision.rationale
        assert d["decision_source"] is None
        assert len(d["evidence"]) == 1
        assert d["recommendations"] == ["audit"]  # sorted
        assert d["applied_policies"] == ["POL-001"]
        assert d["applied_rules"] == ["RULE-42"]
        assert d["execution_time_ms"] == 12
        assert d["audit_metadata"] == {"reviewer": "system"}
        assert "created_at" in d

    def test_decision_from_dict(self, sample_decision):
        d = sample_decision.to_dict()
        dec2 = SecurityDecision.from_dict(d)
        assert dec2.decision == sample_decision.decision
        assert dec2.confidence == sample_decision.confidence
        assert dec2.rationale == sample_decision.rationale
        assert len(dec2.evidence) == 1
        assert dec2.evidence[0].source == sample_decision.evidence[0].source
        assert dec2.recommendations == sample_decision.recommendations
        assert dec2.applied_policies == sample_decision.applied_policies
        assert dec2.applied_rules == sample_decision.applied_rules
        assert dec2.execution_time_ms == sample_decision.execution_time_ms
        assert dec2.audit_metadata == sample_decision.audit_metadata
        assert dec2.decision_id == sample_decision.decision_id
        assert dec2.created_at == sample_decision.created_at

    def test_decision_from_dict_missing_fields(self):
        data = {"decision": "ALLOW", "confidence": 0.9}
        with pytest.raises(ServiceValidationError, match="Missing required fields"):
            SecurityDecision.from_dict(data)

    def test_decision_from_dict_invalid_decision(self):
        data = {"decision": "INVALID", "confidence": 0.9, "rationale": "test"}
        with pytest.raises(ServiceValidationError, match="Invalid decision"):
            SecurityDecision.from_dict(data)

    def test_decision_from_dict_invalid_timestamp(self):
        data = {
            "decision": "ALLOW",
            "confidence": 0.9,
            "rationale": "test",
            "created_at": "2021-01-01T00:00:00",
        }
        with pytest.raises(ServiceValidationError, match="created_at must be timezone-aware"):
            SecurityDecision.from_dict(data)

    def test_decision_repr(self, sample_decision):
        assert "SecurityDecision" in repr(sample_decision)
        assert "ALLOW" in repr(sample_decision)

    def test_decision_str(self, sample_decision):
        assert "SecurityDecision" in str(sample_decision)
        assert "ALLOW" in str(sample_decision)


# ------------------------------------------------------------------
# Tests for SecurityResult
# ------------------------------------------------------------------

class TestSecurityResult:
    def test_result_creation_ok(self, sample_result):
        assert sample_result.success is True
        assert sample_result.message == "Operation successful"
        assert sample_result.data == {"processed": True}
        assert sample_result.error_code is None
        assert sample_result.details["duration_ms"] == 42
        assert sample_result.timestamp.tzinfo == timezone.utc
        assert isinstance(sample_result.result_id, str)

    def test_result_creation_error(self):
        r = SecurityResult.error(
            message="Something went wrong",
            error_code="E001",
            details={"field": "email"},
            data=None,
        )
        assert r.success is False
        assert r.message == "Something went wrong"
        assert r.error_code == "E001"
        assert r.details["field"] == "email"

    def test_result_validation(self):
        with pytest.raises(ServiceValidationError, match="message cannot be empty"):
            SecurityResult(success=True, message="")
        with pytest.raises(ServiceValidationError, match="details must be a Mapping"):
            SecurityResult(success=True, message="ok", details=123)  # type: ignore
        naive = datetime.now()
        with pytest.raises(ServiceValidationError, match="timestamp must be timezone-aware"):
            SecurityResult(success=True, message="ok", timestamp=naive)

    def test_result_immutable_details(self, sample_result):
        with pytest.raises(TypeError):
            sample_result.details["duration_ms"] = 100  # type: ignore

    def test_result_hash_consistency(self):
        r = SecurityResult(success=True, message="ok")
        h = hash(r)
        assert h == hash(r)
        r2 = SecurityResult(success=True, message="ok", data={"x": 1})
        assert hash(r) != hash(r2)  # different data and result_id

    def test_result_to_dict(self, sample_result):
        d = sample_result.to_dict()
        assert d["success"] is True
        assert d["message"] == "Operation successful"
        assert d["data"] == {"processed": True}
        assert d["error_code"] is None
        assert d["details"] == {"duration_ms": 42}
        assert "timestamp" in d
        assert "result_id" in d

    def test_result_from_dict(self, sample_result):
        d = sample_result.to_dict()
        r2 = SecurityResult.from_dict(d)
        assert r2.success == sample_result.success
        assert r2.message == sample_result.message
        assert r2.data == sample_result.data
        assert r2.error_code == sample_result.error_code
        assert r2.details == sample_result.details
        assert r2.result_id == sample_result.result_id
        assert r2.timestamp == sample_result.timestamp

    def test_result_from_dict_missing_fields(self):
        data = {"success": True}
        with pytest.raises(ServiceValidationError, match="Missing required fields"):
            SecurityResult.from_dict(data)

    def test_result_from_dict_invalid_timestamp(self):
        data = {
            "success": True,
            "message": "ok",
            "timestamp": "2021-01-01T00:00:00",
        }
        with pytest.raises(ServiceValidationError, match="timestamp must be timezone-aware"):
            SecurityResult.from_dict(data)

    def test_result_repr(self, sample_result):
        assert "SecurityResult" in repr(sample_result)
        assert "OK" in repr(sample_result)

    def test_result_str(self, sample_result):
        assert "SecurityResult" in str(sample_result)
        assert "Operation successful" in str(sample_result)

    def test_result_with_updates(self, sample_result):
        r2 = sample_result.with_updates(message="Updated message")
        assert r2.message == "Updated message"
        assert sample_result.message == "Operation successful"

    def test_result_bool(self, sample_result):
        assert bool(sample_result) is True
        err = SecurityResult.error(message="fail")
        assert bool(err) is False
