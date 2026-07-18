# security/services/audit/audit_mapper.py
from datetime import datetime, timezone
from uuid import uuid4

from security.services.base.security_decision import SecurityDecision, DecisionType, Evidence
from security.audit.models import AuditResult


class AuditMapper:
    @staticmethod
    def to_security_decision(result: AuditResult) -> SecurityDecision:
        decision = DecisionType.ALLOW if result.success else DecisionType.DENY

        evidence = []
        for ev in result.evidence:
            evidence.append(
                Evidence(
                    source=ev.source,
                    data=dict(ev.attributes),
                    timestamp=ev.timestamp,
                    evidence_id=uuid4(),
                )
            )

        if not evidence:
            evidence.append(
                Evidence(
                    source="audit_mapper",
                    data={"default": True},
                    timestamp=datetime.now(timezone.utc),
                    evidence_id=uuid4(),
                )
            )

        return SecurityDecision(
            decision=decision,
            confidence=1.0,
            rationale=result.message or "Audit event logged.",
            evidence=tuple(evidence),
            recommendations=(),
            audit_metadata={
                "request_id": str(result.request_id),
                "event_id": str(result.event_id) if result.event_id else None,
                "created_at": result.created_at.isoformat(),
            },
        )
