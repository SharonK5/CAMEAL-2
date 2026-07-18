# security/trust/default_trust_provider.py
from typing import Any, Optional, Tuple

from .trust_provider import TrustProvider
from .models import TrustSignal, TrustSignalType, TrustRequest, Provenance


class DefaultTrustProvider(TrustProvider):
    PROVIDER_NAME = "DefaultTrustProvider"
    PROVIDER_VERSION = "1.0.0"

    def get_signals(
        self,
        request: TrustRequest,
        previous_results: Optional[dict[str, Any]] = None,
    ) -> Tuple[TrustSignal, ...]:
        # In a real implementation, this would extract signals from
        # AuthenticationResult, AuthorizationResult, PolicyResult, RiskResult, AuditResult.
        # For now, we provide a sensible stub.
        signals = []

        # Example: if authentication result is available, create a signal
        if previous_results and "authentication" in previous_results:
            auth_result = previous_results["authentication"]
            signals.append(
                TrustSignal(
                    signal_type=TrustSignalType.AUTHENTICATION,
                    score=auth_result.get("confidence", 0.8),
                    weight=1.0,
                    reliability=0.9,
                    source="Authentication",
                    provenance=Provenance(
                        source_type="SERVICE",
                        source_id="authentication.default",
                        version="1.0.0",
                        authority="CAMEAL",
                    ),
                    valid_from=datetime.now(timezone.utc),
                    valid_until=datetime.now(timezone.utc) + timedelta(days=1),
                    description="Authentication signal",
                )
            )

        # Always provide a default signal for fallback
        if not signals:
            signals.append(
                TrustSignal(
                    signal_type=TrustSignalType.BEHAVIOR,
                    score=0.7,
                    weight=1.0,
                    reliability=0.8,
                    source=self.PROVIDER_NAME,
                    provenance=Provenance(
                        source_type="PROVIDER",
                        source_id="trust.default",
                        version=self.PROVIDER_VERSION,
                    ),
                    valid_from=datetime.now(timezone.utc),
                    valid_until=datetime.now(timezone.utc) + timedelta(hours=1),
                    description="Default trust signal.",
                )
            )

        return tuple(signals)
