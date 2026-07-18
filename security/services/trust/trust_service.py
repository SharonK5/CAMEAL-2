# security/services/trust/trust_service.py
from __future__ import annotations

from abc import abstractmethod

from security.services.base.security_context import SecurityContext
from security.services.base.security_decision import SecurityDecision
from security.services.base.service import Service


class TrustService(Service):
    @property
    def security_domain(self) -> str:
        return "trust"

    @abstractmethod
    def evaluate(self, context: SecurityContext) -> SecurityDecision:
        pass
