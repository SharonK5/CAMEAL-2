# security/orchestration/models.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from types import MappingProxyType
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from uuid import UUID, uuid4

from security.core.exceptions import SecurityValidationError
from security.services.base.security_decision import SecurityDecision


class OrchestrationDecisionType(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REVIEW = "REVIEW"
    ESCALATE = "ESCALATE"


class EscalationReason(str, Enum):
    CONFLICTING_EVIDENCE = "CONFLICTING_EVIDENCE"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    HIGH_RISK = "HIGH_RISK"
    POLICY_CONFLICT = "POLICY_CONFLICT"
    INSUFFICIENT_PROVENANCE = "INSUFFICIENT_PROVENANCE"
    LOW_TRUST = "LOW_TRUST"
    HUMAN_REQUIRED = "HUMAN_REQUIRED"
    POLICY_VIOLATION = "POLICY_VIOLATION"
    AUTHENTICATION_FAILURE = "AUTHENTICATION_FAILURE"
    AUTHORIZATION_FAILURE = "AUTHORIZATION_FAILURE"


@dataclass(frozen=True, slots=True)
class Provenance:
    service_name: str
    service_version: str
    engine_name: str
    engine_version: str

    def __post_init__(self) -> None:
        if not self.service_name.strip():
            raise SecurityValidationError("service_name cannot be empty.")
        if not self.service_version.strip():
            raise SecurityValidationError("service_version cannot be empty.")
        if not self.engine_name.strip():
            raise SecurityValidationError("engine_name cannot be empty.")
        if not self.engine_version.strip():
            raise SecurityValidationError("engine_version cannot be empty.")

    def to_dict(self) -> Dict[str, str]:
        return {
            "service_name": self.service_name,
            "service_version": self.service_version,
            "engine_name": self.engine_name,
            "engine_version": self.engine_version,
        }


@dataclass(frozen=True, slots=True)
class ServiceResult:
    provenance: Provenance
    decision: SecurityDecision
    execution_time_ms: int
    error: Optional[str] = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if self.execution_time_ms < 0:
            raise SecurityValidationError("execution_time_ms cannot be negative.")
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata))
        )


@dataclass(frozen=True, slots=True)
class OrchestrationContext:
    # Required fields first
    identity: str
    resource: str
    operation: str

    # Optional fields with defaults
    request_id: UUID = field(default_factory=uuid4)
    correlation_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
    service_results: Mapping[str, ServiceResult] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.identity.strip():
            raise SecurityValidationError("Identity cannot be empty.")
        if not self.resource.strip():
            raise SecurityValidationError("Resource cannot be empty.")
        if not self.operation.strip():
            raise SecurityValidationError("Operation cannot be empty.")
        if self.created_at.tzinfo is None:
            raise SecurityValidationError("created_at must be timezone-aware.")
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata))
        )
        object.__setattr__(
            self,
            "service_results",
            MappingProxyType(dict(self.service_results))
        )

    def with_updates(self, **kwargs) -> "OrchestrationContext":
        # Handle updates immutably
        identity = kwargs.get("identity", self.identity)
        resource = kwargs.get("resource", self.resource)
        operation = kwargs.get("operation", self.operation)
        request_id = kwargs.get("request_id", self.request_id)
        correlation_id = kwargs.get("correlation_id", self.correlation_id)
        created_at = kwargs.get("created_at", self.created_at)
        metadata = kwargs.get("metadata", self.metadata)
        service_results = kwargs.get("service_results", self.service_results)

        return OrchestrationContext(
            identity=identity,
            resource=resource,
            operation=operation,
            request_id=request_id,
            correlation_id=correlation_id,
            created_at=created_at,
            metadata=metadata,
            service_results=service_results,
        )

    def add_service_result(self, name: str, result: ServiceResult) -> "OrchestrationContext":
        new_results = dict(self.service_results)
        new_results[name] = result
        return self.with_updates(service_results=MappingProxyType(new_results))


@dataclass(frozen=True, slots=True)
class EvidenceBundle:
    service_results: Mapping[str, ServiceResult]
    provenance: Mapping[str, Provenance]
    timestamps: Mapping[str, datetime]
    overall_confidence: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.overall_confidence <= 1.0:
            raise SecurityValidationError("overall_confidence must be between 0 and 1.")


@dataclass(frozen=True, slots=True)
class OrchestrationResult:
    # Required fields first
    decision: OrchestrationDecisionType
    confidence: float
    rationale: str
    request_id: UUID
    evidence_bundle: EvidenceBundle

    # Optional fields with defaults
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: Optional[str] = None
    decision_trace: Tuple[str, ...] = ()
    escalation_reasons: Tuple[EscalationReason, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise SecurityValidationError("confidence must be between 0 and 1.")
        if self.created_at.tzinfo is None:
            raise SecurityValidationError("created_at must be timezone-aware.")
        if not self.rationale.strip():
            raise SecurityValidationError("rationale cannot be empty.")
