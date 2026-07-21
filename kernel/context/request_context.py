# kernel/context/request_context.py
"""
Request context – immutable request metadata.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from .exceptions import ContextValidationError


@dataclass(frozen=True)
class RequestContext:
    """
    Immutable request context.

    Attributes:
        request_id: Unique request identifier.
        identity: User or system identity.
        resource: Target resource.
        operation: Requested operation.
        timestamp: Request timestamp.
        metadata: Additional request metadata.
        environment: Runtime environment data.
        session: Session state.
    """

    request_id: UUID = field(default_factory=uuid4)
    identity: str = ""
    resource: str = ""
    operation: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)
    environment: Dict[str, Any] = field(default_factory=dict)
    session: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.timestamp.tzinfo is None:
            object.__setattr__(self, "timestamp", self.timestamp.replace(tzinfo=timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": str(self.request_id),
            "identity": self.identity,
            "resource": self.resource,
            "operation": self.operation,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "environment": self.environment,
            "session": self.session,
        }
