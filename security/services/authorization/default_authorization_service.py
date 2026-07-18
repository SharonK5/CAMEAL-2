# security/services/authorization/default_authorization_service.py
from __future__ import annotations

from typing import Optional

from security.services.base.security_context import SecurityContext
from security.services.base.security_decision import SecurityDecision
from security.services.base.lifecycle import HealthStatus

from security.authorization.models import (
    AuthorizationRequest,
    AuthorizationResult,
    AuthorizationDecisionType,
    AuthorizationEvidence,
)
from security.authorization.authorizer import Authorizer
from security.authorization.permission_provider import PermissionProvider
from security.authorization.role_provider import RoleProvider
from security.authorization.constraint_provider import ConstraintProvider
from security.authorization.obligation_provider import ObligationProvider

from .authorization_service import AuthorizationService
from .authorization_mapper import AuthorizationMapper


class DefaultAuthorizationService(AuthorizationService):
    VERSION = "1.0.0"
    NAME = "default_authorization"
    DOMAIN = "authorization"

    def __init__(
        self,
        authorizer: Authorizer,
        permission_provider: PermissionProvider,
        role_provider: RoleProvider,
        constraint_provider: ConstraintProvider,
        obligation_provider: ObligationProvider,
    ) -> None:
        super().__init__()
        self._authorizer = authorizer
        self._permission_provider = permission_provider
        self._role_provider = role_provider
        self._constraint_provider = constraint_provider
        self._obligation_provider = obligation_provider
        self._mapper = AuthorizationMapper()

    # ------------------------------------------------------------------
    # Service lifecycle
    # ------------------------------------------------------------------

    def _on_initialize(self) -> None:
        self._authorizer.initialize()
        self._permission_provider.initialize()
        self._role_provider.initialize()
        self._constraint_provider.initialize()
        self._obligation_provider.initialize()

    def _on_validate(self) -> None:
        self._authorizer.validate()
        self._permission_provider.validate()
        self._role_provider.validate()
        self._constraint_provider.validate()
        self._obligation_provider.validate()

    def _on_start(self) -> None:
        pass

    def _on_shutdown(self) -> None:
        self._authorizer.shutdown()
        self._permission_provider.shutdown()
        self._role_provider.shutdown()
        self._constraint_provider.shutdown()
        self._obligation_provider.shutdown()

    def _on_dispose(self) -> None:
        # Only service-owned resources cleanup
        # Providers are already shut down
        pass

    def _on_health(self) -> HealthStatus:
        statuses = [
            self._authorizer.health(),
            self._permission_provider.health(),
            self._role_provider.health(),
            self._constraint_provider.health(),
            self._obligation_provider.health(),
        ]
        return HealthStatus.HEALTHY if all(statuses) else HealthStatus.UNHEALTHY

    @property
    def name(self) -> str:
        return self.NAME

    @property
    def version(self) -> str:
        return self.VERSION

    @property
    def security_domain(self) -> str:
        return self.DOMAIN

    # ------------------------------------------------------------------
    # Private orchestration
    # ------------------------------------------------------------------

    def _evaluate_with_authorizer(self, request: AuthorizationRequest) -> AuthorizationResult:
        """
        Evaluate using the authorizer. The authorizer may use its own internal providers.
        """
        return self._authorizer.evaluate(request)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def authorize(self, context: SecurityContext) -> SecurityDecision:
        request = AuthorizationRequest(
            identity=context.identity,
            resource=context.resource,
            operation=context.operation,
            metadata=context.metadata,
        )
        domain_result = self._evaluate_with_authorizer(request)
        return self._mapper.to_security_decision(domain_result)

    def evaluate(self, identity: str, resource: str, operation: str) -> SecurityDecision:
        request = AuthorizationRequest(
            identity=identity,
            resource=resource,
            operation=operation,
        )
        domain_result = self._evaluate_with_authorizer(request)
        return self._mapper.to_security_decision(domain_result)

    def check_permission(self, identity: str, permission: str, resource: str) -> SecurityDecision:
        # Build request
        request = AuthorizationRequest(
            identity=identity,
            resource=resource,
            operation="check_permission",
        )
        # Use permission provider directly
        perms = self._permission_provider.get_permissions(request)
        has_perm = any(p.name == permission for p in perms)
        if has_perm:
            domain_result = AuthorizationResult(
                decision=AuthorizationDecisionType.ALLOW,
                rationale=f"Permission '{permission}' granted.",
                evidence=(AuthorizationEvidence(
                    source="permission_provider",
                    description=f"Permission {permission} found.",
                    attributes={"permission": permission, "identity": identity},
                ),),
            )
        else:
            domain_result = AuthorizationResult(
                decision=AuthorizationDecisionType.DENY,
                rationale=f"Permission '{permission}' denied.",
                evidence=(AuthorizationEvidence(
                    source="permission_provider",
                    description=f"Permission {permission} not found.",
                    attributes={"permission": permission, "identity": identity},
                ),),
            )
        return self._mapper.to_security_decision(domain_result)

    def check_role(self, identity: str, role: str) -> SecurityDecision:
        request = AuthorizationRequest(
            identity=identity,
            resource="role",
            operation="check_role",
        )
        roles = self._role_provider.get_roles(request)
        has_role = any(r.name == role for r in roles)
        if has_role:
            domain_result = AuthorizationResult(
                decision=AuthorizationDecisionType.ALLOW,
                rationale=f"Role '{role}' granted.",
                evidence=(AuthorizationEvidence(
                    source="role_provider",
                    description=f"Role {role} found.",
                    attributes={"role": role, "identity": identity},
                ),),
            )
        else:
            domain_result = AuthorizationResult(
                decision=AuthorizationDecisionType.DENY,
                rationale=f"Role '{role}' denied.",
                evidence=(AuthorizationEvidence(
                    source="role_provider",
                    description=f"Role {role} not found.",
                    attributes={"role": role, "identity": identity},
                ),),
            )
        return self._mapper.to_security_decision(domain_result)

    def check_constraint(self, identity: str, resource: str, constraint: str) -> SecurityDecision:
        request = AuthorizationRequest(
            identity=identity,
            resource=resource,
            operation="check_constraint",
        )
        constraints = self._constraint_provider.get_constraints(request)
        has_constraint = any(c.name == constraint for c in constraints)
        if has_constraint:
            domain_result = AuthorizationResult(
                decision=AuthorizationDecisionType.ALLOW,
                rationale=f"Constraint '{constraint}' satisfied.",
                evidence=(AuthorizationEvidence(
                    source="constraint_provider",
                    description=f"Constraint {constraint} found.",
                ),),
            )
        else:
            domain_result = AuthorizationResult(
                decision=AuthorizationDecisionType.DENY,
                rationale=f"Constraint '{constraint}' not satisfied.",
                evidence=(AuthorizationEvidence(
                    source="constraint_provider",
                    description=f"Constraint {constraint} not found.",
                ),),
            )
        return self._mapper.to_security_decision(domain_result)

    def check_obligation(self, identity: str, resource: str, obligation: str) -> SecurityDecision:
        request = AuthorizationRequest(
            identity=identity,
            resource=resource,
            operation="check_obligation",
        )
        obligations = self._obligation_provider.get_obligations(request)
        has_obligation = any(o.name == obligation for o in obligations)
        if has_obligation:
            domain_result = AuthorizationResult(
                decision=AuthorizationDecisionType.ALLOW,
                rationale=f"Obligation '{obligation}' required.",
                evidence=(AuthorizationEvidence(
                    source="obligation_provider",
                    description=f"Obligation {obligation} found.",
                ),),
            )
        else:
            domain_result = AuthorizationResult(
                decision=AuthorizationDecisionType.DENY,
                rationale=f"Obligation '{obligation}' not required.",
                evidence=(AuthorizationEvidence(
                    source="obligation_provider",
                    description=f"Obligation {obligation} not found.",
                ),),
            )
        return self._mapper.to_security_decision(domain_result)

    def allowed(self, identity: str, resource: str, operation: str) -> bool:
        decision = self.evaluate(identity, resource, operation)
        return decision.is_allowed

    def denied(self, identity: str, resource: str, operation: str) -> bool:
        return not self.allowed(identity, resource, operation)
