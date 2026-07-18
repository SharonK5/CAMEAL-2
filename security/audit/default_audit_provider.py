# security/audit/default_audit_provider.py
from .audit_provider import AuditProvider
from .models import AuditEvent, AuditRequest, AuditResult, AuditEvidence


class DefaultAuditProvider(AuditProvider):
    """
    Default in-memory audit provider.

    Intended for development and testing.
    """

    PROVIDER_NAME = "DefaultAuditProvider"
    PROVIDER_VERSION = "1.0.0"

    def record(self, request: AuditRequest, event: AuditEvent) -> AuditResult:
        return AuditResult(
            success=True,
            request_id=event.request_id,
            event_id=event.event_id,
            message="Audit event recorded.",
            evidence=(
                AuditEvidence(
                    source=self.provider_name,
                    description="Audit successfully recorded.",
                    attributes={
                        "provider_version": self.provider_version,
                        "category": event.category.value,
                        "severity": event.severity.value,
                    },
                ),
            ),
        )
