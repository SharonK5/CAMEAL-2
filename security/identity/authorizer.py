# security/authorizer.py

from __future__ import annotations

from .authorization_request import AuthorizationRequest
from .authorization_result import AuthorizationResult
from .role_permission_provider import RolePermissionProvider


class Authorizer:
    """
    Stateless RBAC authorization service using a pluggable permission provider.
    """

    def __init__(self, provider: RolePermissionProvider) -> None:
        self._provider = provider

    def authorize(self, request: AuthorizationRequest) -> AuthorizationResult:
        # 1. Check if the user is active
        if not request.user.active:
            return AuthorizationResult(
                success=False,
                message="User account is inactive.",
            )

        # 2. Try each role the user has
        for role in request.user.roles:
            permissions = self._provider.permissions_for(role)
            if request.permission in permissions:
                return AuthorizationResult(
                    success=True,
                    message="Authorization granted.",
                )

        # 3. No matching role granted the required permission
        return AuthorizationResult(
            success=False,
            message="Permission denied.",
        )
