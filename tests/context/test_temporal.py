"""
===============================================================================
Tests for context.temporal

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from context.temporal import TemporalContext


def test_default_construction():
    context = TemporalContext()

    assert context.identifier is None
    assert context.name is None
    assert context.revision == 1
    assert context.metadata == {}
    assert isinstance(context.timestamp, datetime)


def test_full_construction():
    now = datetime.now(UTC)

    context = TemporalContext(
        identifier="FY2026",
        name="Financial Year 2026",
        timestamp=now,
        start_time=now,
        end_time=now,
        reporting_period="Annual",
        fiscal_year="2026",
        financial_quarter="Q3",
        season="Long Rains",
        phase="Monitoring",
        version="1.0",
        revision=2,
        metadata={
            "programme": "Climate Resilience",
        },
    )

    assert context.identifier == "FY2026"
    assert context.reporting_period == "Annual"
    assert context.fiscal_year == "2026"
    assert context.financial_quarter == "Q3"
    assert context.phase == "Monitoring"
    assert context.version == "1.0"
    assert context.revision == 2


def test_metadata_get():
    context = TemporalContext(
        metadata={
            "cycle": "Quarterly",
        }
    )

    assert context.get("cycle") == "Quarterly"


def test_metadata_default():
    context = TemporalContext()

    assert context.get("missing") is None
    assert context.get("missing", "default") == "default"


def test_contains():
    context = TemporalContext(
        metadata={
            "year": 2026,
        }
    )

    assert context.contains("year")
    assert not context.contains("month")


def test_immutable():
    context = TemporalContext()

    with pytest.raises(FrozenInstanceError):
        context.phase = "Evaluation"


def test_timestamp_created():
    context = TemporalContext()

    assert isinstance(context.timestamp, datetime)
