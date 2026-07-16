# security/__init__.py

# Public façade – import common classes from subpackages

from .core import (
    DecisionEngine,
    RiskEngine,
    SecurityError,
    RiskLevel,
)

from .identity import (
    Authenticator,
    Authorizer,
    AuthenticationRequest,
    AuthenticationResult,
    AuthorizationRequest,
    AuthorizationResult,
    IdentityProvider,
    IdentityRecord,
    Session,
    SessionProvider,
    User,
    Role,
    Permission,
    RolePermissionProvider,
    DefaultRolePermissionProvider,
    InMemoryPermissionProvider,
    MemoryIdentityProvider,
    MemorySessionProvider,
)

from .governance import (
    Policy,
    PolicyEngine,
    PolicyStore,
    Constraint,
    Obligation,
)

from .audit import (
    AuditEvent,
    Decision,
    DecisionLog,
)

from .integrity import (
    HashingService,
)

__all__ = [
    # core
    "DecisionEngine",
    "RiskEngine",
    "SecurityError",
    "RiskLevel",
    # identity
    "Authenticator",
    "Authorizer",
    "AuthenticationRequest",
    "AuthenticationResult",
    "AuthorizationRequest",
    "AuthorizationResult",
    "IdentityProvider",
    "IdentityRecord",
    "Session",
    "SessionProvider",
    "User",
    "Role",
    "Permission",
    "RolePermissionProvider",
    "DefaultRolePermissionProvider",
    "InMemoryPermissionProvider",
    "MemoryIdentityProvider",
    "MemorySessionProvider",
    # governance
    "Policy",
    "PolicyEngine",
    "PolicyStore",
    "Constraint",
    "Obligation",
    # audit
    "AuditEvent",
    "Decision",
    "DecisionLog",
    # integrity
    "HashingService",
]
