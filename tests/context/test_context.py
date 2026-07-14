"""
Tests for the canonical GovernanceContext.
"""

import pytest
from dataclasses import FrozenInstanceError

# -----------------------------------------------------------------------------
# Dummy contexts for the missing dimensions (replace with real imports later)
# -----------------------------------------------------------------------------
from dataclasses import dataclass

@dataclass(frozen=True)
class JurisdictionalContext:
    authority: str = ""

@dataclass(frozen=True)
class SpatialContext:
    location: str = ""

@dataclass(frozen=True)
class TemporalContext:
    period: str = ""

@dataclass(frozen=True)
class OperationalContext:
    status: str = ""

# -----------------------------------------------------------------------------
# Real imports
# -----------------------------------------------------------------------------
from context.context import GovernanceContext
from context.institutional import InstitutionalContext


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------

@pytest.fixture
def minimal_institutional() -> InstitutionalContext:
    return InstitutionalContext(identifier="KE-MOA", name="Ministry of Agriculture")


@pytest.fixture
def full_institutional() -> InstitutionalContext:
    return InstitutionalContext(
        identifier="KE-MOA",
        name="Ministry",
        mandates=("Policy", "Food"),
    )


@pytest.fixture
def dummy_jurisdictional() -> JurisdictionalContext:
    return JurisdictionalContext(authority="National")


@pytest.fixture
def dummy_spatial() -> SpatialContext:
    return SpatialContext(location="Nairobi")


@pytest.fixture
def dummy_temporal() -> TemporalContext:
    return TemporalContext(period="2025-Q1")


@pytest.fixture
def dummy_operational() -> OperationalContext:
    return OperationalContext(status="Active")


@pytest.fixture
def minimal_governance_context(
    minimal_institutional: InstitutionalContext,
) -> GovernanceContext:
    """Context with only institutional dimension."""
    return GovernanceContext(institutional=minimal_institutional)


@pytest.fixture
def full_governance_context(
    full_institutional: InstitutionalContext,
    dummy_jurisdictional: JurisdictionalContext,
    dummy_spatial: SpatialContext,
    dummy_temporal: TemporalContext,
    dummy_operational: OperationalContext,
) -> GovernanceContext:
    """Context with all five dimensions populated."""
    return GovernanceContext(
        institutional=full_institutional,
        jurisdictional=dummy_jurisdictional,
        spatial=dummy_spatial,
        temporal=dummy_temporal,
        operational=dummy_operational,
        metadata=(("source", "test"), ("version", 1)),  # <-- tuple, not dict
    )


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------

def test_minimal_creation(minimal_governance_context: GovernanceContext) -> None:
    assert minimal_governance_context.institutional is not None
    assert minimal_governance_context.institutional.identifier == "KE-MOA"
    assert minimal_governance_context.jurisdictional is None
    assert minimal_governance_context.spatial is None
    assert minimal_governance_context.temporal is None
    assert minimal_governance_context.operational is None
    assert minimal_governance_context.metadata == ()  # <-- empty tuple


def test_full_creation(full_governance_context: GovernanceContext) -> None:
    ctx = full_governance_context
    assert ctx.institutional.identifier == "KE-MOA"
    assert ctx.jurisdictional.authority == "National"
    assert ctx.spatial.location == "Nairobi"
    assert ctx.temporal.period == "2025-Q1"
    assert ctx.operational.status == "Active"
    assert ctx.metadata == (("source", "test"), ("version", 1))


def test_immutability(minimal_governance_context: GovernanceContext) -> None:
    with pytest.raises(FrozenInstanceError):
        minimal_governance_context.institutional = None  # type: ignore

    with pytest.raises(FrozenInstanceError):
        minimal_governance_context.metadata = ()  # type: ignore


def test_metadata_get_and_contains(full_governance_context: GovernanceContext) -> None:
    ctx = full_governance_context
    assert ctx.get("source") == "test"
    assert ctx.get("nonexistent", default="default") == "default"
    assert ctx.contains("source") is True
    assert ctx.contains("nonexistent") is False


def test_equality_and_hashing() -> None:
    inst = InstitutionalContext(identifier="KE-MOA")
    jur = JurisdictionalContext(authority="National")
    spa = SpatialContext(location="Nairobi")

    ctx1 = GovernanceContext(institutional=inst, jurisdictional=jur, spatial=spa)
    ctx2 = GovernanceContext(institutional=inst, jurisdictional=jur, spatial=spa)
    ctx3 = GovernanceContext(institutional=inst, jurisdictional=jur)

    assert ctx1 == ctx2
    assert hash(ctx1) == hash(ctx2)  # <-- now works because metadata is tuple
    assert ctx1 != ctx3


def test_creation_with_only_metadata() -> None:
    ctx = GovernanceContext(metadata=(("only", "metadata"),))
    assert ctx.institutional is None
    assert ctx.jurisdictional is None
    assert ctx.spatial is None
    assert ctx.temporal is None
    assert ctx.operational is None
    assert ctx.metadata == (("only", "metadata"),)


def test_creation_with_none_dimensions() -> None:
    ctx = GovernanceContext(
        institutional=None,
        jurisdictional=None,
        spatial=None,
        temporal=None,
        operational=None,
    )
    assert ctx.institutional is None
    assert ctx.metadata == ()  # <-- empty tuple, not dict
