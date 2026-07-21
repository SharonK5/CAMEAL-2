import logging
# kernel/providers/model/implementations/mock_model_provider.py
"""
Mock model provider for testing.
"""

import json
from typing import Any, Dict, Optional

from ..model_provider import ModelProvider
from kernel.lifecycle import HealthStatus
from ...base.exceptions import ProviderInitializationError, ProviderError

logger = logging.getLogger(__name__)


class MockModelProvider(ModelProvider):
    """
    Mock model provider for testing.

    This provider simulates a model without requiring any ML libraries.
    It can return configurable predictions and is useful for testing.

    Usage:
        provider = MockModelProvider()
        provider.load("dummy_path")
        prediction = provider.predict({"input": "test"})
    """

    def __init__(self, default_output: Any = "mock prediction"):
        self._default_output = default_output
        self._model = None
        self._metadata = {}
        self._loaded = False

    def get(self) -> Any:
        """Return the mock model."""
        return self._model

    def start(self) -> None:
        """Initialize the mock provider."""
        self._loaded = False

    def stop(self) -> None:
        """Clean up the mock provider."""
        self._model = None
        self._loaded = False

    def health(self) -> HealthStatus:
        """Check if the mock provider is healthy."""
        return HealthStatus.HEALTHY

    def load(self, model_path: str, **kwargs) -> None:
        """
        Load a mock model.

        Args:
            model_path: Path to model file (not actually used).
            **kwargs: Metadata override.

        Raises:
            ProviderInitializationError: If the path is invalid (simulated).
        """
        if not model_path:
            raise ProviderInitializationError("Model path is required")

        self._model = {"path": model_path, "loaded": True}
        self._metadata = {
            "name": kwargs.get("name", "mock_model"),
            "version": kwargs.get("version", "1.0.0"),
            "model_type": "mock",
            "input_shape": kwargs.get("input_shape", [None]),
            "output_shape": kwargs.get("output_shape", [None]),
            "description": "Mock model for testing",
        }
        self._loaded = True
        logger.info(f"Mock model loaded from {model_path}")

    def predict(self, inputs: Any, **kwargs) -> Any:
        """
        Simulate model inference.

        Args:
            inputs: The input data.
            **kwargs: Override default output.

        Returns:
            The default output or a custom output from kwargs.

        Raises:
            ProviderError: If the model is not loaded.
        """
        if not self._loaded:
            raise ProviderError("Model not loaded")

        if "output" in kwargs:
            return kwargs["output"]
        if isinstance(inputs, dict) and "output" in inputs:
            return inputs["output"]
        return self._default_output

    def metadata(self) -> Dict[str, Any]:
        """Return metadata about the mock model."""
        if not self._loaded:
            raise ProviderError("Model not loaded")
        return self._metadata

    def is_loaded(self) -> bool:
        return self._loaded
