"""
===============================================================================
Tests for context.operational

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from dataclasses import FrozenInstanceError

import pytest

from context.operational import OperationalContext


def test_default_construction():
    context = OperationalContext()

    assert context.identifier is None
    assert context.environment is None
    assert context.emergency is False
    assert context.automated is False
    assert context.metadata == {}


def test_full_construction():
    context = OperationalContext(
        identifier="OPS001",
        name="Climate Monitoring",
        environment="Production",
        workflow="Climate Early Warning",
        workflow_stage="Monitoring",
        process="Observation",
        service="Climate API",
        operation="Daily Monitoring",
        platform="Linux",
        technology="Python",
        execution_mode="Human-AI",
        status="Running",
        priority="High",
        emergency=True,
        automated=True,
        metadata={
            "cluster": "production-east",
        },
    )

    assert context.environment == "Production"
    assert context.workflow == "Climate Early Warning"
    assert context.execution_mode == "Human-AI"
    assert context.priority == "High"
    assert context.emergency
    assert context.automated


def test_metadata_get():
    context = OperationalContext(
        metadata={
            "cluster": "node-01",
        }
    )

    assert context.get("cluster") == "node-01"


def test_metadata_default():
    context = OperationalContext()

    assert context.get("missing") is None
    assert context.get("missing", "default") == "default"


def test_contains():
    context = OperationalContext(
        metadata={
            "cluster": "node",
        }
    )

    assert context.contains("cluster")
    assert not context.contains("missing")


def test_immutable():
    context = OperationalContext()

    with pytest.raises(FrozenInstanceError):
        context.environment = "Development"


def test_boolean_fields():
    context = OperationalContext(
        emergency=True,
        automated=True,
    )

    assert context.emergency is True
    assert context.automated is True
