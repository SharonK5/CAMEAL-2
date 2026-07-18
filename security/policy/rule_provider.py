# security/policy/rule_provider.py
from __future__ import annotations

from abc import abstractmethod
from typing import Tuple

from .provider import PolicyProvider
from .models import PolicyRule, PolicyRequest


class RuleProvider(PolicyProvider):
    """
    Supplies rules applicable to a request.

    Implementations may load rules from external stores or generate them dynamically.
    """

    PROVIDER_NAME = "RuleProvider"
    PROVIDER_VERSION = "1.0.0"

    @abstractmethod
    def get_rules(self, request: PolicyRequest) -> Tuple[PolicyRule, ...]:
        """
        Retrieve rules applicable to the request.
        """
        raise NotImplementedError
