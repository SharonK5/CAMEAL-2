# security/orchestration/decision_fusion.py
from typing import Tuple
from .models import OrchestrationContext, OrchestrationDecisionType, EscalationReason


class DecisionFusion:
    """
    Fuses outputs from multiple security services into a single decision.
    """

    def fuse(self, ctx: OrchestrationContext) -> Tuple[OrchestrationDecisionType, Tuple[EscalationReason, ...], float]:
        # Collect all non-error results
        results = []
        for name, result in ctx.service_results.items():
            if not result.error:
                results.append((name, result))

        if not results:
            return (
                OrchestrationDecisionType.DENY,
                (EscalationReason.CONFLICTING_EVIDENCE,),
                0.0,
            )

        # Count decisions
        allows = 0
        denies = 0
        abstains = 0
        total_confidence = 0.0
        escalation_set = set()

        for name, result in results:
            if result.decision.decision.value == "ALLOW":
                allows += 1
            elif result.decision.decision.value == "DENY":
                denies += 1
            else:
                abstains += 1
            total_confidence += result.decision.confidence

        avg_confidence = total_confidence / len(results)

        # Determine final decision
        if denies > allows:
            final = OrchestrationDecisionType.DENY
            escalation_set.add(EscalationReason.CONFLICTING_EVIDENCE)
        elif allows > denies:
            final = OrchestrationDecisionType.ALLOW
        else:
            if abstains == len(results):
                final = OrchestrationDecisionType.REVIEW
                escalation_set.add(EscalationReason.HUMAN_REQUIRED)
            else:
                final = OrchestrationDecisionType.REVIEW
                escalation_set.add(EscalationReason.CONFLICTING_EVIDENCE)

        # Check for high risk
        if "risk" in ctx.service_results and ctx.service_results["risk"].decision.decision.value == "DENY":
            if final == OrchestrationDecisionType.ALLOW:
                final = OrchestrationDecisionType.REVIEW
                escalation_set.add(EscalationReason.HIGH_RISK)

        # Check for low trust
        if "trust" in ctx.service_results and ctx.service_results["trust"].decision.confidence < 0.4:
            if final == OrchestrationDecisionType.ALLOW:
                final = OrchestrationDecisionType.REVIEW
                escalation_set.add(EscalationReason.LOW_TRUST)

        # Check for low confidence
        if avg_confidence < 0.5 and final == OrchestrationDecisionType.ALLOW:
            final = OrchestrationDecisionType.REVIEW
            escalation_set.add(EscalationReason.LOW_CONFIDENCE)

        # Add other reasons based on specific service failures
        if "authentication" in ctx.service_results and ctx.service_results["authentication"].error:
            escalation_set.add(EscalationReason.AUTHENTICATION_FAILURE)
        if "authorization" in ctx.service_results and ctx.service_results["authorization"].error:
            escalation_set.add(EscalationReason.AUTHORIZATION_FAILURE)
        if "policy" in ctx.service_results and ctx.service_results["policy"].error:
            escalation_set.add(EscalationReason.POLICY_VIOLATION)

        return final, tuple(escalation_set), avg_confidence  # FIXED: was avg_confidenceo
