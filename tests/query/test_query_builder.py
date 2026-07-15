"""
===============================================================================
Tests for query.query_builder
===============================================================================
"""

from query.query_builder import QueryBuilder
from query.query_intent import QueryIntent

# For context tests
from context.context_builder import ContextBuilder
from context.context_registry import ContextRegistry
from context.institutional import InstitutionalContext
from context.jurisdictional import JurisdictionalContext
from context.spatial import SpatialContext
from context.temporal import TemporalContext
from context.operational import OperationalContext


def make_context():
    return (
        ContextBuilder()
        .add_institutional(
            InstitutionalContext(identifier="inst001", name="Ministry")
        )
        .add_jurisdictional(JurisdictionalContext())
        .add_spatial(SpatialContext())
        .add_temporal(TemporalContext())
        .add_operational(OperationalContext())
        .build()
    )


# --- Existing tests (with intent added) ---

def test_build():
    request = (
        QueryBuilder()
        .identifier("query-001")
        .intent(QueryIntent.RETRIEVE)
        .query("Retrieve climate policies")
        .build()
    )
    assert request.identifier == "query-001"
    assert request.intent is QueryIntent.RETRIEVE
    assert request.query == "Retrieve climate policies"


def test_source():
    request = (
        QueryBuilder()
        .identifier("query")
        .intent(QueryIntent.RETRIEVE)
        .query("test")
        .source("enterprise")
        .build()
    )
    assert request.source == "enterprise"


def test_context():
    context = make_context()
    request = (
        QueryBuilder()
        .identifier("query")
        .intent(QueryIntent.RETRIEVE)
        .query("test")
        .context(context)
        .build()
    )
    assert request.context == context


def test_repository():
    request = (
        QueryBuilder()
        .identifier("query")
        .intent(QueryIntent.RETRIEVE)
        .query("test")
        .repository("policy")
        .repository("rag")
        .build()
    )
    assert request.repositories == ("policy", "rag")


def test_parameter():
    request = (
        QueryBuilder()
        .identifier("query")
        .intent(QueryIntent.RETRIEVE)
        .query("test")
        .parameter("country", "Kenya")
        .build()
    )
    assert request.get_parameter("country") == "Kenya"


def test_metadata():
    request = (
        QueryBuilder()
        .identifier("query")
        .intent(QueryIntent.RETRIEVE)
        .query("test")
        .metadata("user", "admin")
        .build()
    )
    assert request.get_metadata("user") == "admin"


def test_priority():
    request = (
        QueryBuilder()
        .identifier("query")
        .intent(QueryIntent.RETRIEVE)
        .query("test")
        .priority(10)
        .build()
    )
    assert request.priority == 10


# --- New tests for context registry resolution ---

def test_context_resolution():
    registry = ContextRegistry()
    context = make_context()
    registry.register("kenya", context)

    request = (
        QueryBuilder(registry)
        .identifier("q1")
        .intent(QueryIntent.RETRIEVE)
        .query("policy")
        .context_id("kenya")
        .build()
    )
    assert request.context == context


def test_context_resolution_without_registry_raises():
    builder = QueryBuilder()
    builder.identifier("q").query("test")
    try:
        builder.context_id("some-id")
        raised = False
    except RuntimeError:
        raised = True
    assert raised
