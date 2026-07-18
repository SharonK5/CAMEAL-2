# security/services/audit/tests/test_audit_service.py
import pytest
from unittest.mock import Mock
from uuid import uuid4

from security.services.audit.default_audit_service import DefaultAuditService
from security.services.base.security_context import SecurityContext
from security.services.base.lifecycle import ServiceState, HealthStatus
from security.audit.models import AuditEvent, AuditResult, AuditRequest, AuditCategory, AuditSeverity, AuditOutcome


@pytest.fixture
def mock_audit_provider():
    return Mock()


@pytest.fixture
def mock_audit_engine():
    return Mock()


@pytest.fixture
def service(mock_audit_provider, mock_audit_engine):
    return DefaultAuditService(
        audit_provider=mock_audit_provider,
        audit_engine=mock_audit_engine,
    )


def test_log_event(service, mock_audit_provider, mock_audit_engine):
    context = SecurityContext(identity="alice", resource="/doc/1", operation="read")
    event = AuditEvent(
        request_id=uuid4(),
        category=AuditCategory.DATA_ACCESS,
        severity=AuditSeverity.INFO,
        outcome=AuditOutcome.SUCCESS,
        identity="alice",
        resource="/doc/1",
        operation="read",
    )
    mock_audit_engine.build_event.return_value = event
    mock_audit_provider.record.return_value = AuditResult(success=True, message="Logged")

    decision = service.log_event(context, category=AuditCategory.DATA_ACCESS)

    assert decision.is_allowed is True
    mock_audit_engine.build_event.assert_called_once()
    mock_audit_provider.record.assert_called_once()


def test_log_event_with_details(service, mock_audit_provider, mock_audit_engine):
    context = SecurityContext(identity="alice", resource="/doc/1", operation="read")
    event = AuditEvent(
        request_id=uuid4(),
        category=AuditCategory.SYSTEM,
        severity=AuditSeverity.WARNING,
        outcome=AuditOutcome.FAILURE,
        identity="alice",
        resource="/doc/1",
        operation="read",
    )
    mock_audit_engine.build_event.return_value = event
    mock_audit_provider.record.return_value = AuditResult(success=True, message="Logged")

    decision = service.log_event(
        context,
        category=AuditCategory.SYSTEM,
        severity=AuditSeverity.WARNING,
        outcome=AuditOutcome.FAILURE,
        details={"error": "access denied"},
    )

    assert decision.is_allowed is True
    mock_audit_engine.build_event.assert_called_once()
    mock_audit_provider.record.assert_called_once()


def test_query_events(service, mock_audit_provider):
    event = AuditEvent(
        request_id=uuid4(),
        category=AuditCategory.SYSTEM,
        severity=AuditSeverity.INFO,
        outcome=AuditOutcome.SUCCESS,
        identity="alice",
        resource="/r",
        operation="op",
    )
    mock_audit_provider.query.return_value = (event,)
    results = service.query_events({})
    assert len(results) == 1
    assert results[0].identity == "alice"


def test_query_events_no_provider_query(service, mock_audit_provider):
    # Remove the query method from the mock to simulate a provider that doesn't support querying
    del mock_audit_provider.query
    results = service.query_events({})
    assert results == ()


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
    mock_provider = Mock()
    mock_engine = Mock()
    mock_provider.health.return_value = True
    mock_engine.health.return_value = True
    service = DefaultAuditService(audit_provider=mock_provider, audit_engine=mock_engine)
    service.initialize()
    service.validate()
    service.start()
    assert service.health() == HealthStatus.HEALTHY
    mock_provider.health.return_value = False
    assert service.health() == HealthStatus.UNHEALTHY
