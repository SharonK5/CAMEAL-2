# kernel/providers/embedding/implementations/sentence_transformer.py
"""
SentenceTransformer embedding provider.

This provider uses the SentenceTransformers library to generate
high-quality embeddings from a variety of pre-trained models.
"""

from typing import Any, List, Union
import numpy as np

from ..embedding_provider import EmbeddingProvider
from kernel.lifecycle import HealthStatus
from ...base.exceptions import ProviderInitializationError


class SentenceTransformerProvider(EmbeddingProvider):
    """
    Embedding provider using SentenceTransformers.

    SentenceTransformers provides state-of-the-art embedding models
    that can run locally without API calls.

    Default model: all-MiniLM-L6-v2 (384 dimensions)
    - Fast, lightweight, and effective for many tasks.

    Alternative models:
        - all-mpnet-base-v2 (768 dimensions) - higher quality, slower
        - multi-qa-MiniLM-L6-cos-v1 (384 dimensions) - optimized for search
        - intfloat/e5-base-v2 (768 dimensions) - advanced retrieval

    Usage:
        provider = SentenceTransformerProvider()
        provider.start()
        embeddings = provider.embed(["Hello world", "Goodbye"])
        query_embedding = provider.embed_query("Search query")
        print(provider.dimension)  # 384
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        device: str = "cpu",
        normalize: bool = True,
    ) -> None:
        """
        Initialize the SentenceTransformer provider.

        Args:
            model_name: Name of the SentenceTransformer model.
            device: Device to use ("cpu" or "cuda").
            normalize: Whether to normalize embeddings (recommended for similarity search).
        """
        self._model_name = model_name
        self._device = device
        self._normalize = normalize
        self._model = None
        self._dimension = None
        self._batch_size = 32
        self._initialized = False

    def get(self) -> Any:
        """
        Return the underlying SentenceTransformer model.

        Returns:
            The SentenceTransformer model instance.
        """
        return self._model

    def start(self) -> None:
        """
        Load the SentenceTransformer model.

        Raises:
            ProviderInitializationError: If sentence-transformers is not installed
                or if the model cannot be loaded.
        """
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            raise ProviderInitializationError(
                "sentence-transformers library not installed. "
                "Install it with: pip install sentence-transformers"
            ) from e

        try:
            self._model = SentenceTransformer(
                self._model_name,
                device=self._device,
            )
            # Use new method name, fallback to old for compatibility
            try:
                self._dimension = self._model.get_embedding_dimension()
            except AttributeError:
                self._dimension = self._model.get_sentence_embedding_dimension()
            self._initialized = True
        except Exception as e:
            raise ProviderInitializationError(
                f"Failed to load SentenceTransformer model '{self._model_name}': {e}"
            ) from e

    def stop(self) -> None:
        """Release the model and clean up resources."""
        self._model = None
        self._dimension = None
        self._initialized = False

    def health(self) -> HealthStatus:
        """
        Check if the provider is healthy.

        Returns:
            HealthStatus.HEALTHY if the model is loaded and ready.
            HealthStatus.UNHEALTHY otherwise.
        """
        if not self._initialized:
            return HealthStatus.UNHEALTHY
        if self._model is None:
            return HealthStatus.UNHEALTHY
        return HealthStatus.HEALTHY

    def embed(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        Generate embeddings for one or more texts.

        Args:
            texts: A single string or list of strings.

        Returns:
            List of embedding vectors (list of floats each).

        Raises:
            ProviderInitializationError: If the provider is not initialized.
        """
        if not self._initialized or self._model is None:
            raise ProviderInitializationError(
                "Embedding provider not initialized. Call start() first."
            )

        if isinstance(texts, str):
            texts = [texts]

        embeddings = self._model.encode(
            texts,
            normalize_embeddings=self._normalize,
            batch_size=self._batch_size,
            device=self._device,
        )
        return embeddings.tolist()

    def embed_query(self, query: str) -> List[float]:
        """
        Generate an embedding for a single query.

        For symmetric models (e.g., all-MiniLM-L6-v2), this is the same as embed().
        For asymmetric models (e.g., multi-qa-MiniLM-L6-cos-v1), this may use
        different processing.

        Args:
            query: The query string to embed.

        Returns:
            The query embedding vector (list of floats).

        Raises:
            ProviderInitializationError: If the provider is not initialized.
        """
        if not self._initialized or self._model is None:
            raise ProviderInitializationError(
                "Embedding provider not initialized. Call start() first."
            )

        embedding = self._model.encode(
            query,
            normalize_embeddings=self._normalize,
            device=self._device,
        )
        return embedding.tolist()

    @property
    def dimension(self) -> int:
        """
        Return the embedding dimension.

        Returns:
            The dimension of the embedding vectors.

        Raises:
            ProviderInitializationError: If the provider is not initialized.
        """
        if not self._initialized:
            raise ProviderInitializationError(
                "Embedding provider not initialized. Call start() first."
            )
        return self._dimension

    def batch_size(self) -> int:
        """
        Return the recommended batch size for embedding.

        Returns:
            The recommended batch size.
        """
        return self._batch_size

    def set_batch_size(self, batch_size: int) -> None:
        """
        Set the batch size for embedding.

        Args:
            batch_size: New batch size (must be > 0).
        """
        if batch_size <= 0:
            raise ValueError("Batch size must be > 0")
        self._batch_size = batch_size
