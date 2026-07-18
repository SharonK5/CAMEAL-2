# security/audit/models.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Optional, Tuple
from uuid import UUID, uuid4

from security.core.exceptions import SecurityValidationError


class AuditSeverity(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AuditCategory(str, Enum):
    AUTHENTICATION = "AUTHENTICATION"
    AUTHORIZATION = "AUTHORIZATION"
    POLICY = "POLICY"
    RISK = "RISK"
    SYSTEM = "SYSTEM"
    DATA_ACCESS = "DATA_ACCESS"
    ADMIN = "ADMIN"
    COMPLIANCE = "COMPLIANCE"
    SECURITY = "SECURITY"
    GOVERNANCE = "GOVERNANCE"


class AuditOutcome(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    DENIED = "DENIED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    PARTIAL = "PARTIAL"


# ------------------------------------------------------------------
# Audit Request
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class AuditRequest:
    identity: str
    resource: str
    operation: str
    category: AuditCategory
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.identity.strip():
            raise SecurityValidationError("Identity cannot be empty.")
        if not self.resource.strip():
            raise SecurityValidationError("Resource cannot be empty.")
        if not self.operation.strip():
            raise SecurityValidationError("Operation cannot be empty.")
        if not isinstance(self.category, AuditCategory):
            raise SecurityValidationError("category must be an AuditCategory.")
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata))
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "identity": self.identity,
            "resource": self.resource,
            "operation": self.operation,
            "category": self.category.value,
            "metadata": dict(self.metadata),
        }


# ------------------------------------------------------------------
# Audit Evidence
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class AuditEvidence:
    source: str
    description: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    attributes: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise SecurityValidationError("Evidence source cannot be empty.")
        if not self.description.strip():
            raise SecurityValidationError("Evidence description cannot be empty.")
        if self.timestamp.tzinfo is None:
            raise SecurityValidationError("timestamp must be timezone-aware.")
        object.__setattr__(
            self,
            "attributes",
            MappingProxyType(dict(self.attributes))
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "attributes": dict(self.attributes),
        }


# ------------------------------------------------------------------
# Audit Event (immutable record)
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class AuditEvent:
    # Required fields first
    request_id: UUID
    category: AuditCategory
    severity: AuditSeverity
    outcome: AuditOutcome
    identity: str
    resource: str
    operation: str

    # Optional fields with defaults
    event_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    details: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
    evidence: Tuple[AuditEvidence, ...] = ()
    correlation_id: Optional[str] = None

    def __post_init__(self) -> None:
        if self.timestamp.tzinfo is None:
            raise SecurityValidationError("timestamp must be timezone-aware.")
        if not isinstance(self.category, AuditCategory):
            raise SecurityValidationError("category must be an AuditCategory.")
        if not isinstance(self.severity, AuditSeverity):
            raise SecurityValidationError("severity must be an AuditSeverity.")
        if not isinstance(self.outcome, AuditOutcome):
            raise SecurityValidationError("outcome must be an AuditOutcome.")
        if not self.identity.strip():
            raise SecurityValidationError("Identity cannot be empty.")
        if not self.resource.strip():
            raise SecurityValidationError("Resource cannot be empty.")
        if not self.operation.strip():
            raise SecurityValidationError("Operation cannot be empty.")
        if not isinstance(self.request_id, UUID):
            raise SecurityValidationError("request_id must be a UUID.")
        object.__setattr__(
            self,
            "details",
            MappingProxyType(dict(self.details))
        )
        object.__setattr__(self, "evidence", tuple(self.evidence))
        if any(not isinstance(e, AuditEvidence) for e in self.evidence):
            raise SecurityValidationError("All evidence items must be AuditEvidence instances.")

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": str(self.event_id),
            "request_id": str(self.request_id),
            "timestamp": self.timestamp.isoformat(),
            "category": self.category.value,
            "severity": self.severity.value,
            "outcome": self.outcome.value,
            "identity": self.identity,
            "resource": self.resource,
            "operation": self.operation,
            "details": dict(self.details),
            "evidence": [e.to_dict() for e in self.evidence],
            "correlation_id": self.correlation_id,
        }


# ------------------------------------------------------------------
# Audit Result (domain result)
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class AuditResult:
    # Required fields first
    success: bool
    event_id: Optional[UUID] = None
    message: str = ""

    # Optional fields with defaults
    request_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    evidence: Tuple[AuditEvidence, ...] = ()

    def __post_init__(self) -> None:
        if self.created_at.tzinfo is None:
            raise SecurityValidationError("created_at must be timezone-aware.")
        if self.event_id is not None and not isinstance(self.event_id, UUID):
            raise SecurityValidationError("event_id must be a UUID.")
        if not isinstance(self.request_id, UUID):
            raise SecurityValidationError("request_id must be a UUID.")
        message = self.message.strip()
        object.__setattr__(self, "message", message)
        object.__setattr__(self, "evidence", tuple(self.evidence))
        if any(not isinstance(e, AuditEvidence) for e in self.evidence):
            raise SecurityValidationError("All evidence items must be AuditEvidence instances.")

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "request_id": str(self.request_id),
            "created_at": self.created_at.isoformat(),
            "event_id": str(self.event_id) if self.event_id else None,
            "message": self.message,
            "evidence": [e.to_dict() for e in self.evidence],
        }
