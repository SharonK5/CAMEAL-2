"""
Version information for the CAMEAL Kernel.

This module provides a single source of truth for the kernel version.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VersionInfo:
    """
    Represents the kernel version.

    Attributes
    ----------
    major : int
        Major release number.
    minor : int
        Minor release number.
    patch : int
        Patch release number.
    stage : str
        Development stage (alpha, beta, rc, stable).
    """

    major: int
    minor: int
    patch: int
    stage: str = "alpha"

    @property
    def full(self) -> str:
        """Return the formatted version string."""
        return f"{self.major}.{self.minor}.{self.patch}-{self.stage}"


VERSION = VersionInfo(
    major=1,
    minor=0,
    patch=0,
    stage="alpha",
)

__version__ = VERSION.full
