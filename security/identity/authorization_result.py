"""
===============================================================================
Module: security.authorization_result

Authorization result.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class AuthorizationResult:
    """
    Authorization outcome.
    """

    success: bool

    message: str = ""
