import pytest

from context.context import GovernanceContext
from context.context_builder import ContextBuilder
from context.institutional import InstitutionalContext
from context.jurisdictional import JurisdictionalContext
from context.operational import OperationalContext
from context.spatial import SpatialContext
from context.temporal import TemporalContext


def test_empty_builder():
    context = ContextBuilder().build()

    assert isinstance(context, GovernanceContext)
    assert context.institutional is None
    assert context.jurisdictional is None
    assert context.spatial is None
    assert context.temporal is None
    assert context.operational is None


def test_builder_institutional():
    # Add required identifier
    institutional = InstitutionalContext(identifier="test", name="Ministry")

    context = (
        ContextBuilder()
        .add_institutional(institutional)
        .build()
    )

    assert context.institutional == institutional


def test_builder_complete():
    institutional = InstitutionalContext(identifier="test1", name="MoH")
    jurisdictional = JurisdictionalContext(name="Kenya")
    spatial = SpatialContext(country="Kenya")
    temporal = TemporalContext(fiscal_year="2026")
    operational = OperationalContext(environment="Production")

    context = (
        ContextBuilder()
        .add_institutional(institutional)
        .add_jurisdictional(jurisdictional)
        .add_spatial(spatial)
        .add_temporal(temporal)
        .add_operational(operational)
        .build()
    )

    assert context.institutional == institutional
    assert context.jurisdictional == jurisdictional
    assert context.spatial == spatial
    assert context.temporal == temporal
    assert context.operational == operational


def test_builder_overwrite():
    first = InstitutionalContext(identifier="a", name="One")
    second = InstitutionalContext(identifier="b", name="Two")

    context = (
        ContextBuilder()
        .add_institutional(first)
        .add_institutional(second)
        .build()
    )

    assert context.institutional == second


def test_builder_returns_self():
    builder = ContextBuilder()

    result = builder.add_spatial(SpatialContext())

    assert result is builder
