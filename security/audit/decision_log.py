from dataclasses import dataclass, field
from datetime import UTC, datetime

from .decision import Decision


@dataclass(slots=True, frozen=True)
class DecisionLog:

    decision: Decision

    recorded: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
