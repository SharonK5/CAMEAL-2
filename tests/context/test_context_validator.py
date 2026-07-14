from datetime import UTC, datetime

from context.context import GovernanceContext
from context.context_builder import ContextBuilder
from context.context_validator import ContextValidator
from context.institutional import InstitutionalContext
from context.jurisdictional import JurisdictionalContext
from context.spatial import SpatialContext
from context.temporal import TemporalContext
from context.operational import OperationalContext


def make_context():
    # InstitutionalContext now requires an identifier
    return ContextBuilder().build(
        institutional=InstitutionalContext(identifier="test"),
        jurisdictional=JurisdictionalContext(),
        spatial=SpatialContext(),
        temporal=TemporalContext(),
        operational=OperationalContext(),
    )


def test_valid_context():
    validator = ContextValidator()
    assert validator.is_valid(make_context())


def test_invalid_latitude():
    validator = ContextValidator()

    context = ContextBuilder().build(
        institutional=InstitutionalContext(identifier="test"),
        jurisdictional=JurisdictionalContext(),
        spatial=SpatialContext(latitude=120),   # invalid: > 90
        temporal=TemporalContext(),
        operational=OperationalContext(),
    )

    assert not validator.is_valid(context)


def test_invalid_longitude():
    validator = ContextValidator()

    context = ContextBuilder().build(
        institutional=InstitutionalContext(identifier="test"),
        jurisdictional=JurisdictionalContext(),
        spatial=SpatialContext(longitude=250),  # invalid: > 180
        temporal=TemporalContext(),
        operational=OperationalContext(),
    )

    assert not validator.is_valid(context)


def test_invalid_bbox():
    validator = ContextValidator()

    context = ContextBuilder().build(
        institutional=InstitutionalContext(identifier="test"),
        jurisdictional=JurisdictionalContext(),
        spatial=SpatialContext(
            bounding_box=(10, 5, 1, 8),  # invalid: min_x > max_x (10 > 1) or min_y > max_y (5 > 8)
        ),
        temporal=TemporalContext(),
        operational=OperationalContext(),
    )

    assert not validator.is_valid(context)


def test_invalid_time():
    validator = ContextValidator()

    now = datetime.now(UTC)

    context = ContextBuilder().build(
        institutional=InstitutionalContext(identifier="test"),
        jurisdictional=JurisdictionalContext(),
        spatial=SpatialContext(),
        temporal=TemporalContext(
            start_time=now,
            end_time=now.replace(year=2025),   # invalid: end < start (2025 vs now)
        ),
        operational=OperationalContext(),
    )

    assert not validator.is_valid(context)


def test_invalid_revision():
    validator = ContextValidator()

    context = ContextBuilder().build(
        institutional=InstitutionalContext(identifier="test"),
        jurisdictional=JurisdictionalContext(),
        spatial=SpatialContext(),
        temporal=TemporalContext(
            revision=0,   # invalid: revision must be >= 1 (if required)
        ),
        operational=OperationalContext(),
    )

    assert not validator.is_valid(context)


def test_invalid_execution_mode():
    validator = ContextValidator()

    context = ContextBuilder().build(
        institutional=InstitutionalContext(identifier="test"),
        jurisdictional=JurisdictionalContext(),
        spatial=SpatialContext(),
        temporal=TemporalContext(),
        operational=OperationalContext(
            execution_mode="QuantumAI",   # not allowed by validator
        ),
    )

    assert not validator.is_valid(context)
