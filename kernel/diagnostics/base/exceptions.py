# kernel/diagnostics/base/exceptions.py
"""
Diagnostics-specific exceptions.
"""


class DiagnosticsError(Exception):
    """Base exception for all diagnostics errors."""
    pass


class HealthCheckError(DiagnosticsError):
    """Raised when a health check fails unexpectedly."""
    pass


class MetricsError(DiagnosticsError):
    """Raised when a metric collection fails."""
    pass


class TraceError(DiagnosticsError):
    """Raised when a trace operation fails."""
    pass


class LoggerError(DiagnosticsError):
    """Raised when a logging operation fails."""
    pass
