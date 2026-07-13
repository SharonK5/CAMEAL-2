"""
===============================================================================
Module: security.authorizer

Role-Based Authorization Service for CAMEAL.

Responsibilities
----------------
- Evaluate authorization requests.
- Map roles to permissions.
- Produce AuthorizationResult.
- Remain stateless.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .authorization_request import AuthorizationRequest
from .authorization_result import AuthorizationResult
from .permissions import Permission
from .roles import Role


class Authorizer:
    """
    Stateless RBAC authorization service.
    """

    def __init__(self) -> None:

        self._role_permissions: dict[Role, set[Permission]] = {

            Role.SYSTEM_ADMIN: set(Permission),

            Role.AI_ADMINISTRATOR: {
                Permission.READ,
                Permission.WRITE,
                Permission.QUERY,
                Permission.ANALYZE,
                Permission.CONFIGURE,
                Permission.REVIEW,
            },

            Role.GOVERNANCE_OFFICER: {
                Permission.READ,
                Permission.WRITE,
                Permission.REVIEW,
                Permission.GOVERN,
                Permission.QUERY,
            },

            Role.RESEARCHER: {
                Permission.READ,
                Permission.QUERY,
                Permission.ANALYZE,
                Permission.EXPORT,
            },

            Role.ANALYST: {
                Permission.READ,
                Permission.QUERY,
                Permission.ANALYZE,
            },

            Role.OPERATOR: {
                Permission.READ,
                Permission.WRITE,
                Permission.INGEST,
            },

            Role.API_CLIENT: {
                Permission.READ,
                Permission.QUERY,
            },

            Role.REVIEWER: {
                Permission.READ,
                Permission.REVIEW,
            },

            Role.GUEST: {
                Permission.READ,
            },
        }

    def authorize(
        self,
        request: AuthorizationRequest,
    ) -> AuthorizationResult:

        if not request.user.active:

            return AuthorizationResult(
                success=False,
                message="User account is inactive.",
            )

        for role in request.user.roles:

            permissions = self._role_permissions.get(role, set())

            if request.permission in permissions:

                return AuthorizationResult(
                    success=True,
                    message="Authorization granted.",
                )

        return AuthorizationResult(
            success=False,
            message="Permission denied.",
        )
