# security/audit/default_audit_engine.py
from .audit_engine import AuditEngine
from .models import AuditEvent, AuditRequest, AuditSeverity, AuditOutcome


class DefaultAuditEngine(AuditEngine):
    ENGINE_NAME = "DefaultAuditEngine"
    ENGINE_VERSION = "1.0.0"

    def build_event(self, request: AuditRequest) -> AuditEvent:
        return AuditEvent(
            request_id=request.metadata.get("request_id"),
            category=request.category,
            severity=AuditSeverity.INFO,
            outcome=AuditOutcome.SUCCESS,
            identity=request.identity,
            resource=request.resource,
            operation=request.operation,
            details={
                "engine": self.ENGINE_NAME,
                "version": self.ENGINE_VERSION,
            },
        )

    def health(self) -> bool:
        return True
