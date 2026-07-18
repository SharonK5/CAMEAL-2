# security/authorization/models.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Optional, Tuple
from uuid import UUID, uuid4

from security.core.exceptions import SecurityValidationError


class AuthorizationDecisionType(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class ResourceType(str, Enum):
    DOCUMENT = "DOCUMENT"
    API = "API"
    SYSTEM = "SYSTEM"
    DATA = "DATA"
    WORKFLOW = "WORKFLOW"
    POLICY = "POLICY"
    EVIDENCE = "EVIDENCE"
    DATASET = "DATASET"
    CLIMATE_RECORD = "CLIMATE_RECORD"
    KNOWLEDGE_OBJECT = "KNOWLEDGE_OBJECT"
    CUSTOM = "CUSTOM"


class AuthorizationReasonCode(str, Enum):
    """Machine‑readable reason codes for authorization decisions."""
    DEFAULT_ALLOW = "DEFAULT_ALLOW"
    POLICY_ALLOW = "POLICY_ALLOW"
    POLICY_DENY = "POLICY_DENY"
    RISK_DENY = "RISK_DENY"
    CONSTRAINT_FAIL = "CONSTRAINT_FAIL"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    ROLE_DENIED = "ROLE_DENIED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


# ------------------------------------------------------------------
# Core domain models
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class Permission:
    name: str
    description: Optional[str] = None
    resource_type: Optional[ResourceType] = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise SecurityValidationError("Permission name cannot be empty.")
        if self.resource_type is not None and not isinstance(self.resource_type, ResourceType):
            raise SecurityValidationError("resource_type must be a ResourceType.")
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata))
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "resource_type": self.resource_type.value if self.resource_type else None,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class Role:
    name: str
    permissions: Tuple[Permission, ...] = ()
    description: Optional[str] = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise SecurityValidationError("Role name cannot be empty.")
        perms = tuple(self.permissions)
        if any(not isinstance(p, Permission) for p in perms):
            raise SecurityValidationError("All permissions must be Permission instances.")
        object.__setattr__(self, "permissions", perms)
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata))
        )

    def has_permission(self, permission_name: str) -> bool:
        return any(p.name == permission_name for p in self.permissions)

    @property
    def permission_names(self) -> frozenset[str]:
        return frozenset(p.name for p in self.permissions)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "permissions": [p.to_dict() for p in self.permissions],
            "description": self.description,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class Constraint:
    name: str
    expression: str
    description: Optional[str] = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise SecurityValidationError("Constraint name cannot be empty.")
        if not self.expression.strip():
            raise SecurityValidationError("Constraint expression cannot be empty.")
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
class Obligation:
    name: str
    action: str
    parameters: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise SecurityValidationError("Obligation name cannot be empty.")
        if not self.action.strip():
            raise SecurityValidationError("Obligation action cannot be empty.")
        object.__setattr__(
            self,
            "parameters",
            MappingProxyType(dict(self.parameters))
        )
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata))
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "action": self.action,
            "parameters": dict(self.parameters),
            "metadata": dict(self.metadata),
        }


# ------------------------------------------------------------------
# Authorization Evidence (typed)
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class AuthorizationEvidence:
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
            raise SecurityValidationError("Evidence timestamp must be timezone-aware.")
        if not isinstance(self.timestamp, datetime):
            raise SecurityValidationError("timestamp must be a datetime.")
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
# Authorization Request (with request_id)
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class AuthorizationRequest:
    identity: str
    resource: str
    operation: str
    request_id: UUID = field(default_factory=uuid4)  # Added
    resource_type: Optional[ResourceType] = None
    resource_id: Optional[str] = None
    permissions: Tuple[str, ...] = ()
    roles: Tuple[str, ...] = ()
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
        if self.resource_type is not None and not isinstance(self.resource_type, ResourceType):
            raise SecurityValidationError("resource_type must be a ResourceType.")
        object.__setattr__(self, "permissions", tuple(self.permissions))
        object.__setattr__(self, "roles", tuple(self.roles))
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
            "resource_type": self.resource_type.value if self.resource_type else None,
            "resource_id": self.resource_id,
            "permissions": list(self.permissions),
            "roles": list(self.roles),
            "metadata": dict(self.metadata),
        }


# ------------------------------------------------------------------
# Authorization Result
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class AuthorizationResult:
    decision: AuthorizationDecisionType
    request_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    confidence: float = 1.0
    rationale: str = ""
    permissions: Tuple[Permission, ...] = ()
    roles: Tuple[Role, ...] = ()
    constraints: Tuple[Constraint, ...] = ()
    obligations: Tuple[Obligation, ...] = ()
    evidence: Tuple[AuthorizationEvidence, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.decision, AuthorizationDecisionType):
            raise SecurityValidationError("decision must be an AuthorizationDecisionType.")
        if not 0.0 <= self.confidence <= 1.0:
            raise SecurityValidationError("confidence must be between 0 and 1.")
        if not isinstance(self.request_id, UUID):
            raise SecurityValidationError("request_id must be a UUID.")
        if not isinstance(self.created_at, datetime):
            raise SecurityValidationError("created_at must be a datetime.")
        if self.created_at.tzinfo is None:
            raise SecurityValidationError("created_at must be timezone-aware.")
        rationale = self.rationale.strip()
        object.__setattr__(self, "rationale", rationale)

        object.__setattr__(self, "permissions", tuple(self.permissions))
        object.__setattr__(self, "roles", tuple(self.roles))
        object.__setattr__(self, "constraints", tuple(self.constraints))
        object.__setattr__(self, "obligations", tuple(self.obligations))
        object.__setattr__(self, "evidence", tuple(self.evidence))

        if any(not isinstance(p, Permission) for p in self.permissions):
            raise SecurityValidationError("All permissions must be Permission instances.")
        if any(not isinstance(r, Role) for r in self.roles):
            raise SecurityValidationError("All roles must be Role instances.")
        if any(not isinstance(c, Constraint) for c in self.constraints):
            raise SecurityValidationError("All constraints must be Constraint instances.")
        if any(not isinstance(o, Obligation) for o in self.obligations):
            raise SecurityValidationError("All obligations must be Obligation instances.")
        if any(not isinstance(e, AuthorizationEvidence) for e in self.evidence):
            raise SecurityValidationError("All evidence items must be AuthorizationEvidence instances.")

    @property
    def allowed(self) -> bool:
        return self.decision is AuthorizationDecisionType.ALLOW

    @property
    def denied(self) -> bool:
        return self.decision is AuthorizationDecisionType.DENY

    @property
    def not_applicable(self) -> bool:
        return self.decision is AuthorizationDecisionType.NOT_APPLICABLE

    @property
    def permission_names(self) -> frozenset[str]:
        return frozenset(p.name for p in self.permissions)

    @property
    def role_names(self) -> frozenset[str]:
        return frozenset(r.name for r in self.roles)

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "request_id": str(self.request_id),
            "created_at": self.created_at.isoformat(),
            "confidence": self.confidence,
            "rationale": self.rationale,
            "permissions": [p.to_dict() for p in self.permissions],
            "roles": [r.to_dict() for r in self.roles],
            "constraints": [c.to_dict() for c in self.constraints],
            "obligations": [o.to_dict() for o in self.obligations],
            "evidence": [e.to_dict() for e in self.evidence],
        }
