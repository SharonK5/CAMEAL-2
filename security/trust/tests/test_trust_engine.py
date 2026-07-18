# security/trust/tests/test_trust_engine.py
import pytest
from datetime import datetime, timezone, timedelta
from security.trust.default_trust_engine import DefaultTrustEngine
from security.trust.models import TrustSignal, TrustSignalType, TrustLevel, Provenance


def test_evaluate_no_signals():
    engine = DefaultTrustEngine()
    result = engine.evaluate(())
    assert result.overall_score == 0.0
    assert result.trust_level == TrustLevel.NONE
    assert "No trust signals provided" in result.rationale
    assert len(result.evidence) == 1
    assert result.expired_signals == ()


def test_evaluate_single_signal():
    engine = DefaultTrustEngine()
    p = Provenance(source_type="SERVICE", source_id="test", version="1.0.0")
    signals = (TrustSignal(signal_type=TrustSignalType.BEHAVIOR, score=0.5, source="test", provenance=p),)
    result = engine.evaluate(signals)
    assert result.overall_score == 0.5
    assert result.trust_level == TrustLevel.MEDIUM
    assert result.signals == signals
    assert result.expired_signals == ()


def test_evaluate_multiple_signals():
    engine = DefaultTrustEngine()
    p = Provenance(source_type="SERVICE", source_id="test", version="1.0.0")
    s1 = TrustSignal(
        signal_type=TrustSignalType.BEHAVIOR,
        score=0.2,
        weight=1.0,
        source="a",
        provenance=p,
        reliability=0.9,
    )
    s2 = TrustSignal(
        signal_type=TrustSignalType.AUTHENTICATION,
        score=0.8,
        weight=2.0,
        source="b",
        provenance=p,
        reliability=0.8,
    )
    result = engine.evaluate((s1, s2))
    # effective: s1: 0.2*1*0.9 = 0.18, s2: 0.8*2*0.8 = 1.28, total effective = 1.46, total weight = 3, overall = 1.46/3 ≈ 0.4867
    assert result.overall_score == pytest.approx(0.4867, rel=1e-3)
    assert result.trust_level == TrustLevel.MEDIUM
    assert result.expired_signals == ()


def test_evaluate_with_expired_signals():
    engine = DefaultTrustEngine()
    p = Provenance(source_type="SERVICE", source_id="test", version="1.0.0")
    now = datetime.now(timezone.utc)
    expired = TrustSignal(
        signal_type=TrustSignalType.BEHAVIOR,
        score=0.9,
        weight=1.0,
        source="a",
        provenance=p,
        valid_from=now - timedelta(seconds=10),
        valid_until=now - timedelta(seconds=5),
    )
    active = TrustSignal(
        signal_type=TrustSignalType.AUTHENTICATION,
        score=0.5,
        weight=1.0,
        source="b",
        provenance=p,
        valid_from=now,
        valid_until=now + timedelta(hours=1),
    )
    result = engine.evaluate((expired, active))
    # expired effective = 0, active = 0.5*1*1 = 0.5, total weight = 1 (only active)
    assert result.overall_score == 0.5
    assert result.trust_level == TrustLevel.MEDIUM
    assert len(result.expired_signals) == 1
    assert result.expired_signals[0] == expired
    assert "1 expired signal(s) ignored" in result.rationale


def test_classification():
    engine = DefaultTrustEngine()
    assert engine._classify(0.0) == TrustLevel.NONE
    assert engine._classify(0.1) == TrustLevel.LOW
    assert engine._classify(0.3) == TrustLevel.MEDIUM
    assert engine._classify(0.6) == TrustLevel.HIGH
    assert engine._classify(0.8) == TrustLevel.MAXIMUM


def test_engine_metadata():
    engine = DefaultTrustEngine()
    assert engine.ENGINE_NAME == "DefaultTrustEngine"
    assert engine.ENGINE_VERSION == "1.0.0"
