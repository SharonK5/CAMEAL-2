# security/policy/default_rule_provider.py
from __future__ import annotations

from typing import Tuple

from .rule_provider import RuleProvider
from .models import PolicyRule, PolicyRequest, PolicyEffect


class DefaultRuleProvider(RuleProvider):
    """
    Default rule provider that returns a single allow rule.
    """

    PROVIDER_NAME = "DefaultRuleProvider"
    PROVIDER_VERSION = "1.0.0"

    def get_rules(self, request: PolicyRequest) -> Tuple[PolicyRule, ...]:
        return (
            PolicyRule(
                name="default_allow",
                effect=PolicyEffect.PERMIT,
                description="Default allow rule.",
            ),
        )
