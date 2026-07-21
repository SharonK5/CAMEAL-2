# kernel/providers/embedding/embedding_provider.py
"""
Embedding provider abstraction.
"""

from abc import abstractmethod
from typing import Any, List, Union

from ..base.provider import Provider


class EmbeddingProvider(Provider):
    """
    Base interface for embedding generation providers.

    Embedding providers transform text into dense vector representations
    that can be used for similarity search, clustering, classification,
    and other machine learning tasks.

    Examples of implementations:
        - SentenceTransformers (local models)
        - OpenAI embeddings (API-based)
        - HuggingFace transformers (local models)
        - Cohere embeddings (API-based)
        - Custom embedding models (ONNX, PyTorch)

    All embedding providers must support:
        - Embedding multiple texts in a single batch
        - Query embedding (potentially with different normalization)
        - Reporting the embedding dimension
    """

    @abstractmethod
    def get(self) -> Any:
        """
        Return the underlying embedding client or model.

        Returns:
            The underlying embedding client (e.g., SentenceTransformer, OpenAI client).
        """
        pass

    @abstractmethod
    def embed(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        Generate embeddings for one or more texts.

        Args:
            texts: A single string or a list of strings to embed.

        Returns:
            A list of embedding vectors (each a list of floats).

        Raises:
            ProviderInitializationError: If the provider is not initialized.
        """
        pass

    @abstractmethod
    def embed_query(self, query: str) -> List[float]:
        """
        Generate an embedding for a single query.

        Query embedding may use different normalization or processing
        compared to document embedding (e.g., for asymmetric search).

        Args:
            query: The query string to embed.

        Returns:
            The query embedding vector (list of floats).
        """
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """
        Return the dimension of the embeddings.

        Returns:
            The embedding dimension (e.g., 384 for all-MiniLM-L6-v2).

        Raises:
            ProviderInitializationError: If the provider is not initialized.
        """
        pass

    @abstractmethod
    def batch_size(self) -> int:
        """
        Return the recommended batch size for embedding.

        Returns:
            The recommended batch size (e.g., 32, 64, 128).
        """
        pass
