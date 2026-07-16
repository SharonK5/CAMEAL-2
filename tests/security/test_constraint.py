"""
===============================================================================
Tests for security.constraint
===============================================================================
"""

import pytest
from dataclasses import FrozenInstanceError

from security.governance.constraint import Constraint


def test_create_constraint():

    constraint = Constraint(
        constraint_id="c1",
        name="Business Hours",
        description="Office hours only.",
        constraint_type="time_window",
    )

    assert constraint.constraint_id == "c1"
    assert constraint.name == "Business Hours"
    assert constraint.enabled is True


def test_default_parameters():

    constraint = Constraint(
        constraint_id="c1",
        name="Test",
        description="Test",
        constraint_type="generic",
    )

    assert constraint.parameters == {}


def test_custom_parameters():

    constraint = Constraint(
        constraint_id="c1",
        name="Confidence",
        description="Minimum confidence",
        constraint_type="confidence",
        parameters={
            "threshold": 0.85,
        },
    )

    assert constraint.parameters["threshold"] == 0.85


def test_disabled_constraint():

    constraint = Constraint(
        constraint_id="c1",
        name="Disabled",
        description="Disabled",
        constraint_type="generic",
        enabled=False,
    )

    assert constraint.enabled is False


def test_constraint_is_immutable():

    constraint = Constraint(
        constraint_id="c1",
        name="Immutable",
        description="Test",
        constraint_type="generic",
    )

    with pytest.raises(FrozenInstanceError):
        constraint.name = "Changed"
