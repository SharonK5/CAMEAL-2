import pytest
from security.risk.default_risk_engine import DefaultRiskEngine
from security.risk.models import RiskFactor, RiskFactorType, RiskLevel


def test_evaluate_no_factors():
    engine = DefaultRiskEngine()
    result = engine.evaluate(())
    assert result.overall_score == 0.0
    assert result.risk_level == RiskLevel.NONE
    assert "No risk factors provided" in result.rationale
    assert result.confidence == 1.0
    assert len(result.evidence) == 1


def test_evaluate_single_factor():
    engine = DefaultRiskEngine()
    factors = (RiskFactor(name="f", factor_type=RiskFactorType.CUSTOM, score=0.5),)
    result = engine.evaluate(factors)
    assert result.overall_score == 0.5
    assert result.risk_level == RiskLevel.HIGH
    assert result.factors == factors
    assert result.confidence == 1.0
    assert len(result.evidence) == 1
    assert result.evidence[0].source == "DefaultRiskEngine"


def test_evaluate_multiple_factors():
    engine = DefaultRiskEngine()
    f1 = RiskFactor(name="a", factor_type=RiskFactorType.CUSTOM, score=0.2, weight=1.0)
    f2 = RiskFactor(name="b", factor_type=RiskFactorType.CUSTOM, score=0.8, weight=2.0)
    result = engine.evaluate((f1, f2))
    assert result.overall_score == 0.6
    assert result.risk_level == RiskLevel.HIGH
    assert result.confidence == 1.0


def test_classification():
    engine = DefaultRiskEngine()
    assert engine._classify(0.0) == RiskLevel.NONE
    assert engine._classify(0.1) == RiskLevel.LOW
    assert engine._classify(0.3) == RiskLevel.MEDIUM
    assert engine._classify(0.6) == RiskLevel.HIGH
    assert engine._classify(0.8) == RiskLevel.CRITICAL


def test_engine_metadata():
    engine = DefaultRiskEngine()
    assert engine.engine_name == "DefaultRiskEngine"
    assert engine.version == "1.0.0"
    assert engine.ALGORITHM == "weighted_average"


def test_lifecycle():
    engine = DefaultRiskEngine()
    engine.initialize()
    engine.validate()
    assert engine.health() is True
    engine.shutdown()
