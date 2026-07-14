"""
===============================================================================
Module: context.spatial

Spatial governance context.

Represents the geographical environment associated with governance
decisions, policies, documents, workflows, observations, and services.

The Spatial Context intentionally remains independent of any GIS,
remote sensing, or mapping library.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(slots=True, frozen=True)
class SpatialContext:
    """
    Immutable spatial governance context.
    """

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    identifier: str |None = None

    name: str |None = None

    # -------------------------------------------------------------------------
    # Administrative Geography
    # -------------------------------------------------------------------------

    country: str |None = None

    region: str |None = None

    county: str |None = None

    district: str |None = None

    subcounty: str |None = None

    ward: str |None = None

    locality: str |None = None

    # -------------------------------------------------------------------------
    # Coordinates
    # -------------------------------------------------------------------------

    latitude: float |None = None

    longitude: float |None = None

    elevation: float |None = None

    # -------------------------------------------------------------------------
    # Spatial Reference
    # -------------------------------------------------------------------------

    coordinate_reference_system: str |None = None

    geometry_type: str |None = None

    # Examples:
    # Point
    # Polygon
    # MultiPolygon
    # Raster
    # BoundingBox

    bounding_box: tuple[float, float, float, float] |None = None

    # (west, south, east, north)

    # -------------------------------------------------------------------------
    # Governance Geography
    # -------------------------------------------------------------------------

    climate_zone: str |None = None

    watershed: str |None = None

    ecosystem: str |None = None

    land_use: str |None = None

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    metadata: Mapping[str, Any] = field(
        default_factory=dict
    )

    # -------------------------------------------------------------------------
    # Convenience
    # -------------------------------------------------------------------------

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Return metadata value.
        """
        return self.metadata.get(key, default)

    def contains(
        self,
        key: str,
    ) -> bool:
        """
        Return True if metadata contains key.
        """
        return key in self.metadata
