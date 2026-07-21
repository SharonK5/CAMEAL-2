# kernel/models/request.py
"""
Request model – input to the kernel.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Request:
    """
    Immutable request object.

    Attributes:
        request_id: Unique request identifier.
        identity: User or system identity.
        resource: Target resource.
        operation: Requested operation.
        workflow_name: Optional name of the workflow to execute.  # ✅ added
        context: Additional context data.
        metadata: Additional metadata.
        environment: Runtime environment data.
        session: Session state.
    """

    request_id: UUID = field(default_factory=uuid4)
    identity: str = ""
    resource: str = ""
    operation: str = ""
    workflow_name: Optional[str] = None   # ✅ added
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    environment: Dict[str, Any] = field(default_factory=dict)
    session: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": str(self.request_id),
            "identity": self.identity,
            "resource": self.resource,
            "operation": self.operation,
            "workflow_name": self.workflow_name,
            "context": self.context,
            "metadata": self.metadata,
            "environment": self.environment,
            "session": self.session,
        }
