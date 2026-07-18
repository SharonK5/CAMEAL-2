# security/orchestration/recommendation_engine.py
from typing import Tuple
from .models import OrchestrationContext, OrchestrationDecisionType, EscalationReason


class RecommendationEngine:
    def generate(self, ctx: OrchestrationContext, decision: OrchestrationDecisionType, escalation_reasons: Tuple[EscalationReason, ...]) -> Tuple[str, ...]:
        recommendations = []

        if EscalationReason.HIGH_RISK in escalation_reasons:
            recommendations.append("Review risk assessment details.")
        if EscalationReason.LOW_TRUST in escalation_reasons:
            recommendations.append("Review trust signals and provenance.")
        if EscalationReason.CONFLICTING_EVIDENCE in escalation_reasons:
            recommendations.append("Reconcile conflicting service outputs.")
        if EscalationReason.HUMAN_REQUIRED in escalation_reasons:
            recommendations.append("Mandatory human review required.")
        if EscalationReason.LOW_CONFIDENCE in escalation_reasons:
            recommendations.append("Overall confidence is low; verify service outputs.")
        if EscalationReason.AUTHENTICATION_FAILURE in escalation_reasons:
            recommendations.append("Authentication service failed; check identity.")
        if EscalationReason.AUTHORIZATION_FAILURE in escalation_reasons:
            recommendations.append("Authorization service failed; check permissions.")
        if EscalationReason.POLICY_VIOLATION in escalation_reasons:
            recommendations.append("Policy violation detected; review policy rules.")

        if decision == OrchestrationDecisionType.REVIEW:
            recommendations.append("Escalate to human operator.")
        elif decision == OrchestrationDecisionType.DENY:
            recommendations.append("Investigate denial reasons.")
        elif decision == OrchestrationDecisionType.ALLOW:
            recommendations.append("Proceed with confidence.")

        if not recommendations:
            recommendations.append("No specific actions required.")

        return tuple(recommendations)
