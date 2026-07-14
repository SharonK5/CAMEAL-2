"""
===============================================================================
Tests for context.institutional

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from dataclasses import FrozenInstanceError

import pytest

from context.institutional import InstitutionalContext


def test_default_construction():
    """
    Default construction succeeds.
    """
    context = InstitutionalContext()

    assert context.identifier is None
    assert context.name is None
    assert context.institution_type is None
    assert context.mandates == ()
    assert context.responsibilities == ()
    assert context.metadata == {}


def test_full_construction():
    """
    All fields are correctly assigned.
    """
    context = InstitutionalContext(
        identifier="KE-MOA",
        name="Ministry of Agriculture",
        institution_type="Ministry",
        sector="Agriculture",
        level="National",
        parent="Government of Kenya",
        authority="Strategic",
        ownership="Public",
        mandates=(
            "Policy",
            "Food Security",
        ),
        responsibilities=(
            "Monitoring",
            "Evaluation",
        ),
        metadata={
            "country": "Kenya",
        },
    )

    assert context.identifier == "KE-MOA"
    assert context.name == "Ministry of Agriculture"
    assert context.sector == "Agriculture"
    assert context.level == "National"
    assert context.parent == "Government of Kenya"
    assert context.authority == "Strategic"
    assert context.ownership == "Public"

    assert len(context.mandates) == 2
    assert len(context.responsibilities) == 2


def test_metadata_get():
    """
    Metadata lookup succeeds.
    """
    context = InstitutionalContext(
        metadata={
            "country": "Kenya",
            "county": "Kakamega",
        }
    )

    assert context.get("country") == "Kenya"
    assert context.get("county") == "Kakamega"


def test_metadata_default():
    """
    Missing metadata returns default.
    """
    context = InstitutionalContext()

    assert context.get("missing") is None
    assert context.get("missing", "default") == "default"


def test_contains():
    """
    contains() behaves correctly.
    """
    context = InstitutionalContext(
        metadata={
            "country": "Kenya",
        }
    )

    assert context.contains("country")
    assert not context.contains("county")


def test_immutable():
    """
    InstitutionalContext is immutable.
    """
    context = InstitutionalContext()

    with pytest.raises(FrozenInstanceError):
        context.name = "Changed"


def test_tuple_fields_are_immutable():
    """
    Governance collections are tuples.
    """
    context = InstitutionalContext(
        mandates=("Policy",),
        responsibilities=("Monitoring",),
    )

    assert isinstance(context.mandates, tuple)
    assert isinstance(context.responsibilities, tuple)
