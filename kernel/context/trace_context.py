# kernel/context/trace_context.py
"""
Trace context – distributed tracing.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional

from .exceptions import ContextValidationError


@dataclass(frozen=True)
class TraceContext:
    """
    Immutable trace context.

    Attributes:
        trace_id: Distributed trace identifier.
        span_id: Current span identifier.
        parent_span_id: Parent span identifier.
        sampled: Whether the trace is sampled.
        tags: Additional trace tags.
    """

    trace_id: str = ""
    span_id: str = ""
    parent_span_id: Optional[str] = None
    sampled: bool = True
    tags: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, str]:
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "sampled": str(self.sampled),
            **self.tags,
        }
