# security/services/audit/audit_service.py
from __future__ import annotations

from abc import abstractmethod
from typing import Any, Tuple

from security.services.base.security_context import SecurityContext
from security.services.base.security_decision import SecurityDecision
from security.services.base.service import Service
from security.audit.models import AuditEvent


class AuditService(Service):
    @property
    def security_domain(self) -> str:
        return "audit"

    @abstractmethod
    def log_event(self, context: SecurityContext, **kwargs: Any) -> SecurityDecision:
        pass

    @abstractmethod
    def query_events(self, filters: dict[str, Any]) -> Tuple[AuditEvent, ...]:
        pass
