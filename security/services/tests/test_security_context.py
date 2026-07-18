"""
tests/test_security_context.py

Unit tests for SecurityContext.
"""

from __future__ import annotations

from datetime import datetime, timezone
from types import MappingProxyType
from uuid import UUID

import pytest

from security.services.base.exceptions import ServiceValidationError
from security.services.base.security_context import (
    PrincipalType,
    SecurityContext,
)


# ---------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------

@pytest.fixture
def context() -> SecurityContext:
    return SecurityContext(
        identity="alice",
        principal_type=PrincipalType.USER,
        resource="/documents/report.pdf",
        operation="read",
        permissions=("read", "download"),
        metadata={"ip": "127.0.0.1"},
        policy_context={"classification": "internal"},
    )


# ---------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------

def test_context_creation(context: SecurityContext):

    assert context.identity == "alice"

    assert context.resource == "/documents/report.pdf"

    assert context.operation == "read"

    assert context.principal_type == PrincipalType.USER


def test_request_id_generated(context: SecurityContext):

    assert isinstance(context.request_id, UUID)


def test_created_at_is_utc(context: SecurityContext):

    assert isinstance(context.created_at, datetime)

    assert context.created_at.tzinfo == timezone.utc


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

@pytest.mark.parametrize(
    "identity",
    ["", " ", "\t", "\n"],
)
def test_invalid_identity(identity):

    with pytest.raises(ServiceValidationError):

        SecurityContext(
            identity=identity,
            resource="/resource",
            operation="read",
        )


@pytest.mark.parametrize(
    "resource",
    ["", " ", "\n"],
)
def test_invalid_resource(resource):

    with pytest.raises(ServiceValidationError):

        SecurityContext(
            identity="alice",
            resource=resource,
            operation="read",
        )


@pytest.mark.parametrize(
    "operation",
    ["", " ", "\t"],
)
def test_invalid_operation(operation):

    with pytest.raises(ServiceValidationError):

        SecurityContext(
            identity="alice",
            resource="/resource",
            operation=operation,
        )


def test_permissions_must_be_tuple():

    with pytest.raises(ServiceValidationError):

        SecurityContext(
            identity="alice",
            resource="/resource",
            operation="read",
            permissions=["read"],   # type: ignore
        )


def test_metadata_must_be_mapping():

    with pytest.raises(ServiceValidationError):

        SecurityContext(
            identity="alice",
            resource="/resource",
            operation="read",
            metadata=123,          # type: ignore
        )


def test_policy_context_must_be_mapping():

    with pytest.raises(ServiceValidationError):

        SecurityContext(
            identity="alice",
            resource="/resource",
            operation="read",
            policy_context=5,      # type: ignore
        )


# ---------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------

def test_context_is_frozen(context):

    with pytest.raises(AttributeError):

        context.identity = "bob"


def test_metadata_is_mapping_proxy(context):

    assert isinstance(context.metadata, MappingProxyType)


def test_policy_context_is_mapping_proxy(context):

    assert isinstance(context.policy_context, MappingProxyType)


def test_metadata_cannot_be_modified(context):

    with pytest.raises(TypeError):

        context.metadata["ip"] = "8.8.8.8"


def test_policy_context_cannot_be_modified(context):

    with pytest.raises(TypeError):

        context.policy_context["classification"] = "public"


# ---------------------------------------------------------------------
# Permission Helpers
# ---------------------------------------------------------------------

def test_has_permission_true(context):

    assert context.has_permission("read")


def test_has_permission_false(context):

    assert not context.has_permission("delete")


def test_permission_count(context):

    assert context.permission_count == 2


# ---------------------------------------------------------------------
# Authentication Helpers
# ---------------------------------------------------------------------

def test_is_authenticated(context):

    assert context.is_authenticated


# ---------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------

def test_to_dict(context):

    data = context.to_dict()

    assert data["identity"] == "alice"

    assert data["resource"] == "/documents/report.pdf"

    assert data["operation"] == "read"

    assert data["principal_type"] == "USER"

    assert data["permissions"] == [
        "read",
        "download",
    ]

    assert isinstance(data["metadata"], dict)

    assert isinstance(data["policy_context"], dict)

    assert isinstance(data["request_id"], str)

    assert isinstance(data["created_at"], str)


# ---------------------------------------------------------------------
# String Representation
# ---------------------------------------------------------------------

def test_string_representation(context):

    text = str(context)

    assert "alice" in text

    assert "USER" in text

    assert "/documents/report.pdf" in text

    assert "read" in text


# ---------------------------------------------------------------------
# Equality
# ---------------------------------------------------------------------

def test_context_equality():

    request_id = UUID("11111111-1111-1111-1111-111111111111")

    created = datetime.now(timezone.utc)

    c1 = SecurityContext(
        identity="alice",
        resource="/r",
        operation="read",
        request_id=request_id,
        created_at=created,
    )

    c2 = SecurityContext(
        identity="alice",
        resource="/r",
        operation="read",
        request_id=request_id,
        created_at=created,
    )

    assert c1 == c2


def test_context_hashable(context):

    mapping = {context: "value"}

    assert mapping[context] == "value"
