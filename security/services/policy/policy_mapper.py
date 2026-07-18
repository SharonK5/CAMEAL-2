# security/services/policy/policy_mapper.py
"""
Mapper for converting policy domain objects to service-layer objects.
"""

from uuid import uuid4
from datetime import datetime, timezone

from security.services.base.security_decision import SecurityDecision, DecisionType, Evidence
from security.policy.models import PolicyResult, PolicyDecisionType


class PolicyMapper:
    @staticmethod
    def to_security_decision(policy_result: PolicyResult) -> SecurityDecision:
        # Map policy decision to service decision
        if policy_result.decision == PolicyDecisionType.ALLOW:
            decision = DecisionType.ALLOW
        elif policy_result.decision == PolicyDecisionType.DENY:
            decision = DecisionType.DENY
        else:  # NOT_APPLICABLE
            decision = DecisionType.ABSTAIN

        # Convert PolicyEvidence to Evidence
        evidence_list = []
        for policy_ev in policy_result.evidence:
            evidence_list.append(
                Evidence(
                    source=policy_ev.source,
                    data=dict(policy_ev.details),
                    timestamp=policy_ev.timestamp,
                    evidence_id=uuid4(),
                )
            )

        # If no evidence, add a default one
        if not evidence_list:
            evidence_list.append(
                Evidence(
                    source="policy_mapper",
                    data={"default": True},
                    timestamp=datetime.now(timezone.utc),
                    evidence_id=uuid4(),
                )
            )

        rationale = policy_result.rationale or "Policy decision."

        return SecurityDecision(
            decision=decision,
            confidence=policy_result.confidence,
            rationale=rationale,
            evidence=tuple(evidence_list),
            recommendations=(),
            audit_metadata={
                "request_id": str(policy_result.request_id),
                "created_at": policy_result.created_at.isoformat(),
                "execution_time_ms": policy_result.execution_time_ms,
                "policies_applied": list(policy_result.policy_names),
                "rules_applied": list(policy_result.rule_names),
            },
        )
