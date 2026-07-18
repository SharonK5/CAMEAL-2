import pytest
from unittest.mock import Mock

from security.services.authentication.default_authentication_service import (
    DefaultAuthenticationService,
)
from security.services.base.lifecycle import ServiceState, HealthStatus


def test_service_lifecycle():
    authenticator = Mock()
    identity_provider = Mock()
    session_provider = Mock()
    audit_logger = Mock()

    service = DefaultAuthenticationService(
        authenticator=authenticator,
        identity_provider=identity_provider,
        session_provider=session_provider,
        audit_logger=audit_logger,
    )

    assert service.state == ServiceState.CREATED

    service.initialize()
    assert service.state == ServiceState.INITIALIZED

    service.validate()
    assert service.state == ServiceState.VALIDATED

    service.start()
    assert service.state == ServiceState.RUNNING

    authenticator.health.return_value = True
    identity_provider.health.return_value = True
    session_provider.health.return_value = True
    audit_logger.health.return_value = True

    assert service.health() == HealthStatus.HEALTHY

    authenticator.health.return_value = False
    assert service.health() == HealthStatus.UNHEALTHY

    service.shutdown()
    assert service.state == ServiceState.STOPPED

    service.dispose()
    assert service.state == ServiceState.DISPOSED
