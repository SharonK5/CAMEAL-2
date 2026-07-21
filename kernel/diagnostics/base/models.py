# kernel/diagnostics/base/models.py
"""
Data models for diagnostics.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional, List
from enum import Enum

from ...lifecycle import HealthStatus


class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    FATAL = "fatal"


class TraceStatus(str, Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Metric:
    """A single metric value."""
    name: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    type: str = "counter"  # counter, gauge, histogram


@dataclass
class LogEntry:
    """A structured log entry."""
    level: LogLevel
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    source: Optional[str] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    request_id: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Span:
    """A trace span."""
    name: str
    span_id: str
    trace_id: str
    parent_span_id: Optional[str] = None
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    status: TraceStatus = TraceStatus.STARTED
    attributes: Dict[str, str] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Trace:
    """A complete trace consisting of multiple spans."""
    trace_id: str
    name: str
    spans: List[Span] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    status: TraceStatus = TraceStatus.STARTED


@dataclass
class HealthReport:
    """Health report for a component."""
    component: str
    status: HealthStatus
    timestamp: datetime = field(default_factory=datetime.now)
    details: Optional[Dict[str, Any]] = None
