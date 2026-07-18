# security/services/risk/tests/test_risk_service.py
import pytest
from unittest.mock import Mock

from security.services.risk.default_risk_service import DefaultRiskService
from security.services.base.security_context import SecurityContext
from security.services.base.lifecycle import ServiceState, HealthStatus
from security.risk.models import (
    RiskRequest,
    RiskResult,
    RiskLevel,
    RiskFactor,
    RiskFactorType,
    RiskEvidence,
)


@pytest.fixture
def mock_risk_engine():
    return Mock()


@pytest.fixture
def mock_risk_provider():
    return Mock()


@pytest.fixture
def service(mock_risk_engine, mock_risk_provider):
    return DefaultRiskService(
        risk_engine=mock_risk_engine,
        risk_provider=mock_risk_provider,
    )


def test_evaluate_low_risk(service, mock_risk_provider, mock_risk_engine):
    factors = (RiskFactor(name="f", factor_type=RiskFactorType.CUSTOM, score=0.1),)
    mock_risk_provider.get_factors.return_value = factors
    mock_risk_engine.evaluate.return_value = RiskResult(
        overall_score=0.1,
        risk_level=RiskLevel.LOW,
        factors=factors,
        evidence=(RiskEvidence(source="test", description="low"),),
    )

    context = SecurityContext(
        identity="alice",
        resource="/doc/1",
        operation="read",
    )

    decision = service.evaluate(context)

    assert decision.is_abstained is True
    assert "acceptable" in decision.rationale.lower()
    mock_risk_provider.get_factors.assert_called_once()
    mock_risk_engine.evaluate.assert_called_once()


def test_evaluate_high_risk(service, mock_risk_provider, mock_risk_engine):
    factors = (RiskFactor(name="f", factor_type=RiskFactorType.CUSTOM, score=0.9),)
    mock_risk_provider.get_factors.return_value = factors
    mock_risk_engine.evaluate.return_value = RiskResult(
        overall_score=0.9,
        risk_level=RiskLevel.CRITICAL,
        factors=factors,
        evidence=(RiskEvidence(source="test", description="high"),),
    )

    context = SecurityContext(
        identity="alice",
        resource="/doc/1",
        operation="delete",
    )

    decision = service.evaluate(context)

    assert decision.is_denied is True
    assert "too high" in decision.rationale.lower()


def test_assess_alias(service, mock_risk_provider, mock_risk_engine):
    factors = (RiskFactor(name="f", factor_type=RiskFactorType.CUSTOM, score=0.1),)
    mock_risk_provider.get_factors.return_value = factors
    mock_risk_engine.evaluate.return_value = RiskResult(
        overall_score=0.1,
        risk_level=RiskLevel.LOW,
        factors=factors,
    )

    context = SecurityContext(
        identity="alice",
        resource="/doc/1",
        operation="read",
    )

    decision = service.assess(context)
    assert decision.is_abstained is True
    mock_risk_engine.evaluate.assert_called_once()


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
    mock_engine.health.return_value = True
    mock_provider.health.return_value = True
    service = DefaultRiskService(risk_engine=mock_engine, risk_provider=mock_provider)
    service.initialize()
    service.validate()
    service.start()
    assert service.health() == HealthStatus.HEALTHY
    mock_engine.health.return_value = False
    assert service.health() == HealthStatus.UNHEALTHY
