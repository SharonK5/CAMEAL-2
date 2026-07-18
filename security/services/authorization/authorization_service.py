# security/services/authorization/authorization_service.py
from __future__ import annotations

from abc import ABC, abstractmethod

from security.services.base.security_context import SecurityContext
from security.services.base.security_decision import SecurityDecision
from security.services.base.service import Service


class AuthorizationService(Service):
    @property
    def security_domain(self) -> str:
        return "authorization"

    @abstractmethod
    def authorize(self, context: SecurityContext) -> SecurityDecision:
        pass

    @abstractmethod
    def check_permission(self, identity: str, permission: str, resource: str) -> SecurityDecision:
        pass

    @abstractmethod
    def check_role(self, identity: str, role: str) -> SecurityDecision:
        pass

    @abstractmethod
    def check_constraint(self, identity: str, resource: str, constraint: str) -> SecurityDecision:
        pass

    @abstractmethod
    def check_obligation(self, identity: str, resource: str, obligation: str) -> SecurityDecision:
        pass

    @abstractmethod
    def evaluate(self, identity: str, resource: str, operation: str) -> SecurityDecision:
        pass

    @abstractmethod
    def allowed(self, identity: str, resource: str, operation: str) -> bool:
        pass

    @abstractmethod
    def denied(self, identity: str, resource: str, operation: str) -> bool:
        pass
