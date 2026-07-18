# security/trust/tests/test_trust_models.py
import pytest
from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid4

from security.core.exceptions import SecurityValidationError
from security.trust.models import (
    TrustLevel,
    TrustSignalType,
    Provenance,
    TrustSignal,
    TrustRequest,
    TrustEvidence,
    TrustResult,
)


def test_provenance_creation():
    p = Provenance(
        source_type="SERVICE",
        source_id="auth.default",
        version="1.0.0",
        authority="CAMEAL",
        jurisdiction="EU",
        model_name="AuthModel",
        model_version="2.1.0",
        checksum="abc123",
        generated_at=datetime.now(timezone.utc),
        evidence_uri="file:///evidence.json",
    )
    assert p.source_type == "SERVICE"
    assert p.source_id == "auth.default"
    assert p.version == "1.0.0"
    assert p.authority == "CAMEAL"
    assert p.jurisdiction == "EU"
    assert p.model_name == "AuthModel"
    assert p.model_version == "2.1.0"
    assert p.checksum == "abc123"
    assert p.generated_at.tzinfo == timezone.utc
    assert p.evidence_uri == "file:///evidence.json"


def test_provenance_empty_fields():
    with pytest.raises(SecurityValidationError, match="source_type cannot be empty"):
        Provenance(source_type="", source_id="id", version="1.0.0")


def test_provenance_generated_at_naive():
    naive = datetime.now()
    with pytest.raises(SecurityValidationError, match="generated_at must be timezone-aware"):
        Provenance(source_type="S", source_id="id", version="1.0.0", generated_at=naive)


def test_trust_signal_creation():
    p = Provenance(source_type="SERVICE", source_id="auth.default", version="1.0.0")
    now = datetime.now(timezone.utc)
    until = now + timedelta(hours=1)
    s = TrustSignal(
        signal_type=TrustSignalType.BEHAVIOR,
        score=0.8,
        weight=1.5,
        reliability=0.9,
        source="test",
        provenance=p,
        valid_from=now,
        valid_until=until,
        description="Test signal",
    )
    assert isinstance(s.signal_id, UUID)
    assert s.signal_type == TrustSignalType.BEHAVIOR
    assert s.score == 0.8
    assert s.weight == 1.5
    assert s.reliability == 0.9
    assert s.source == "test"
    assert s.provenance == p
    assert s.valid_from == now
    assert s.valid_until == until
    assert s.effective_score == 0.8 * 1.5 * 0.9  # not expired
    assert s.is_expired is False


def test_trust_signal_invalid_reliability():
    p = Provenance(source_type="SERVICE", source_id="id", version="1.0.0")
    with pytest.raises(SecurityValidationError, match="reliability must be between 0 and 1"):
        TrustSignal(signal_type=TrustSignalType.BEHAVIOR, score=0.5, source="s", provenance=p, reliability=1.5)


def test_trust_signal_valid_until_before_from():
    p = Provenance(source_type="SERVICE", source_id="id", version="1.0.0")
    now = datetime.now(timezone.utc)
    earlier = now - timedelta(seconds=10)
    with pytest.raises(SecurityValidationError, match="valid_until must be after valid_from"):
        TrustSignal(
            signal_type=TrustSignalType.BEHAVIOR,
            score=0.5,
            source="s",
            provenance=p,
            valid_from=now,
            valid_until=earlier,
        )


def test_trust_signal_is_expired():
    p = Provenance(source_type="SERVICE", source_id="id", version="1.0.0")
    now = datetime.now(timezone.utc)
    expired = TrustSignal(
        signal_type=TrustSignalType.BEHAVIOR,
        score=0.5,
        source="s",
        provenance=p,
        valid_from=now - timedelta(seconds=10),
        valid_until=now - timedelta(seconds=5),
    )
    assert expired.is_expired is True
    assert expired.effective_score == 0.0


def test_trust_signal_age_seconds():
    p = Provenance(source_type="SERVICE", source_id="id", version="1.0.0")
    now = datetime.now(timezone.utc)
    s = TrustSignal(
        signal_type=TrustSignalType.BEHAVIOR,
        score=0.5,
        source="s",
        provenance=p,
        valid_from=now - timedelta(seconds=30),
    )
    assert 29 <= s.age_seconds <= 31


def test_trust_request_creation():
    req = TrustRequest(
        identity="alice",
        resource="/doc/1",
        operation="read",
        metadata={"ip": "127.0.0.1"},
    )
    assert req.identity == "alice"
    assert req.resource == "/doc/1"
    assert req.operation == "read"
    assert req.metadata["ip"] == "127.0.0.1"


def test_trust_request_identity_empty():
    with pytest.raises(SecurityValidationError, match="Identity cannot be empty"):
        TrustRequest(identity="", resource="/r", operation="op")


def test_trust_evidence_creation():
    ev = TrustEvidence(source="test", description="desc")
    assert ev.source == "test"
    assert ev.description == "desc"
    assert ev.timestamp.tzinfo == timezone.utc


def test_trust_result_creation():
    p = Provenance(source_type="SERVICE", source_id="test", version="1.0.0")
    signal = TrustSignal(signal_type=TrustSignalType.BEHAVIOR, score=0.8, source="test", provenance=p)
    result = TrustResult(
        overall_score=0.75,
        trust_level=TrustLevel.HIGH,
        signals=(signal,),
        rationale="High trust",
    )
    assert result.overall_score == 0.75
    assert result.trust_level == TrustLevel.HIGH
    assert result.signals == (signal,)
    assert result.is_high_trust is True
    assert result.is_acceptable is True


def test_trust_result_invalid_score():
    with pytest.raises(SecurityValidationError, match="overall_score must be between 0 and 1"):
        TrustResult(overall_score=1.5, trust_level=TrustLevel.NONE)


def test_trust_result_created_at_naive():
    naive = datetime.now()
    with pytest.raises(SecurityValidationError, match="created_at must be timezone-aware"):
        TrustResult(overall_score=0.5, trust_level=TrustLevel.MEDIUM, created_at=naive)


def test_trust_result_invalid_signal():
    with pytest.raises(SecurityValidationError, match="All signals must be TrustSignal"):
        TrustResult(
            overall_score=0.5,
            trust_level=TrustLevel.MEDIUM,
            signals=("not a signal",),  # type: ignore
        )


def test_trust_result_properties():
    r_low = TrustResult(overall_score=0.1, trust_level=TrustLevel.LOW)
    assert r_low.is_acceptable is False
    assert r_low.is_high_trust is False

    r_high = TrustResult(overall_score=0.9, trust_level=TrustLevel.MAXIMUM)
    assert r_high.is_acceptable is True
    assert r_high.is_high_trust is True


def test_trust_result_total_effective_score():
    p = Provenance(source_type="SERVICE", source_id="test", version="1.0.0")
    s1 = TrustSignal(signal_type=TrustSignalType.BEHAVIOR, score=0.8, weight=1.0, source="a", provenance=p)
    s2 = TrustSignal(signal_type=TrustSignalType.AUTHENTICATION, score=0.9, weight=2.0, source="b", provenance=p)
    result = TrustResult(
        overall_score=0.85,
        trust_level=TrustLevel.HIGH,
        signals=(s1, s2),
    )
    expected = (0.8*1.0*1.0) + (0.9*2.0*1.0)  # reliability default 1.0
    assert result.total_effective_score == expected
    assert result.total_weight == 3.0


def test_trust_result_expired_signals():
    p = Provenance(source_type="SERVICE", source_id="test", version="1.0.0")
    now = datetime.now(timezone.utc)
    expired = TrustSignal(
        signal_type=TrustSignalType.BEHAVIOR,
        score=0.8,
        source="a",
        provenance=p,
        valid_from=now - timedelta(seconds=10),
        valid_until=now - timedelta(seconds=5),
    )
    active = TrustSignal(
        signal_type=TrustSignalType.BEHAVIOR,
        score=0.5,
        source="b",
        provenance=p,
        valid_from=now,
        valid_until=now + timedelta(hours=1),
    )
    result = TrustResult(
        overall_score=0.5,
        trust_level=TrustLevel.MEDIUM,
        signals=(expired, active),
    )
    assert len(result.expired_signals) == 1
    assert result.expired_signals[0] == expired
