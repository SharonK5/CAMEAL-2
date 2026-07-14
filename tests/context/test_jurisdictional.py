"""
===============================================================================
Tests for context.jurisdictional

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from dataclasses import FrozenInstanceError

import pytest

from context.jurisdictional import JurisdictionalContext


def test_default_construction():
    context = JurisdictionalContext()

    assert context.identifier is None
    assert context.name is None
    assert context.legal_frameworks == ()
    assert context.metadata == {}


def test_full_construction():
    context = JurisdictionalContext(
        identifier="KE",
        name="Republic of Kenya",
        jurisdiction_type="National",
        level="National",
        parent="East Africa",
        code="KE",
        authority="Constitutional",
        legal_frameworks=(
            "Constitution of Kenya 2010",
        ),
        policies=(
            "National Climate Change Action Plan",
        ),
        regulations=(
            "Data Protection Act",
        ),
        metadata={
            "continent": "Africa",
        },
    )

    assert context.identifier == "KE"
    assert context.name == "Republic of Kenya"
    assert context.code == "KE"
    assert context.authority == "Constitutional"

    assert len(context.legal_frameworks) == 1
    assert len(context.policies) == 1
    assert len(context.regulations) == 1


def test_metadata_get():
    context = JurisdictionalContext(
        metadata={
            "country": "Kenya",
        }
    )

    assert context.get("country") == "Kenya"


def test_metadata_default():
    context = JurisdictionalContext()

    assert context.get("missing") is None
    assert context.get("missing", "default") == "default"


def test_contains():
    context = JurisdictionalContext(
        metadata={
            "country": "Kenya",
        }
    )

    assert context.contains("country")
    assert not context.contains("county")


def test_immutable():
    context = JurisdictionalContext()

    with pytest.raises(FrozenInstanceError):
        context.name = "Changed"


def test_tuple_fields():
    context = JurisdictionalContext(
        legal_frameworks=("Framework",),
        policies=("Policy",),
        regulations=("Regulation",),
    )

    assert isinstance(context.legal_frameworks, tuple)
    assert isinstance(context.policies, tuple)
    assert isinstance(context.regulations, tuple)
