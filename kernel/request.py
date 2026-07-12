"""
===============================================================================
Module: kernel.request

Immutable request object passed through the CAMEAL Kernel.

Responsibilities:
    - Represent a user or system request.
    - Carry execution metadata.
    - Support traceability and auditing.
    - Provide a consistent interface across all kernel components.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

# =============================================================================
# Standard Library Imports
# =============================================================================
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

# =============================================================================
# Data Classes
# =============================================================================


@dataclass(slots=True, frozen=True)
class Request:
    """
    Immutable kernel request.

    Attributes
    ----------
    action:
        Requested operation.

    payload:
        Primary request data.

    metadata:
        Optional execution metadata.

    correlation_id:
        Unique identifier used for tracing.

    timestamp:
        UTC creation timestamp.

    priority:
        Execution priority.
        Lower values indicate higher priority.

    source:
        Origin of the request
        (CLI, API, Dashboard, Scheduler, etc.).

    workflow:
        Optional workflow identifier.
    """

    action: str

    payload: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    correlation_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    priority: int = 100

    source: str = "unknown"

    workflow: str | None = None

    user: str | None = None

    session: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """
        Convert request to a serializable dictionary.
        """

        return {
            "action": self.action,
            "payload": self.payload,
            "metadata": self.metadata,
            "correlation_id": self.correlation_id,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority,
            "source": self.source,
            "workflow": self.workflow,
            "user": self.user,
            "session": self.session,
        }
