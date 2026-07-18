# security/services/base/security_context.py
"""
Security execution context.

Defines the immutable contextual information shared by all
Security Services during authentication, authorization,
policy evaluation, auditing, risk assessment, and trust
computation.

Instances are immutable and safe to share between services.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Any, Optional, Tuple, Dict
from uuid import UUID, uuid4

from .exceptions import ServiceValidationError


class PrincipalType(str, Enum):
    """Types of principals supported by the security framework."""

    USER = "USER"
    SYSTEM = "SYSTEM"
    SERVICE = "SERVICE"
    API_KEY = "API_KEY"
    TOKEN = "TOKEN"
    LLM = "LLM"
    AGENT = "AGENT"


@dataclass(frozen=True, slots=True)
class SecurityContext:
    """
    Immutable context for a security operation.

    Attributes:
        identity: Principal identifier.
        resource: Target resource.
        operation: Requested action.
        principal_type: Type of principal.
        request_id: Unique request identifier.
        session_id: Optional session identifier.
        permissions: Tuple of granted permissions.
        created_at: UTC timestamp of creation.
        metadata: Immutable request metadata (MappingProxyType).
        policy_context: Immutable policy‑specific context (MappingProxyType).

    Note on hashability:
        `metadata` and `policy_context` are excluded from the hash
        because they may contain complex, non‑hashable values.
        This design allows SecurityContext to be used as a dictionary key
        while treating these fields as non‑structural for hashing.
        Two contexts that differ only in metadata or policy_context will
        be considered distinct by `__eq__` but may have the same hash.
        This is intentional and documented; see the associated unit test
        `test_hash_semantics` for a detailed demonstration.
    """

    identity: str
    resource: str
    operation: str

    principal_type: PrincipalType = PrincipalType.USER
    request_id: UUID = field(default_factory=uuid4)
    session_id: Optional[UUID] = None
    permissions: Tuple[str, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
    policy_context: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Validate and normalise the context."""
        if not self.identity.strip():
            raise ServiceValidationError("identity cannot be empty.")
        if not self.resource.strip():
            raise ServiceValidationError("resource cannot be empty.")
        if not self.operation.strip():
            raise ServiceValidationError("operation cannot be empty.")
        if not isinstance(self.permissions, tuple):
            raise ServiceValidationError("permissions must be a tuple.")

        if not isinstance(self.metadata, Mapping):
            raise ServiceValidationError("metadata must be a Mapping.")
        if not isinstance(self.policy_context, Mapping):
            raise ServiceValidationError("policy_context must be a Mapping.")

        # Ensure immutability by converting to MappingProxyType
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata))
        )
        object.__setattr__(
            self,
            "policy_context",
            MappingProxyType(dict(self.policy_context))
        )

    # ------------------------------------------------------------------
    # Custom hash – excludes metadata and policy_context intentionally
    # ------------------------------------------------------------------
    def __hash__(self) -> int:
        return hash((
            self.identity,
            self.resource,
            self.operation,
            self.principal_type,
            self.request_id,
            self.session_id,
            self.permissions,
            self.created_at,
        ))

    # ------------------------------------------------------------------
    # Principal type helpers
    # ------------------------------------------------------------------
    @property
    def is_system(self) -> bool:
        return self.principal_type is PrincipalType.SYSTEM

    @property
    def is_user(self) -> bool:
        return self.principal_type is PrincipalType.USER

    @property
    def is_service(self) -> bool:
        return self.principal_type is PrincipalType.SERVICE

    @property
    def is_machine_identity(self) -> bool:
        return self.principal_type in (
            PrincipalType.SYSTEM,
            PrincipalType.SERVICE,
            PrincipalType.API_KEY,
            PrincipalType.TOKEN,
            PrincipalType.LLM,
            PrincipalType.AGENT,
        )

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------
    @property
    def is_authenticated(self) -> bool:
        return bool(self.identity)

    @property
    def permission_count(self) -> int:
        return len(self.permissions)

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions

    # ------------------------------------------------------------------
    # Copy with updates
    # ------------------------------------------------------------------
    def with_updates(self, **changes) -> "SecurityContext":
        """Create a new context with specified fields updated."""
        return replace(self, **changes)

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary (JSON‑friendly)."""
        return {
            "request_id": str(self.request_id),
            "identity": self.identity,
            "principal_type": self.principal_type.value,
            "resource": self.resource,
            "operation": self.operation,
            "session_id": str(self.session_id) if self.session_id else None,
            "permissions": list(self.permissions),
            "metadata": dict(sorted(self.metadata.items())),
            "policy_context": dict(sorted(self.policy_context.items())),
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SecurityContext":
        """
        Reconstruct a SecurityContext from a dictionary.

        All timestamps must be timezone‑aware (UTC is recommended).
        Missing optional fields (request_id, session_id, created_at)
        will be filled with dataclass defaults.
        """
        # Validate required fields
        required = {"identity", "resource", "operation", "principal_type"}
        missing = required - set(data.keys())
        if missing:
            raise ServiceValidationError(
                f"Missing required fields: {', '.join(sorted(missing))}"
            )

        try:
            principal_type = PrincipalType(data["principal_type"])
        except (KeyError, ValueError) as e:
            raise ServiceValidationError(
                f"Invalid principal_type: {data.get('principal_type')!r}"
            ) from e

        kwargs = {
            "identity": data["identity"],
            "resource": data["resource"],
            "operation": data["operation"],
            "principal_type": principal_type,
            "permissions": tuple(data.get("permissions", [])),
            "metadata": data.get("metadata", {}),
            "policy_context": data.get("policy_context", {}),
        }

        if "request_id" in data and data["request_id"] is not None:
            try:
                kwargs["request_id"] = UUID(data["request_id"])
            except ValueError as e:
                raise ServiceValidationError(
                    f"Invalid request_id: {data['request_id']!r}"
                ) from e

        if "session_id" in data and data["session_id"] is not None:
            try:
                kwargs["session_id"] = UUID(data["session_id"])
            except ValueError as e:
                raise ServiceValidationError(
                    f"Invalid session_id: {data['session_id']!r}"
                ) from e

        if "created_at" in data and data["created_at"] is not None:
            try:
                dt = datetime.fromisoformat(data["created_at"])
                if dt.tzinfo is None:
                    raise ServiceValidationError(
                        f"created_at must be timezone‑aware, got: {data['created_at']}"
                    )
                kwargs["created_at"] = dt
            except ValueError as e:
                raise ServiceValidationError(
                    f"Invalid created_at: {data['created_at']!r}"
                ) from e

        return cls(**kwargs)

    def __repr__(self) -> str:
        return (
            f"SecurityContext(identity={self.identity!r}, "
            f"resource={self.resource!r}, "
            f"operation={self.operation!r}, "
            f"principal={self.principal_type.value}, "
            f"request_id={self.request_id!r})"
        )

    def __str__(self) -> str:
        return (
            f"SecurityContext("
            f"identity={self.identity!r}, "
            f"principal={self.principal_type.value}, "
            f"resource={self.resource!r}, "
            f"operation={self.operation!r})"
        )
