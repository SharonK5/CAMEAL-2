# kernel/providers/vector/vector_provider.py
"""
Vector store provider abstraction.
"""

from abc import abstractmethod
from typing import Any, List, Dict, Optional, Tuple

from ..base.provider import Provider


class VectorProvider(Provider):
    """
    Base interface for vector store providers.

    Vector stores are specialized databases that store high-dimensional
    vectors and enable efficient similarity search.

    Examples of implementations:
        - FAISS (local, in-memory)
        - Pinecone (cloud)
        - Qdrant (local or cloud)
        - Milvus (distributed)
        - Chroma (local)
        - LanceDB (embedded)

    All vector providers must support:
        - Upserting vectors with metadata
        - Nearest neighbor search (query)
        - Deleting vectors by ID
        - Getting vectors by ID
    """

    @abstractmethod
    def get(self) -> Any:
        """
        Return the underlying vector store client.

        Returns:
            The vector store client (implementation-specific).
        """
        pass

    @abstractmethod
    def upsert(
        self,
        ids: List[str],
        vectors: List[List[float]],
        metadata: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> None:
        """
        Insert or update vectors in the store.

        Args:
            ids: List of unique vector IDs.
            vectors: List of embedding vectors (each a list of floats).
            metadata: Optional list of metadata dicts (same order as ids).
            **kwargs: Implementation-specific parameters.

        Raises:
            ProviderError: If the operation fails.
        """
        pass

    @abstractmethod
    def query(
        self,
        vector: List[float],
        top_k: int = 10,
        filter: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Query the nearest neighbors.

        Args:
            vector: The query vector.
            top_k: Number of nearest neighbors to return.
            filter: Optional metadata filter.
            **kwargs: Implementation-specific parameters.

        Returns:
            A list of results, each containing:
                - id: The vector ID
                - score: Similarity score (higher is better)
                - metadata: Associated metadata (if any)

        Raises:
            ProviderError: If the query fails.
        """
        pass

    @abstractmethod
    def delete(self, ids: List[str]) -> None:
        """
        Delete vectors by ID.

        Args:
            ids: List of vector IDs to delete.

        Raises:
            ProviderError: If the deletion fails.
        """
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single vector by ID.

        Args:
            id: The vector ID.

        Returns:
            A dict containing:
                - id: The vector ID
                - vector: The embedding vector
                - metadata: Associated metadata
            Returns None if the vector is not found.

        Raises:
            ProviderError: If the operation fails.
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """
        Return the total number of vectors in the store.

        Returns:
            The total count of vectors.

        Raises:
            ProviderError: If the operation fails.
        """
        pass

    @abstractmethod
    def dimension(self) -> int:
        """
        Return the dimension of vectors stored in this index.

        Returns:
            The vector dimension.

        Raises:
            ProviderError: If the provider is not initialized.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Remove all vectors from the store (use with caution).

        Raises:
            ProviderError: If the operation fails.
        """
        pass
