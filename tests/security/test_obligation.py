"""
===============================================================================
Tests for security.obligation
===============================================================================
"""

from dataclasses import FrozenInstanceError

import pytest

from security.governance.obligation import Obligation


def test_create_obligation():
    """
    An obligation can be created with the required fields.
    """

    obligation = Obligation(
        obligation_id="o1",
        name="Audit Log",
        description="Record every governance decision.",
        obligation_type="audit",
    )

    assert obligation.obligation_id == "o1"
    assert obligation.name == "Audit Log"
    assert obligation.description == "Record every governance decision."
    assert obligation.obligation_type == "audit"
    assert obligation.enabled is True


def test_default_parameters():
    """
    Parameters default to an empty dictionary.
    """

    obligation = Obligation(
        obligation_id="o1",
        name="Audit",
        description="Test",
        obligation_type="audit",
    )

    assert obligation.parameters == {}


def test_custom_parameters():
    """
    Custom parameters are preserved.
    """

    obligation = Obligation(
        obligation_id="o1",
        name="Notify",
        description="Notify governance officer.",
        obligation_type="notification",
        parameters={
            "recipient": "governance_officer",
            "priority": "high",
        },
    )

    assert obligation.parameters["recipient"] == "governance_officer"
    assert obligation.parameters["priority"] == "high"


def test_disabled_obligation():
    """
    Obligations may be disabled.
    """

    obligation = Obligation(
        obligation_id="o1",
        name="Archive",
        description="Archive decision.",
        obligation_type="archive",
        enabled=False,
    )

    assert obligation.enabled is False


def test_obligation_is_immutable():
    """
    Obligation objects are immutable.
    """

    obligation = Obligation(
        obligation_id="o1",
        name="Immutable",
        description="Cannot change.",
        obligation_type="audit",
    )

    with pytest.raises(FrozenInstanceError):
        obligation.name = "Changed"


def test_obligation_equality():
    """
    Two identical obligations compare equal.
    """

    left = Obligation(
        obligation_id="o1",
        name="Audit",
        description="Audit decision.",
        obligation_type="audit",
    )

    right = Obligation(
        obligation_id="o1",
        name="Audit",
        description="Audit decision.",
        obligation_type="audit",
    )

    assert left == right


def test_obligation_repr_contains_name():
    """
    Dataclass repr should contain useful identifying information.
    """

    obligation = Obligation(
        obligation_id="o1",
        name="Audit",
        description="Audit decision.",
        obligation_type="audit",
    )

    representation = repr(obligation)

    assert "Audit" in representation
    assert "o1" in representation
