"""
===============================================================================
Module: security.authorization

Role-Based Authorization (RBAC) service.

Responsibilities
----------------
- Evaluate whether an authenticated user possesses a required permission.
- Aggregate permissions from all assigned roles.
- Track which role grants each permission (for auditability).
- Return an immutable AuthorizationResult.

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

    Attributes
    ----------
    _role_permissions : dict[Role, set[Permission]]
        Mapping from role to the set of permissions it grants.
        If None is passed, an empty mapping is used.
    """

    def __init__(
        self,
        role_permissions: dict[Role, set[Permission]] | None = None,
    ) -> None:
        """
        Initialize the authorizer.

        Parameters
        ----------
        role_permissions : dict[Role, set[Permission]], optional
            Role‑to‑permissions mapping. If omitted, an empty mapping is used
            (allows for later injection via dependency container).
        """
        self._role_permissions = role_permissions or {}

    def authorize(
        self,
        request: AuthorizationRequest,
    ) -> AuthorizationResult:
        """
        Determine whether the user has the requested permission.

        This method aggregates permissions from all roles assigned to the user,
        remembers which role granted each permission, and returns a result
        with a success flag and a descriptive message.

        Parameters
        ----------
        request : AuthorizationRequest
            Contains the user and the permission being checked.

        Returns
        -------
        AuthorizationResult
            Immutable result with `allowed` (bool), `permission`,
            `user`, and a `message` string.
        """
        # Build a mapping of permission → role that granted it.
        # This enables future explanations like "granted via role X".
        granted_by: dict[Permission, Role] = {}

        for role in request.user.roles:
            for perm in self._role_permissions.get(role, set()):
                # If a permission is granted by multiple roles, the last one wins.
                # For audit purposes you could store a list/set instead.
                granted_by[perm] = role

        success = request.permission in granted_by

        return AuthorizationResult(
            allowed=success,
            permission=request.permission,
            user=request.user,
            message=(
                "Authorization successful."
                if success
                else "Permission denied."
            ),
            # Optionally include `granted_by` if the result class is extended.
            # For now, we keep it internal.
        )
