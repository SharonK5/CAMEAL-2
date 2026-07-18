# security/trust/trust_engine.py
from abc import ABC, abstractmethod
from typing import Tuple

from .models import TrustSignal, TrustResult


class TrustEngine(ABC):
    @abstractmethod
    def evaluate(self, signals: Tuple[TrustSignal, ...]) -> TrustResult:
        pass

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def validate(self) -> None:
        pass

    def health(self) -> bool:
        return True
