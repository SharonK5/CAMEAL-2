# security/trust/default_trust_engine.py
"""
Default trust engine implementation.

Computes trust scores using a weighted average of effective scores,
with automatic discounting of expired signals.
"""

from typing import Tuple

from .trust_engine import TrustEngine
from .models import TrustSignal, TrustResult, TrustLevel, TrustEvidence


class DefaultTrustEngine(TrustEngine):
    """
    Default trust engine using weighted reliability with freshness.

    Attributes:
        ENGINE_NAME: Unique identifier for this engine.
        ENGINE_VERSION: Semantic version string.
        ALGORITHM: The algorithm used for trust computation.
    """

    ENGINE_NAME = "DefaultTrustEngine"
    ENGINE_VERSION = "1.0.0"
    ALGORITHM = "weighted_reliability_with_freshness"

    def evaluate(self, signals: Tuple[TrustSignal, ...]) -> TrustResult:
        """
        Evaluate trust signals and return a TrustResult.

        Expired signals are automatically ignored (effective_score = 0).
        The overall score is a weighted average of effective scores.

        Args:
            signals: Tuple of TrustSignal objects.

        Returns:
            TrustResult: The computed trust result with evidence and metadata.
        """
        if not signals:
            return TrustResult(
                overall_score=0.0,
                trust_level=TrustLevel.NONE,
                rationale="No trust signals provided.",
                confidence=1.0,
                evidence=(TrustEvidence(
                    source=self.ENGINE_NAME,
                    description="No signals to evaluate.",
                    attributes={
                        "engine": self.ENGINE_NAME,
                        "engine_version": self.ENGINE_VERSION,
                    },
                ),),
            )

        # Separate active and expired signals
        active = [s for s in signals if not s.is_expired]
        expired_count = len(signals) - len(active)

        # Compute weighted average of effective scores using active signals
        total_effective = sum(s.effective_score for s in active)
        total_weight = sum(s.weight for s in active)
        overall_score = total_effective / total_weight if total_weight > 0 else 0.0

        trust_level = self._classify(overall_score)

        # Identify highest scoring signal (by effective score)
        highest = max(active, key=lambda s: s.effective_score) if active else None

        rationale = (
            f"Evaluated {len(active)} active signal(s) out of {len(signals)} total. "
            f"{expired_count} expired signal(s) ignored. "
            f"Overall trust score: {overall_score:.3f}. "
            f"Trust level: {trust_level.value}."
        )

        # Build evidence
        evidence_attrs = {
            "engine": self.ENGINE_NAME,
            "engine_version": self.ENGINE_VERSION,
            "algorithm": self.ALGORITHM,
            "total_signals": len(signals),
            "active_signals": len(active),
            "expired_signals": expired_count,
            "total_weight": total_weight,
            "total_effective": total_effective,
        }
        if highest:
            evidence_attrs.update({
                "highest_signal": highest.source,
                "highest_signal_score": highest.score,
                "highest_signal_reliability": highest.reliability,
            })

        evidence = (
            TrustEvidence(
                source=self.ENGINE_NAME,
                description="Trust computation using weighted reliability with freshness decay.",
                attributes=evidence_attrs,
            ),
        )

        return TrustResult(
            overall_score=overall_score,
            trust_level=trust_level,
            signals=signals,
            rationale=rationale,
            confidence=1.0,
            evidence=evidence,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _classify(score: float) -> TrustLevel:
        """
        Classify a numerical trust score into a TrustLevel.

        Thresholds (inclusive boundaries):
            - NONE:     0.00
            - LOW:      0.01 – 0.25
            - MEDIUM:   0.26 – 0.50
            - HIGH:     0.51 – 0.75
            - MAXIMUM:  0.76 – 1.00

        Args:
            score: Trust score in [0.0, 1.0].

        Returns:
            TrustLevel: The corresponding trust level.
        """
        if score == 0.0:
            return TrustLevel.NONE
        if score <= 0.25:
            return TrustLevel.LOW
        if score <= 0.50:
            return TrustLevel.MEDIUM
        if score <= 0.75:
            return TrustLevel.HIGH
        return TrustLevel.MAXIMUM

    # ------------------------------------------------------------------
    # Lifecycle (optional overrides)
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
