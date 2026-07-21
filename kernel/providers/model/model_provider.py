# kernel/providers/model/model_provider.py
"""
Model provider abstraction.

Provides interfaces for local ML model inference.
"""

from abc import abstractmethod
from typing import Any, Dict, Optional, Union

from ..base.provider import Provider


class ModelProvider(Provider):
    """
    Base interface for model providers.

    Model providers abstract access to local machine learning models:
        - ONNX models
        - PyTorch models
        - TensorFlow models
        - Scikit-learn models
        - Custom model formats

    All model providers must support:
        - Loading a model from a path
        - Running inference (predict)
        - Model metadata (input/output shapes)

    Examples of implementations:
        - ONNX Runtime provider
        - PyTorch provider
        - Scikit-learn provider
        - TensorFlow Lite provider
    """

    @abstractmethod
    def get(self) -> Any:
        """Return the underlying model instance."""
        pass

    @abstractmethod
    def load(self, model_path: str, **kwargs) -> None:
        """
        Load a model from a file path.

        Args:
            model_path: Path to the model file.
            **kwargs: Implementation-specific loading options.

        Raises:
            ProviderInitializationError: If loading fails.
        """
        pass

    @abstractmethod
    def predict(self, inputs: Any, **kwargs) -> Any:
        """
        Run inference on the model.

        Args:
            inputs: Input data for the model (format depends on model type).
            **kwargs: Implementation-specific inference options.

        Returns:
            The model's output.

        Raises:
            ProviderError: If inference fails.
        """
        pass

    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        """
        Return metadata about the model.

        Returns:
            Dict containing:
                - name (optional)
                - version (optional)
                - input_shape (optional)
                - output_shape (optional)
                - model_type (e.g., "onnx", "pytorch")
                - description (optional)

        Raises:
            ProviderError: If metadata cannot be retrieved.
        """
        pass

    @abstractmethod
    def is_loaded(self) -> bool:
        """Return True if a model is currently loaded."""
        pass
