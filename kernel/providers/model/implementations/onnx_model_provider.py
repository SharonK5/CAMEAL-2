import logging
# kernel/providers/model/implementations/onnx_model_provider.py
"""
ONNX Runtime model provider.

Provides inference using ONNX Runtime.
"""

import os
import numpy as np
from typing import Any, Dict, Optional, Union

from ..model_provider import ModelProvider
from kernel.lifecycle import HealthStatus
from ...base.exceptions import ProviderInitializationError, ProviderError

logger = logging.getLogger(__name__)


class ONNXModelProvider(ModelProvider):
    """
    ONNX Runtime model provider.

    Uses ONNX Runtime for fast inference on ONNX models.

    Requirements:
        - onnxruntime package installed

    Usage:
        provider = ONNXModelProvider()
        provider.load("model.onnx", providers=["CPUExecutionProvider"])
        result = provider.predict(input_data)
        provider.stop()
    """

    def __init__(self) -> None:
        self._session = None
        self._loaded = False
        self._input_names = []
        self._output_names = []
        self._metadata = {}

    def get(self) -> Any:
        """Return the ONNX Runtime session."""
        return self._session

    def start(self) -> None:
        """Initialize the ONNX provider."""
        self._loaded = False

    def stop(self) -> None:
        """Clean up the ONNX session."""
        self._session = None
        self._loaded = False

    def health(self) -> HealthStatus:
        """Check if the provider is healthy."""
        if not self._loaded or self._session is None:
            return HealthStatus.UNHEALTHY
        try:
            # Try a dummy run to verify the session is functional
            # But we may not have input data; we'll just check session exists
            return HealthStatus.HEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY

    def load(self, model_path: str, **kwargs) -> None:
        """
        Load an ONNX model.

        Args:
            model_path: Path to the ONNX model file.
            **kwargs: Additional options for ONNX Runtime.

        Raises:
            ProviderInitializationError: If ONNX Runtime is not installed or model load fails.
        """
        try:
            import onnxruntime as ort
        except ImportError as e:
            raise ProviderInitializationError(
                "onnxruntime not installed. Install with: pip install onnxruntime"
            ) from e

        if not os.path.exists(model_path):
            raise ProviderInitializationError(f"Model file not found: {model_path}")

        try:
            providers = kwargs.get("providers", ["CPUExecutionProvider"])
            self._session = ort.InferenceSession(
                model_path,
                providers=providers,
                **{k: v for k, v in kwargs.items() if k != "providers"}
            )

            # Extract input/output info
            self._input_names = [inp.name for inp in self._session.get_inputs()]
            self._output_names = [out.name for out in self._session.get_outputs()]

            # Build metadata
            self._metadata = {
                "name": os.path.basename(model_path),
                "version": "1.0.0",
                "model_type": "onnx",
                "input_names": self._input_names,
                "output_names": self._output_names,
                "input_shapes": [inp.shape for inp in self._session.get_inputs()],
                "output_shapes": [out.shape for out in self._session.get_outputs()],
            }

            self._loaded = True
            logger.info(f"ONNX model loaded from {model_path}")
        except Exception as e:
            raise ProviderInitializationError(f"Failed to load ONNX model: {e}") from e

    def predict(self, inputs: Any, **kwargs) -> Any:
        """
        Run inference on the ONNX model.

        Args:
            inputs: Input data. Can be a dict mapping input names to numpy arrays,
                    or a single numpy array (if single input).
            **kwargs: Additional inference options.

        Returns:
            The model output(s).

        Raises:
            ProviderError: If inference fails.
        """
        if not self._loaded or self._session is None:
            raise ProviderError("Model not loaded")

        try:
            # Convert inputs to dict if needed
            if isinstance(inputs, dict):
                feed = inputs
            elif len(self._input_names) == 1:
                feed = {self._input_names[0]: inputs}
            else:
                # If multiple inputs and provided as list/tuple
                if isinstance(inputs, (list, tuple)) and len(inputs) == len(self._input_names):
                    feed = {name: val for name, val in zip(self._input_names, inputs)}
                else:
                    raise ProviderError(
                        f"Expected {len(self._input_names)} inputs, got {type(inputs)}"
                    )

            # Run inference
            outputs = self._session.run(self._output_names, feed, **kwargs)

            # Return single output if only one output
            if len(outputs) == 1:
                return outputs[0]
            return dict(zip(self._output_names, outputs))

        except Exception as e:
            raise ProviderError(f"ONNX inference failed: {e}") from e

    def metadata(self) -> Dict[str, Any]:
        """Return metadata about the loaded model."""
        if not self._loaded:
            raise ProviderError("Model not loaded")
        return self._metadata

    def is_loaded(self) -> bool:
        return self._loaded
