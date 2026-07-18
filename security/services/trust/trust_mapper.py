# security/services/trust/trust_mapper.py
"""
Mapper for converting trust domain objects to service-layer objects.
"""

from uuid import uuid4
from datetime import datetime, timezone

from security.services.base.security_decision import SecurityDecision, DecisionType, Evidence
from security.trust.models import TrustResult


class TrustMapper:
    """
    Converts TrustResult to SecurityDecision.
    """

    @staticmethod
    def to_security_decision(trust_result: TrustResult) -> SecurityDecision:
        """
        Convert a TrustResult to a SecurityDecision.

        Args:
            trust_result: The domain trust result.

        Returns:
            SecurityDecision: The service-layer decision.
        """
        decision = DecisionType.ALLOW if trust_result.is_acceptable else DecisionType.DENY
        rationale = f"Trust {trust_result.trust_level.value}: {trust_result.rationale}"

        evidence_list = []
        for signal in trust_result.signals:
            evidence_list.append(
                Evidence(
                    source=signal.source,
                    data={
                        "signal_type": signal.signal_type.value,
                        "score": signal.score,
                        "weight": signal.weight,
                        "reliability": signal.reliability,
                        "effective_score": signal.effective_score,
                        "provenance": signal.provenance.to_dict(),
                    },
                    timestamp=datetime.now(timezone.utc),
                    evidence_id=uuid4(),
                )
            )

        for ev in trust_result.evidence:
            evidence_list.append(
                Evidence(
                    source=ev.source,
                    data=dict(ev.attributes),
                    timestamp=ev.timestamp,
                    evidence_id=uuid4(),
                )
            )

        if not evidence_list:
            evidence_list.append(
                Evidence(
                    source="trust_mapper",
                    data={"default": True},
                    timestamp=datetime.now(timezone.utc),
                    evidence_id=uuid4(),
                )
            )

        return SecurityDecision(
            decision=decision,
            confidence=trust_result.confidence,
            rationale=rationale,
            evidence=tuple(evidence_list),
            recommendations=(),
            audit_metadata={
                "request_id": str(trust_result.request_id),
                "created_at": trust_result.created_at.isoformat(),
                "overall_score": trust_result.overall_score,
                "trust_level": trust_result.trust_level.value,
                "signal_count": trust_result.signal_count,
                "total_weight": trust_result.total_weight,
                "total_effective_score": trust_result.total_effective_score,
            },
        )
