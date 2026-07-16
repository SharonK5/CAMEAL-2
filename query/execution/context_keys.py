"""
===============================================================================
Module: query.execution.context_keys

Well-known execution context keys.

These constants define the shared contract between execution stages.
No execution stage should use raw string literals.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations


class ContextKeys:
    """
    Shared execution context keys.
    """

    # Validation
    VALIDATED = "validated"

    # Security
    SECURITY_DECISION = "security_decision"
    SECURITY_RESULT = "security_result"

    # Context
    GOVERNANCE_CONTEXT = "governance_context"

    # Repository
    REPOSITORIES = "repositories"

    # Routing
    ROUTE = "route"
    QUERY_HANDLER = "query_handler"

    # Query result
    QUERY_RESULT = "query_result"

    # Monitoring & metrics
    EVENTS = "events"
    METRICS = "metrics"
    TRACE = "trace"
    ERRORS = "errors"

    # Timings
    START_TIME = "start_time"
    END_TIME = "end_time"
    EXECUTION_TIME = "execution_time"

    # Analytics
    ANALYTICS_RESULT = "analytics_result"

    # Monitoring (future)
    MONITORING_RESULT = "monitoring_result"
