# security/services/trust/tests/test_trust_service.py
import pytest
from unittest.mock import Mock
from types import MappingProxyType
from datetime import datetime, timezone, timedelta

from security.services.trust.default_trust_service import DefaultTrustService
from security.services.base.security_context import SecurityContext
from security.services.base.lifecycle import ServiceState, HealthStatus
from security.trust.models import (
    TrustSignal,
    TrustSignalType,
    TrustResult,
    TrustLevel,
    Provenance,
    TrustRequest,
)


@pytest.fixture
def mock_trust_engine():
    return Mock()


@pytest.fixture
def mock_trust_provider():
    return Mock()


@pytest.fixture
def service(mock_trust_engine, mock_trust_provider):
    return DefaultTrustService(
        trust_engine=mock_trust_engine,
        trust_provider=mock_trust_provider,
    )


def test_evaluate_high_trust(service, mock_trust_provider, mock_trust_engine):
    p = Provenance(source_type="SERVICE", source_id="test", version="1.0.0")
    signals = (TrustSignal(signal_type=TrustSignalType.BEHAVIOR, score=0.8, source="test", provenance=p),)
    mock_trust_provider.get_signals.return_value = signals
    mock_trust_engine.evaluate.return_value = TrustResult(
        overall_score=0.8,
        trust_level=TrustLevel.HIGH,
        signals=signals,
    )

    context = SecurityContext(
        identity="alice",
        resource="/doc/1",
        operation="read",
    )

    decision = service.evaluate(context)
    assert decision.is_allowed is True
    assert "HIGH" in decision.rationale

    # Verify the call was made with the correct request
    mock_trust_provider.get_signals.assert_called_once()
    args, kwargs = mock_trust_provider.get_signals.call_args
    # request is the first positional argument
    request = args[0] if len(args) > 0 else kwargs.get('request')
    assert request is not None
    assert request.identity == "alice"
    assert request.resource == "/doc/1"
    assert request.operation == "read"
    assert dict(request.metadata) == {}
    # previous_results is the second positional argument or keyword
    previous_results = args[1] if len(args) > 1 else kwargs.get('previous_results')
    assert previous_results is None


def test_evaluate_with_previous_results(service, mock_trust_provider, mock_trust_engine):
    p = Provenance(source_type="SERVICE", source_id="test", version="1.0.0")
    signals = (TrustSignal(signal_type=TrustSignalType.AUTHENTICATION, score=0.9, source="auth", provenance=p),)
    mock_trust_provider.get_signals.return_value = signals
    mock_trust_engine.evaluate.return_value = TrustResult(
        overall_score=0.9,
        trust_level=TrustLevel.HIGH,
        signals=signals,
    )

    context = SecurityContext(
        identity="alice",
        resource="/doc/1",
        operation="read",
    )
    previous = {"authentication": {"confidence": 0.9}}
    decision = service.evaluate(context, previous_results=previous)
    assert decision.is_allowed is True

    # Verify the call was made with the correct request
    mock_trust_provider.get_signals.assert_called_once()
    args, kwargs = mock_trust_provider.get_signals.call_args
    request = args[0] if len(args) > 0 else kwargs.get('request')
    assert request is not None
    assert request.identity == "alice"
    assert request.resource == "/doc/1"
    assert request.operation == "read"
    assert dict(request.metadata) == {}
    previous_results = args[1] if len(args) > 1 else kwargs.get('previous_results')
    assert previous_results == previous


def test_evaluate_low_trust(service, mock_trust_provider, mock_trust_engine):
    p = Provenance(source_type="SERVICE", source_id="test", version="1.0.0")
    signals = (TrustSignal(signal_type=TrustSignalType.BEHAVIOR, score=0.1, source="test", provenance=p),)
    mock_trust_provider.get_signals.return_value = signals
    mock_trust_engine.evaluate.return_value = TrustResult(
        overall_score=0.1,
        trust_level=TrustLevel.LOW,
        signals=signals,
    )

    context = SecurityContext(
        identity="alice",
        resource="/doc/1",
        operation="read",
    )

    decision = service.evaluate(context)
    assert decision.is_denied is True


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
    service = DefaultTrustService(trust_engine=mock_engine, trust_provider=mock_provider)
    service.initialize()
    service.validate()
    service.start()
    assert service.health() == HealthStatus.HEALTHY
    mock_engine.health.return_value = False
    assert service.health() == HealthStatus.UNHEALTHY
