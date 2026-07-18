# security/orchestration/tests/test_orchestration.py
import pytest
from unittest.mock import Mock
from datetime import datetime, timezone
from uuid import uuid4

from security.orchestration.models import (
    OrchestrationContext,
    ServiceResult,
    OrchestrationResult,
    Provenance,
    EvidenceBundle,
    EscalationReason,
    OrchestrationDecisionType,
)
from security.orchestration.decision_pipeline import DecisionPipeline
from security.orchestration.decision_fusion import DecisionFusion
from security.orchestration.recommendation_engine import RecommendationEngine
from security.services.base.security_decision import SecurityDecision, DecisionType, Evidence
from security.services.base.security_context import SecurityContext


def _decision(decision_type: DecisionType, confidence: float, rationale: str) -> SecurityDecision:
    """Helper to create a valid SecurityDecision with evidence."""
    evidence = (Evidence(source="test", data={"test": True}),)
    return SecurityDecision(
        decision=decision_type,
        confidence=confidence,
        rationale=rationale,
        evidence=evidence,
    )


def test_pipeline_execution():
    authn = Mock()
    authn.authenticate.return_value = _decision(DecisionType.ALLOW, 0.9, "OK")
    authz = Mock()
    authz.authorize.return_value = _decision(DecisionType.ALLOW, 0.8, "OK")
    policy = Mock()
    policy.evaluate.return_value = _decision(DecisionType.ALLOW, 0.7, "OK")
    risk = Mock()
    risk.evaluate.return_value = _decision(DecisionType.ABSTAIN, 0.5, "OK")
    audit = Mock()
    audit.log_event.return_value = _decision(DecisionType.ALLOW, 1.0, "OK")
    trust = Mock()
    trust.evaluate.return_value = _decision(DecisionType.ALLOW, 0.6, "OK")

    pipeline = DecisionPipeline(
        authentication_service=authn,
        authorization_service=authz,
        policy_service=policy,
        risk_service=risk,
        audit_service=audit,
        trust_service=trust,
        service_versions={"authentication": "2.0.0"},
    )

    context = SecurityContext(identity="alice", resource="/doc", operation="read")
    result = pipeline.execute(context)

    assert isinstance(result, OrchestrationResult)
    assert result.decision in (OrchestrationDecisionType.ALLOW, OrchestrationDecisionType.REVIEW, OrchestrationDecisionType.DENY)
    assert len(result.evidence_bundle.service_results) == 6
    assert result.confidence >= 0.0 and result.confidence <= 1.0
    assert len(result.decision_trace) > 0


def test_fusion_allow():
    fusion = DecisionFusion()
    p = Provenance(service_name="test", service_version="1.0", engine_name="test", engine_version="1.0")
    ctx = OrchestrationContext(identity="alice", resource="/doc", operation="read")
    ctx = ctx.add_service_result(
        "authn",
        ServiceResult(
            provenance=p,
            decision=_decision(DecisionType.ALLOW, 0.9, "OK"),
            execution_time_ms=0,
        ),
    ).add_service_result(
        "authz",
        ServiceResult(
            provenance=p,
            decision=_decision(DecisionType.ALLOW, 0.8, "OK"),
            execution_time_ms=0,
        ),
    )
    final, reasons, conf = fusion.fuse(ctx)
    assert final == OrchestrationDecisionType.ALLOW
    assert len(reasons) == 0


def test_fusion_deny():
    fusion = DecisionFusion()
    p = Provenance(service_name="test", service_version="1.0", engine_name="test", engine_version="1.0")
    ctx = OrchestrationContext(identity="alice", resource="/doc", operation="read")
    ctx = ctx.add_service_result(
        "authn",
        ServiceResult(
            provenance=p,
            decision=_decision(DecisionType.ALLOW, 0.9, "OK"),
            execution_time_ms=0,
        ),
    ).add_service_result(
        "authz",
        ServiceResult(
            provenance=p,
            decision=_decision(DecisionType.DENY, 0.8, "Denied"),
            execution_time_ms=0,
        ),
    ).add_service_result(
        "policy",
        ServiceResult(
            provenance=p,
            decision=_decision(DecisionType.DENY, 0.7, "Denied"),
            execution_time_ms=0,
        ),
    )
    final, reasons, conf = fusion.fuse(ctx)
    assert final == OrchestrationDecisionType.DENY
    assert EscalationReason.CONFLICTING_EVIDENCE in reasons


def test_fusion_review_on_tie():
    fusion = DecisionFusion()
    p = Provenance(service_name="test", service_version="1.0", engine_name="test", engine_version="1.0")
    ctx = OrchestrationContext(identity="alice", resource="/doc", operation="read")
    ctx = ctx.add_service_result(
        "authn",
        ServiceResult(
            provenance=p,
            decision=_decision(DecisionType.ALLOW, 0.9, "OK"),
            execution_time_ms=0,
        ),
    ).add_service_result(
        "authz",
        ServiceResult(
            provenance=p,
            decision=_decision(DecisionType.DENY, 0.8, "Denied"),
            execution_time_ms=0,
        ),
    )
    final, reasons, conf = fusion.fuse(ctx)
    assert final == OrchestrationDecisionType.REVIEW
    assert EscalationReason.CONFLICTING_EVIDENCE in reasons


def test_recommendation_engine():
    eng = RecommendationEngine()
    recs = eng.generate(
        ctx=OrchestrationContext(identity="alice", resource="/doc", operation="read"),
        decision=OrchestrationDecisionType.REVIEW,
        escalation_reasons=(EscalationReason.HIGH_RISK, EscalationReason.LOW_TRUST),
    )
    assert len(recs) >= 2
    assert "Review risk assessment" in " ".join(recs)
    assert "Review trust signals" in " ".join(recs)
