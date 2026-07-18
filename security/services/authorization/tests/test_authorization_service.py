# security/services/authorization/tests/test_authorization_service.py
import pytest
from unittest.mock import Mock
from uuid import uuid4

from security.services.authorization.default_authorization_service import (
    DefaultAuthorizationService,
)
from security.services.base.security_context import SecurityContext
from security.services.base.security_decision import DecisionType
from security.services.base.lifecycle import ServiceState, HealthStatus

from security.authorization.models import (
    AuthorizationResult,
    AuthorizationDecisionType,
    AuthorizationEvidence,
    Permission,
    Role,
)


@pytest.fixture
def mock_authorizer():
    return Mock()


@pytest.fixture
def mock_permission_provider():
    return Mock()


@pytest.fixture
def mock_role_provider():
    return Mock()


@pytest.fixture
def mock_constraint_provider():
    return Mock()


@pytest.fixture
def mock_obligation_provider():
    return Mock()


@pytest.fixture
def service(
    mock_authorizer,
    mock_permission_provider,
    mock_role_provider,
    mock_constraint_provider,
    mock_obligation_provider,
) -> DefaultAuthorizationService:
    return DefaultAuthorizationService(
        authorizer=mock_authorizer,
        permission_provider=mock_permission_provider,
        role_provider=mock_role_provider,
        constraint_provider=mock_constraint_provider,
        obligation_provider=mock_obligation_provider,
    )


# ------------------------------------------------------------------
# authorize()
# ------------------------------------------------------------------

def test_authorize_allow(service, mock_authorizer):
    evidence = AuthorizationEvidence(source="test", description="desc")
    domain_result = AuthorizationResult(
        decision=AuthorizationDecisionType.ALLOW,
        rationale="Allowed",
        evidence=(evidence,),
    )
    mock_authorizer.evaluate.return_value = domain_result

    context = SecurityContext(
        identity="alice",
        resource="/doc/1",
        operation="read",
    )

    decision = service.authorize(context)

    assert decision.is_allowed is True
    assert decision.rationale == "Allowed"
    assert decision.confidence == 1.0
    mock_authorizer.evaluate.assert_called_once()
    call_args = mock_authorizer.evaluate.call_args[0][0]
    assert call_args.identity == "alice"
    assert call_args.resource == "/doc/1"
    assert call_args.operation == "read"


def test_authorize_deny(service, mock_authorizer):
    domain_result = AuthorizationResult(
        decision=AuthorizationDecisionType.DENY,
        rationale="Denied",
        evidence=(AuthorizationEvidence(source="test", description="denied"),),
    )
    mock_authorizer.evaluate.return_value = domain_result

    context = SecurityContext(
        identity="alice",
        resource="/doc/1",
        operation="write",
    )

    decision = service.authorize(context)
    assert decision.is_denied is True
    assert decision.rationale == "Denied"


# ------------------------------------------------------------------
# check_permission()
# ------------------------------------------------------------------

def test_check_permission_granted(service, mock_permission_provider):
    perm = Permission(name="read")
    mock_permission_provider.get_permissions.return_value = (perm,)

    decision = service.check_permission("alice", "read", "/doc/1")
    assert decision.is_allowed is True
    assert decision.rationale == "Permission 'read' granted."
    assert len(decision.evidence) == 1


def test_check_permission_denied(service, mock_permission_provider):
    mock_permission_provider.get_permissions.return_value = (Permission(name="write"),)

    decision = service.check_permission("alice", "read", "/doc/1")
    assert decision.is_denied is True
    assert decision.rationale == "Permission 'read' denied."


# ------------------------------------------------------------------
# check_role()
# ------------------------------------------------------------------

def test_check_role_granted(service, mock_role_provider):
    role = Role(name="admin")
    mock_role_provider.get_roles.return_value = (role,)

    decision = service.check_role("alice", "admin")
    assert decision.is_allowed is True
    assert decision.rationale == "Role 'admin' granted."


def test_check_role_denied(service, mock_role_provider):
    mock_role_provider.get_roles.return_value = (Role(name="user"),)

    decision = service.check_role("alice", "admin")
    assert decision.is_denied is True
    assert decision.rationale == "Role 'admin' denied."


# ------------------------------------------------------------------
# evaluate()
# ------------------------------------------------------------------

def test_evaluate(service, mock_authorizer):
    domain_result = AuthorizationResult(
        decision=AuthorizationDecisionType.ALLOW,
        rationale="Eval allow",
        evidence=(AuthorizationEvidence(source="test", description="eval"),),
    )
    mock_authorizer.evaluate.return_value = domain_result

    decision = service.evaluate("alice", "/doc/1", "read")
    assert decision.is_allowed is True
    assert decision.rationale == "Eval allow"
    mock_authorizer.evaluate.assert_called_once()


# ------------------------------------------------------------------
# allowed() / denied()
# ------------------------------------------------------------------

def test_allowed(service, mock_authorizer):
    domain_result = AuthorizationResult(
        decision=AuthorizationDecisionType.ALLOW,
        rationale="Allowed",
        evidence=(AuthorizationEvidence(source="test", description="allowed"),),
    )
    mock_authorizer.evaluate.return_value = domain_result
    assert service.allowed("alice", "/doc/1", "read") is True


def test_denied(service, mock_authorizer):
    domain_result = AuthorizationResult(
        decision=AuthorizationDecisionType.DENY,
        rationale="Denied",
        evidence=(AuthorizationEvidence(source="test", description="denied"),),
    )
    mock_authorizer.evaluate.return_value = domain_result
    assert service.denied("alice", "/doc/1", "write") is True


# ------------------------------------------------------------------
# Lifecycle
# ------------------------------------------------------------------

def test_lifecycle():
    authorizer = Mock()
    permission_provider = Mock()
    role_provider = Mock()
    constraint_provider = Mock()
    obligation_provider = Mock()

    service = DefaultAuthorizationService(
        authorizer=authorizer,
        permission_provider=permission_provider,
        role_provider=role_provider,
        constraint_provider=constraint_provider,
        obligation_provider=obligation_provider,
    )

    assert service.state == ServiceState.CREATED

    service.initialize()
    assert service.state == ServiceState.INITIALIZED

    service.validate()
    assert service.state == ServiceState.VALIDATED

    service.start()
    assert service.state == ServiceState.RUNNING

    authorizer.health.return_value = True
    permission_provider.health.return_value = True
    role_provider.health.return_value = True
    constraint_provider.health.return_value = True
    obligation_provider.health.return_value = True

    assert service.health() == HealthStatus.HEALTHY

    authorizer.health.return_value = False
    assert service.health() == HealthStatus.UNHEALTHY

    service.shutdown()
    assert service.state == ServiceState.STOPPED

    service.dispose()
    assert service.state == ServiceState.DISPOSED
