# security/risk/risk_engine.py
from abc import ABC, abstractmethod
from typing import Tuple

from .models import RiskFactor, RiskResult


class RiskEngine(ABC):
    """
    Abstract base for risk engines.

    Evaluates risk factors and returns a RiskResult.
    """

    @abstractmethod
    def evaluate(self, factors: Tuple[RiskFactor, ...]) -> RiskResult:
        """
        Evaluate risk factors and return a RiskResult.

        Args:
            factors: Tuple of RiskFactor objects.

        Returns:
            RiskResult: The computed risk result.
        """
        pass

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
