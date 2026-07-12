"""
===============================================================================
Module: kernel.response

Immutable response object returned by kernel components.

Responsibilities:
    - Standardize responses across all kernel components.
    - Support auditing and traceability.
    - Provide serialization for APIs and logging.

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

# =============================================================================
# Data Classes
# =============================================================================


@dataclass(slots=True, frozen=True)
class Response:
    """
    Immutable kernel response.
    """

    success: bool

    message: str = ""

    data: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    correlation_id: str | None = None

    component: str | None = None

    execution_time: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id,
            "component": self.component,
            "execution_time": self.execution_time,
        }
