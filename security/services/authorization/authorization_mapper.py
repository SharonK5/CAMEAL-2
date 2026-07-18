# security/services/authorization/authorization_mapper.py
"""
Mapper for converting authorization domain objects to service-layer objects.
"""

from security.services.base.security_decision import SecurityDecision, DecisionType, Evidence
from security.authorization.models import AuthorizationResult, AuthorizationDecisionType, AuthorizationEvidence


class AuthorizationMapper:
    """
    Converts AuthorizationResult to SecurityDecision.
    """

    @staticmethod
    def to_security_decision(domain_result: AuthorizationResult) -> SecurityDecision:
        """
        Convert an AuthorizationResult to a SecurityDecision.

        Args:
            domain_result: The domain authorization result.

        Returns:
            SecurityDecision: The service-layer decision.
        """
        decision = DecisionType.ALLOW if domain_result.allowed else DecisionType.DENY

        # Convert AuthorizationEvidence to service-layer Evidence
        evidence_list = []
        for ev in domain_result.evidence:
            if isinstance(ev, AuthorizationEvidence):
                evidence_list.append(
                    Evidence(
                        source=ev.source,
                        data=dict(ev.attributes),
                        timestamp=ev.timestamp,
                    )
                )
            elif isinstance(ev, dict):
                # Fallback for raw dicts
                evidence_list.append(
                    Evidence(
                        source=ev.get("source", "unknown"),
                        data=ev.get("attributes", {}),
                        timestamp=ev.get("timestamp", domain_result.created_at),
                    )
                )
            else:
                # Unstructured evidence
                evidence_list.append(
                    Evidence(
                        source=str(ev),
                        data={},
                        timestamp=domain_result.created_at,
                    )
                )

        # Ensure evidence exists for ALLOW/DENY decisions
        if not evidence_list and domain_result.decision in (AuthorizationDecisionType.ALLOW, AuthorizationDecisionType.DENY):
            evidence_list.append(
                Evidence(
                    source="authorization_mapper",
                    data={"default": True},
                    timestamp=domain_result.created_at,
                )
            )

        rationale = domain_result.rationale or "Authorization decision."

        return SecurityDecision(
            decision=decision,
            confidence=domain_result.confidence,
            rationale=rationale,
            evidence=tuple(evidence_list),      # tuple of Evidence objects
            recommendations=(),                 # empty tuple
            audit_metadata={
                "request_id": str(domain_result.request_id),
                "created_at": domain_result.created_at.isoformat(),
                "permissions": list(domain_result.permission_names),
                "roles": list(domain_result.role_names),
                "constraints": [c.name for c in domain_result.constraints],
                "obligations": [o.name for o in domain_result.obligations],
            },
        )
