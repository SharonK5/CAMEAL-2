# security/services/audit/default_audit_service.py
from __future__ import annotations

from typing import Any, Tuple

from security.services.base.security_context import SecurityContext
from security.services.base.security_decision import SecurityDecision
from security.services.base.lifecycle import HealthStatus

from security.audit.audit_provider import AuditProvider
from security.audit.audit_engine import AuditEngine
from security.audit.models import (
    AuditRequest,
    AuditEvent,
    AuditCategory,
    AuditSeverity,
    AuditOutcome,
)

from .audit_service import AuditService
from .audit_mapper import AuditMapper


class DefaultAuditService(AuditService):
    VERSION = "1.0.0"
    NAME = "default_audit"
    DOMAIN = "audit"

    def __init__(
        self,
        audit_provider: AuditProvider,
        audit_engine: AuditEngine,
    ) -> None:
        super().__init__()
        self._audit_provider = audit_provider
        self._audit_engine = audit_engine
        self._mapper = AuditMapper()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def _on_initialize(self) -> None:
        self._audit_provider.initialize()
        self._audit_engine.initialize()

    def _on_validate(self) -> None:
        self._audit_provider.validate()
        self._audit_engine.validate()

    def _on_start(self) -> None:
        pass

    def _on_shutdown(self) -> None:
        self._audit_provider.shutdown()
        self._audit_engine.shutdown()

    def _on_dispose(self) -> None:
        pass

    def _on_health(self) -> HealthStatus:
        statuses = [
            self._audit_provider.health(),
            self._audit_engine.health(),
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
    # Public API
    # ------------------------------------------------------------------

    def log_event(self, context: SecurityContext, **kwargs: Any) -> SecurityDecision:
        request = AuditRequest(
            identity=context.identity,
            resource=context.resource,
            operation=context.operation,
            category=kwargs.get("category", AuditCategory.SYSTEM),
            metadata=dict(context.metadata) | kwargs.get("request_metadata", {}),
        )

        event = self._audit_engine.build_event(request)

        result = self._audit_provider.record(request, event)

        return self._mapper.to_security_decision(result)

    def query_events(self, filters: dict[str, Any]) -> Tuple[AuditEvent, ...]:
        if hasattr(self._audit_provider, "query"):
            return self._audit_provider.query(filters)  # type: ignore
        return ()
