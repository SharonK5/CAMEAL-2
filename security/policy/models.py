# security/policy/models.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Optional, Tuple
from uuid import UUID, uuid4

from security.core.exceptions import SecurityValidationError


class PolicyDecisionType(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class PolicyEffect(str, Enum):
    PERMIT = "PERMIT"
    DENY = "DENY"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class PolicyTargetType(str, Enum):
    RESOURCE = "RESOURCE"
    ACTION = "ACTION"
    PRINCIPAL = "PRINCIPAL"
    ENVIRONMENT = "ENVIRONMENT"


class PolicyStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class PolicyType(str, Enum):
    RBAC = "RBAC"
    ABAC = "ABAC"
    REBAC = "REBAC"
    RULE = "RULE"
    REGO = "REGO"
    CEDAR = "CEDAR"
    CUSTOM = "CUSTOM"


# ------------------------------------------------------------------
# Core domain models
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class PolicyVersion:
    major: int
    minor: int
    patch: int

    def __post_init__(self) -> None:
        if self.major < 0 or self.minor < 0 or self.patch < 0:
            raise SecurityValidationError("Version components must be non-negative.")

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def to_dict(self) -> dict[str, Any]:
        return {"major": self.major, "minor": self.minor, "patch": self.patch}


@dataclass(frozen=True, slots=True)
class PolicyCondition:
    name: str
    expression: str
    description: Optional[str] = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise SecurityValidationError("Condition name cannot be empty.")
        if not self.expression.strip():
            raise SecurityValidationError("Condition expression cannot be empty.")
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata))
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "expression": self.expression,
            "description": self.description,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class PolicyRule:
    name: str
    effect: PolicyEffect
    rule_id: UUID = field(default_factory=uuid4)
    conditions: Tuple[PolicyCondition, ...] = ()
    description: Optional[str] = None
    priority: int = 0
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise SecurityValidationError("Rule name cannot be empty.")
        if not isinstance(self.effect, PolicyEffect):
            raise SecurityValidationError("effect must be a PolicyEffect.")
        conds = tuple(self.conditions)
        if any(not isinstance(c, PolicyCondition) for c in conds):
            raise SecurityValidationError("All conditions must be PolicyCondition instances.")
        object.__setattr__(self, "conditions", conds)
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata))
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": str(self.rule_id),
            "name": self.name,
            "effect": self.effect.value,
            "conditions": [c.to_dict() for c in self.conditions],
            "description": self.description,
            "priority": self.priority,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class Policy:
    name: str
    policy_type: PolicyType = PolicyType.RULE
    status: PolicyStatus = PolicyStatus.ACTIVE
    version: PolicyVersion = field(default_factory=lambda: PolicyVersion(1, 0, 0))
    policy_id: UUID = field(default_factory=uuid4)
    rules: Tuple[PolicyRule, ...] = ()
    target_type: Optional[PolicyTargetType] = None
    target_value: Optional[str] = None
    description: Optional[str] = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise SecurityValidationError("Policy name cannot be empty.")
        if self.target_type is not None and not isinstance(self.target_type, PolicyTargetType):
            raise SecurityValidationError("target_type must be a PolicyTargetType.")
        if not isinstance(self.policy_type, PolicyType):
            raise SecurityValidationError("policy_type must be a PolicyType.")
        if not isinstance(self.status, PolicyStatus):
            raise SecurityValidationError("status must be a PolicyStatus.")
        if not isinstance(self.version, PolicyVersion):
            raise SecurityValidationError("version must be a PolicyVersion.")
        rules = tuple(self.rules)
        if any(not isinstance(r, PolicyRule) for r in rules):
            raise SecurityValidationError("All rules must be PolicyRule instances.")
        object.__setattr__(self, "rules", rules)
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata))
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": str(self.policy_id),
            "name": self.name,
            "policy_type": self.policy_type.value,
            "status": self.status.value,
            "version": self.version.to_dict(),
            "rules": [r.to_dict() for r in self.rules],
            "target_type": self.target_type.value if self.target_type else None,
            "target_value": self.target_value,
            "description": self.description,
            "metadata": dict(self.metadata),
        }


# ------------------------------------------------------------------
# Policy Request
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class PolicyRequest:
    identity: str
    resource: str
    operation: str
    request_id: UUID = field(default_factory=uuid4)
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    permissions: Tuple[str, ...] = ()
    roles: Tuple[str, ...] = ()
    environment: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
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
        if not isinstance(self.request_id, UUID):
            raise SecurityValidationError("request_id must be a UUID.")
        object.__setattr__(self, "permissions", tuple(self.permissions))
        object.__setattr__(self, "roles", tuple(self.roles))
        object.__setattr__(
            self,
            "environment",
            MappingProxyType(dict(self.environment))
        )
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
            "request_id": str(self.request_id),
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "permissions": list(self.permissions),
            "roles": list(self.roles),
            "environment": dict(self.environment),
            "metadata": dict(self.metadata),
        }


# ------------------------------------------------------------------
# Policy Evidence
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class PolicyEvidence:
    source: str
    description: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    details: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise SecurityValidationError("Evidence source cannot be empty.")
        if not self.description.strip():
            raise SecurityValidationError("Evidence description cannot be empty.")
        if self.timestamp.tzinfo is None:
            raise SecurityValidationError("Evidence timestamp must be timezone-aware.")
        object.__setattr__(
            self,
            "details",
            MappingProxyType(dict(self.details))
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "details": dict(self.details),
        }


# ------------------------------------------------------------------
# Policy Result
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class PolicyResult:
    decision: PolicyDecisionType
    request_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    confidence: float = 1.0
    rationale: str = ""
    execution_time_ms: float = 0.0
    policies_applied: Tuple[Policy, ...] = ()
    rules_applied: Tuple[PolicyRule, ...] = ()
    evidence: Tuple[PolicyEvidence, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.decision, PolicyDecisionType):
            raise SecurityValidationError("decision must be a PolicyDecisionType.")
        if not 0.0 <= self.confidence <= 1.0:
            raise SecurityValidationError("confidence must be between 0 and 1.")
        if not isinstance(self.request_id, UUID):
            raise SecurityValidationError("request_id must be a UUID.")
        if self.created_at.tzinfo is None:
            raise SecurityValidationError("created_at must be timezone-aware.")
        if self.execution_time_ms < 0:
            raise SecurityValidationError("execution_time_ms must be non-negative.")
        rationale = self.rationale.strip()
        object.__setattr__(self, "rationale", rationale)

        object.__setattr__(self, "policies_applied", tuple(self.policies_applied))
        object.__setattr__(self, "rules_applied", tuple(self.rules_applied))
        object.__setattr__(self, "evidence", tuple(self.evidence))

        if any(not isinstance(p, Policy) for p in self.policies_applied):
            raise SecurityValidationError("All policies_applied must be Policy instances.")
        if any(not isinstance(r, PolicyRule) for r in self.rules_applied):
            raise SecurityValidationError("All rules_applied must be PolicyRule instances.")
        if any(not isinstance(e, PolicyEvidence) for e in self.evidence):
            raise SecurityValidationError("All evidence items must be PolicyEvidence instances.")

    @property
    def allowed(self) -> bool:
        return self.decision is PolicyDecisionType.ALLOW

    @property
    def denied(self) -> bool:
        return self.decision is PolicyDecisionType.DENY

    @property
    def not_applicable(self) -> bool:
        return self.decision is PolicyDecisionType.NOT_APPLICABLE

    @property
    def applicable(self) -> bool:
        return self.decision != PolicyDecisionType.NOT_APPLICABLE

    @property
    def policy_names(self) -> frozenset[str]:
        return frozenset(p.name for p in self.policies_applied)

    @property
    def rule_names(self) -> frozenset[str]:
        return frozenset(r.name for r in self.rules_applied)

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "request_id": str(self.request_id),
            "created_at": self.created_at.isoformat(),
            "confidence": self.confidence,
            "rationale": self.rationale,
            "execution_time_ms": self.execution_time_ms,
            "policies_applied": [p.to_dict() for p in self.policies_applied],
            "rules_applied": [r.to_dict() for r in self.rules_applied],
            "evidence": [e.to_dict() for e in self.evidence],
        }
