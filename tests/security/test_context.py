"""
===============================================================================
Tests for context.context (security integration)
===============================================================================
"""

from context.context import GovernanceContext


def test_defaults():
    context = GovernanceContext()

    # Only the five governance dimensions exist
    assert context.jurisdictional is None
    assert context.institutional is None
    assert context.spatial is None
    assert context.temporal is None
    assert context.operational is None
    # metadata is now a tuple (hashable)
    assert context.metadata == ()


def test_metadata_lookup():
    # metadata is a tuple of (key, value) pairs
    context = GovernanceContext(
        metadata=(("county", "Kakamega"), ("hazard", "Flood"))
    )

    assert context.get("county") == "Kakamega"
    assert context.get("hazard") == "Flood"


def test_missing_metadata():
    context = GovernanceContext()

    assert context.get("missing") is None
    assert context.get("missing", "default") == "default"


def test_contains():
    context = GovernanceContext(
        metadata=(("country", "Kenya"),)
    )

    assert context.contains("country") is True
    assert context.contains("county") is False


def test_context_is_immutable():
    context = GovernanceContext()
    from dataclasses import FrozenInstanceError
    import pytest

    with pytest.raises(FrozenInstanceError):
        context.institutional = "anything"  # type: ignore
