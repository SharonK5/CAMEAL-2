"""
===============================================================================
Tests for context.spatial

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from dataclasses import FrozenInstanceError

import pytest

from context.spatial import SpatialContext


def test_default_construction():
    context = SpatialContext()

    assert context.identifier is None
    assert context.country is None
    assert context.latitude is None
    assert context.metadata == {}


def test_full_construction():
    context = SpatialContext(
        identifier="KE-KAK",
        name="Kakamega",
        country="Kenya",
        region="Western",
        county="Kakamega",
        district="Lurambi",
        subcounty="Lurambi",
        ward="Shieywe",
        locality="CBD",
        latitude=0.2827,
        longitude=34.7519,
        elevation=1535.0,
        coordinate_reference_system="EPSG:4326",
        geometry_type="Point",
        bounding_box=(34.70, 0.20, 34.80, 0.35),
        climate_zone="Humid",
        watershed="Lake Victoria",
        ecosystem="Rainforest",
        land_use="Urban",
        metadata={
            "population": 192000,
        },
    )

    assert context.country == "Kenya"
    assert context.county == "Kakamega"
    assert context.geometry_type == "Point"
    assert context.coordinate_reference_system == "EPSG:4326"
    assert context.bounding_box == (34.70, 0.20, 34.80, 0.35)


def test_metadata_get():
    context = SpatialContext(
        metadata={
            "county_code": "037",
        }
    )

    assert context.get("county_code") == "037"


def test_metadata_default():
    context = SpatialContext()

    assert context.get("missing") is None
    assert context.get("missing", "default") == "default"


def test_contains():
    context = SpatialContext(
        metadata={
            "country": "Kenya",
        }
    )

    assert context.contains("country")
    assert not context.contains("missing")


def test_immutable():
    context = SpatialContext()

    with pytest.raises(FrozenInstanceError):
        context.country = "Uganda"


def test_bounding_box():
    context = SpatialContext(
        bounding_box=(1.0, 2.0, 3.0, 4.0)
    )

    assert len(context.bounding_box) == 4
