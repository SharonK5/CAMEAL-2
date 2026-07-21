# kernel/context/provenance_context.py
"""
Provenance context – evidence lineage.
"""

from dataclasses import dataclass, field
from typing import Dict, List

from .exceptions import ContextValidationError


@dataclass(frozen=True)
class ProvenanceContext:
    """
    Immutable provenance context.

    Attributes:
        evidence_ids: List of evidence identifiers.
        sources: Source components.
        timestamps: Event timestamps.
        confidence: Confidence scores.
        metadata: Additional provenance metadata.
    """

    evidence_ids: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    timestamps: List[str] = field(default_factory=list)
    confidence: float = 1.0
    metadata: Dict[str, str] = field(default_factory=dict)

    def add_evidence(self, evidence_id: str, source: str, timestamp: str) -> "ProvenanceContext":
        """Create a new context with added evidence."""
        return ProvenanceContext(
            evidence_ids=self.evidence_ids + [evidence_id],
            sources=self.sources + [source],
            timestamps=self.timestamps + [timestamp],
            confidence=self.confidence,
            metadata=self.metadata,
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "evidence_ids": list(self.evidence_ids),
            "sources": list(self.sources),
            "timestamps": list(self.timestamps),
            "confidence": str(self.confidence),
            **self.metadata,
        }
