"""
===============================================================================
Module: security.authorization_request

Authorization request.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from .permissions import Permission
from .user import User


@dataclass(slots=True, frozen=True)
class AuthorizationRequest:
    """
    Authorization request.
    """

    user: User

    permission: Permission
