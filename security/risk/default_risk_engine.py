# security/risk/default_risk_engine.py
"""
Default weighted-average risk engine.

Computes an overall risk score as a weighted average of individual factor scores.
Provides classification, evidence, and metadata for explainability.

This implementation is suitable for Phase 1 and can be replaced with more
sophisticated engines (Bayesian, ML, LLM-assisted, ensemble) as the system evolves.
"""

from typing import Tuple, Optional

from .risk_engine import RiskEngine
from .models import RiskFactor, RiskResult, RiskLevel, RiskEvidence


class DefaultRiskEngine(RiskEngine):
    """
    Default risk engine using weighted average scoring.

    Attributes:
        ENGINE_NAME: Unique identifier for this engine.
        ENGINE_VERSION: Semantic version string.
        ALGORITHM: The algorithm used for risk computation.
    """

    ENGINE_NAME = "DefaultRiskEngine"
    ENGINE_VERSION = "1.0.0"
    ALGORITHM = "weighted_average"

    def __init__(self) -> None:
        """Initialize the default risk engine."""
        # Future configuration can be added here.

    # ------------------------------------------------------------------
    # Engine lifecycle
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        """Initialize engine resources."""
        pass

    def shutdown(self) -> None:
        """Release engine resources."""
        pass

    def validate(self) -> None:
        """Validate engine configuration."""
        pass

    def health(self) -> bool:
        """Return engine health."""
        return True

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def engine_name(self) -> str:
        return self.ENGINE_NAME

    @property
    def version(self) -> str:
        return self.ENGINE_VERSION

    # ------------------------------------------------------------------
    # Core evaluation
    # ------------------------------------------------------------------

    def evaluate(self, factors: Tuple[RiskFactor, ...]) -> RiskResult:
        """
        Evaluate risk factors and return a RiskResult.

        The overall score is a weighted average of factor scores.
        The classification uses fixed thresholds (see _classify).

        Confidence is set to 1.0 as a placeholder. In future releases,
        confidence will be derived from evidence quality, model reliability,
        or empirical validation.

        Args:
            factors: Tuple of RiskFactor objects.

        Returns:
            RiskResult: The computed risk result with evidence and metadata.
        """
        # Handle empty input
        if not factors:
            return RiskResult(
                overall_score=0.0,
                risk_level=RiskLevel.NONE,
                rationale="No risk factors provided.",
                confidence=1.0,
                evidence=(RiskEvidence(
                    source=self.ENGINE_NAME,
                    description="No factors to evaluate.",
                    attributes={
                        "engine": self.ENGINE_NAME,
                        "engine_version": self.ENGINE_VERSION,
                        "algorithm": self.ALGORITHM,
                    },
                ),),
            )

        # Compute total weight and weighted sum
        total_weight = sum(f.weight for f in factors)
        total_weighted = sum(f.weighted_score for f in factors)
        overall_score = total_weighted / total_weight if total_weight > 0 else 0.0

        # Classify the score
        risk_level = self._classify(overall_score)

        # Identify the highest risk factor
        highest_factor = max(factors, key=lambda f: f.score)

        # Prepare rationale
        rationale = (
            f"Evaluated {len(factors)} factor(s). "
            f"Overall score: {overall_score:.3f}. "
            f"Risk level: {risk_level.value}."
        )

        # Confidence placeholder: always 1.0 for Phase 1
        # Future versions may compute confidence from factor certainty, model reliability, etc.
        confidence = 1.0

        # Build evidence
        evidence = (
            RiskEvidence(
                source=self.ENGINE_NAME,
                description="Risk computation using weighted average.",
                attributes={
                    "engine": self.ENGINE_NAME,
                    "engine_version": self.ENGINE_VERSION,
                    "algorithm": self.ALGORITHM,
                    "factor_count": len(factors),
                    "total_weight": total_weight,
                    "highest_factor": highest_factor.name,
                    "highest_factor_score": highest_factor.score,
                },
            ),
        )

        return RiskResult(
            overall_score=overall_score,
            risk_level=risk_level,
            factors=factors,
            rationale=rationale,
            confidence=confidence,
            evidence=evidence,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _classify(score: float) -> RiskLevel:
        """
        Classify a numerical risk score into a RiskLevel.

        Thresholds:
            - NONE:     0.00
            - LOW:      0.01 – 0.24
            - MEDIUM:   0.25 – 0.49
            - HIGH:     0.50 – 0.74
            - CRITICAL: 0.75 – 1.00

        Args:
            score: Risk score in [0.0, 1.0].

        Returns:
            RiskLevel: The corresponding risk level.
        """
        if score == 0.0:
            return RiskLevel.NONE
        if score < 0.25:
            return RiskLevel.LOW
        if score < 0.50:
            return RiskLevel.MEDIUM
        if score < 0.75:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL
