# security/policy/policy_provider.py
from __future__ import annotations

from abc import abstractmethod
from typing import Tuple

from .provider import PolicyProvider
from .models import Policy, PolicyRequest


class PolicyRepositoryProvider(PolicyProvider):
    """
    Supplies policies applicable to a request.

    Implementations may load policies from:
    - YAML / JSON files
    - Database
    - Git repository
    - REST API
    - OPA bundle
    - Cedar store
    """

    PROVIDER_NAME = "PolicyRepositoryProvider"
    PROVIDER_VERSION = "1.0.0"

    @abstractmethod
    def get_policies(self, request: PolicyRequest) -> Tuple[Policy, ...]:
        """
        Retrieve policies applicable to the request.
        """
        raise NotImplementedError
