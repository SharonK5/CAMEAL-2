# security/authorization/tests/test_authorizer.py
"""
Tests for the default authorizer implementation.
"""

import pytest
from datetime import datetime, timezone
from uuid import uuid4

from security.authorization.default_authorizer import DefaultAuthorizer
from security.authorization.models import (
    AuthorizationRequest,
    AuthorizationDecisionType,
    AuthorizationReasonCode,
)
from security.services.base.lifecycle import HealthStatus


def test_default_authorizer_evaluate():
    authorizer = DefaultAuthorizer()
    request = AuthorizationRequest(
        identity="alice",
        resource="/doc/1",
        operation="read",
    )
    result = authorizer.evaluate(request)

    assert result.decision == AuthorizationDecisionType.ALLOW
    assert result.confidence == 1.0
    assert result.rationale == "Authorization allowed by the default permissive authorizer."
    assert len(result.evidence) == 1
    evidence = result.evidence[0]
    assert evidence.source == "DefaultAuthorizer"
    assert evidence.description == "Default authorizer evaluation – always allows."
    assert evidence.attributes["engine_version"] == "1.0.0"
    assert evidence.attributes["reason_code"] == AuthorizationReasonCode.DEFAULT_ALLOW.value
    assert evidence.attributes["policy_evaluated"] is False
    assert evidence.attributes["constraint_evaluated"] is False
    assert evidence.attributes["risk_evaluated"] is False
    assert evidence.attributes["request_identity"] == "alice"
    assert evidence.attributes["request_resource"] == "/doc/1"
    assert evidence.attributes["request_operation"] == "read"
    assert evidence.attributes["request_id"] == str(request.request_id)
    assert evidence.attributes["default_engine"] is True


def test_default_authorizer_health():
    authorizer = DefaultAuthorizer()
    assert authorizer.health() == HealthStatus.HEALTHY


def test_default_authorizer_validate():
    authorizer = DefaultAuthorizer()
    # Should not raise
    authorizer.validate()


def test_default_authorizer_engine_metadata():
    authorizer = DefaultAuthorizer()
    assert authorizer.engine_name == "DefaultAuthorizer"
    assert authorizer.engine_version == "1.0.0"
