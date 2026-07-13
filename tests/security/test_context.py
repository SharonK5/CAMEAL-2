"""
===============================================================================
Tests for security.context
===============================================================================
"""

from security.context import GovernanceContext


def test_defaults():

    context = GovernanceContext()

    assert context.jurisdiction is None
    assert context.institution is None
    assert context.workflow is None
    assert context.environment is None
    assert context.emergency is False
    assert context.metadata == {}


def test_metadata_lookup():

    context = GovernanceContext(
        metadata={
            "county": "Kakamega",
            "hazard": "Flood",
        }
    )

    assert context.get("county") == "Kakamega"
    assert context.get("hazard") == "Flood"


def test_missing_metadata():

    context = GovernanceContext()

    assert context.get("missing") is None
    assert context.get("missing", "default") == "default"


def test_contains():

    context = GovernanceContext(
        metadata={"country": "Kenya"}
    )

    assert context.contains("country")
    assert not context.contains("county")


def test_context_is_immutable():

    context = GovernanceContext()

    try:
        context.workflow = "Emergency"
        assert False
    except Exception:
        assert True
