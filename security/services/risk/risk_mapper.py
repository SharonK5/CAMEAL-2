# security/services/risk/risk_mapper.py
from uuid import uuid4
from datetime import datetime, timezone

from security.services.base.security_decision import SecurityDecision, DecisionType, Evidence
from security.risk.models import RiskResult


class RiskMapper:
    @staticmethod
    def to_security_decision(risk_result: RiskResult) -> SecurityDecision:
        if risk_result.is_acceptable:
            decision = DecisionType.ABSTAIN
            rationale = f"Risk acceptable: {risk_result.risk_level.value}."
        else:
            decision = DecisionType.DENY
            rationale = f"Risk too high: {risk_result.risk_level.value}."

        evidence_list = []
        for factor in risk_result.factors:
            evidence_list.append(
                Evidence(
                    source="risk_mapper",
                    data={
                        "factor": factor.name,
                        "score": factor.score,
                        "weight": factor.weight,
                    },
                    timestamp=datetime.now(timezone.utc),
                    evidence_id=uuid4(),
                )
            )

        for ev in risk_result.evidence:
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
                    source="risk_mapper",
                    data={"default": True},
                    timestamp=datetime.now(timezone.utc),
                    evidence_id=uuid4(),
                )
            )

        return SecurityDecision(
            decision=decision,
            confidence=risk_result.confidence,
            rationale=rationale,
            evidence=tuple(evidence_list),
            recommendations=(),
            audit_metadata={
                "request_id": str(risk_result.request_id),
                "created_at": risk_result.created_at.isoformat(),
                "overall_score": risk_result.overall_score,
                "risk_level": risk_result.risk_level.value,
                "factor_count": risk_result.factor_count,
                "total_weight": risk_result.total_weight,
            },
        )
