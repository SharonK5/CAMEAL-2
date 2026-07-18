# security/authentication/models.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Optional, Tuple
from uuid import UUID, uuid4

from security.core.exceptions import SecurityValidationError


class IdentityType(str, Enum):
    USER = "USER"
    SYSTEM = "SYSTEM"
    SERVICE = "SERVICE"
    API_KEY = "API_KEY"
    TOKEN = "TOKEN"


class CredentialType(str, Enum):
    PASSWORD = "PASSWORD"
    TOKEN = "TOKEN"
    API_KEY = "API_KEY"
    CERTIFICATE = "CERTIFICATE"
    OAUTH = "OAUTH"


def _deep_freeze(value: Any) -> Any:
    """Recursively freeze a value, turning dicts into MappingProxyType."""
    if isinstance(value, dict):
        return MappingProxyType({k: _deep_freeze(v) for k, v in value.items()})
    elif isinstance(value, (list, tuple)):
        return tuple(_deep_freeze(v) for v in value)
    else:
        return value


@dataclass(frozen=True, slots=True)
class Identity:
    identity_id: UUID
    username: str
    identity_type: IdentityType

    email: Optional[str] = None
    full_name: Optional[str] = None
    system_id: Optional[str] = None
    roles: Tuple[str, ...] = ()
    permissions: Tuple[str, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = None
    enabled: bool = True
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        # Normalize strings
        username = self.username.strip()
        if not username:
            raise SecurityValidationError("Username cannot be empty.")
        object.__setattr__(self, "username", username)

        if self.email is not None:
            email = self.email.strip().lower()
            if not email:
                raise SecurityValidationError("Email cannot be empty if provided.")
            object.__setattr__(self, "email", email)

        if self.system_id is not None:
            system_id = self.system_id.strip()
            if not system_id:
                raise SecurityValidationError("System ID cannot be empty if provided.")
            object.__setattr__(self, "system_id", system_id)

        if not isinstance(self.identity_id, UUID):
            raise SecurityValidationError("identity_id must be a UUID.")
        if not isinstance(self.identity_type, IdentityType):
            raise SecurityValidationError("identity_type must be an IdentityType.")
        if self.created_at.tzinfo is None:
            raise SecurityValidationError("created_at must be timezone-aware.")
        if self.last_login is not None and self.last_login.tzinfo is None:
            raise SecurityValidationError("last_login must be timezone-aware.")

        frozen_meta = _deep_freeze(dict(self.metadata))
        object.__setattr__(self, "metadata", frozen_meta)

    def has_role(self, role: str) -> bool:
        return role.lower() in (r.lower() for r in self.roles)

    def has_permission(self, permission: str) -> bool:
        return permission.lower() in (p.lower() for p in self.permissions)

    def to_dict(self) -> dict[str, Any]:
        return {
            "identity_id": str(self.identity_id),
            "username": self.username,
            "identity_type": self.identity_type.value,
            "email": self.email,
            "full_name": self.full_name,
            "system_id": self.system_id,
            "roles": list(self.roles),
            "permissions": list(self.permissions),
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "enabled": self.enabled,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class Credentials:
    credential_type: CredentialType
    value: str
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        value = self.value.strip()
        if not value:
            raise SecurityValidationError("Credential value cannot be empty.")
        object.__setattr__(self, "value", value)

        if not isinstance(self.credential_type, CredentialType):
            raise SecurityValidationError("credential_type must be a CredentialType.")

        frozen_meta = _deep_freeze(dict(self.metadata))
        object.__setattr__(self, "metadata", frozen_meta)


@dataclass(frozen=True, slots=True)
class Session:
    session_id: UUID
    identity_id: UUID
    expires_at: datetime                     # required field, no default
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_revoked: bool = False
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not isinstance(self.session_id, UUID):
            raise SecurityValidationError("session_id must be a UUID.")
        if not isinstance(self.identity_id, UUID):
            raise SecurityValidationError("identity_id must be a UUID.")
        if self.created_at.tzinfo is None:
            raise SecurityValidationError("created_at must be timezone-aware.")
        if self.expires_at.tzinfo is None:
            raise SecurityValidationError("expires_at must be timezone-aware.")
        if self.last_activity.tzinfo is None:
            raise SecurityValidationError("last_activity must be timezone-aware.")
        if self.expires_at <= self.created_at:
            raise SecurityValidationError("expires_at must be after created_at.")

        frozen_meta = _deep_freeze(dict(self.metadata))
        object.__setattr__(self, "metadata", frozen_meta)

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expires_at

    def is_active(self) -> bool:
        return not self.is_revoked and not self.is_expired()


@dataclass(frozen=True, slots=True)
class AuthenticationResult:
    success: bool
    identity: Optional[Identity] = None
    session: Optional[Session] = None
    message: str = ""
    error_code: Optional[str] = None
    evidence: Tuple[Mapping[str, Any], ...] = ()

    def __post_init__(self) -> None:
        if self.identity is not None and not isinstance(self.identity, Identity):
            raise SecurityValidationError("identity must be an Identity instance.")
        if self.session is not None and not isinstance(self.session, Session):
            raise SecurityValidationError("session must be a Session instance.")

        if self.success and self.identity is None:
            raise SecurityValidationError(
                "Successful authentication requires an identity."
            )

        # Normalize message
        message = self.message.strip()
        object.__setattr__(self, "message", message)

        # Deep-freeze evidence
        frozen_evidence = tuple(
            _deep_freeze(dict(e)) if isinstance(e, dict) else e
            for e in self.evidence
        )
        object.__setattr__(self, "evidence", frozen_evidence)
