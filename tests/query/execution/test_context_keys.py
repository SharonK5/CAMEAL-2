"""
===============================================================================
Tests for query.execution.context_keys
===============================================================================
"""

from query.execution.context_keys import ContextKeys


def test_validated_key():

    assert ContextKeys.VALIDATED == "validated"


def test_security_key():

    assert ContextKeys.SECURITY_DECISION == "security_decision"


def test_context_key():

    assert ContextKeys.GOVERNANCE_CONTEXT == "governance_context"


def test_repository_key():

    assert ContextKeys.REPOSITORIES == "repositories"


def test_route_key():

    assert ContextKeys.ROUTE == "route"


def test_query_result_key():

    assert ContextKeys.QUERY_RESULT == "query_result"


def test_events_key():

    assert ContextKeys.EVENTS == "events"


def test_metrics_key():

    assert ContextKeys.METRICS == "metrics"


def test_trace_key():

    assert ContextKeys.TRACE == "trace"


def test_errors_key():

    assert ContextKeys.ERRORS == "errors"


def test_start_time_key():

    assert ContextKeys.START_TIME == "start_time"


def test_end_time_key():

    assert ContextKeys.END_TIME == "end_time"


def test_execution_time_key():

    assert ContextKeys.EXECUTION_TIME == "execution_time"
