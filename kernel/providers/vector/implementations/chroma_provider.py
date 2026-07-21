import logging
# kernel/providers/vector/implementations/chroma_provider.py
"""
Chroma vector store provider.

Chroma is an open-source embedding database that provides:
- Simplicity (easy to use)
- Support for metadata filtering
- Optional persistence
- Built-in support for multiple embeddings providers
"""

import os
from typing import Any, List, Dict, Optional

from ..vector_provider import VectorProvider
from kernel.lifecycle import HealthStatus
from ...base.exceptions import ProviderInitializationError, ProviderError

logger = logging.getLogger(__name__)


class ChromaVectorStoreProvider(VectorProvider):
    """
    Vector store using Chroma DB.

    Chroma is a simple, lightweight vector database that works well
    for development and smaller production workloads.

    Usage:
        provider = ChromaVectorStoreProvider(
            collection_name="my_docs",
            persist_directory="./chroma_data"
        )
        provider.start()
        provider.upsert(
            ids=["doc1", "doc2"],
            vectors=[[0.1, ...], [0.2, ...]],
            metadata=[{"title": "Doc 1"}, {"title": "Doc 2"}]
        )
        results = provider.query(query_vector, top_k=5)
        provider.stop()
    """

    def __init__(
        self,
        collection_name: str = "default",
        persist_directory: Optional[str] = "./chroma_data",
        distance_metric: str = "cosine",
    ) -> None:
        """
        Initialize the Chroma vector store.

        Args:
            collection_name: Name of the collection.
            persist_directory: Directory for persistence.
            distance_metric: Distance metric ("cosine", "l2", "ip").
        """
        self._collection_name = collection_name
        self._persist_directory = persist_directory
        self._distance_metric = distance_metric
        self._client = None
        self._collection = None
        self._initialized = False

    def get(self) -> Any:
        """Return the underlying Chroma collection."""
        return self._collection

    def start(self) -> None:
        """
        Initialize the Chroma client and collection.

        Raises:
            ProviderInitializationError: If chromadb is not installed.
        """
        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError as e:
            raise ProviderInitializationError(
                "chromadb not installed. Install with: pip install chromadb"
            ) from e

        try:
            # Create client
            settings = Settings()
            if self._persist_directory:
                settings.persist_directory = self._persist_directory
                settings.is_persistent = True

            self._client = chromadb.Client(settings)

            # Get or create collection
            self._collection = self._client.get_or_create_collection(
                name=self._collection_name,
                metadata={"hnsw:space": self._distance_metric},
            )
            self._initialized = True
            logger.info(f"Chroma collection '{self._collection_name}' initialized")
        except Exception as e:
            raise ProviderInitializationError(f"Failed to initialize Chroma: {e}") from e

    def stop(self) -> None:
        """Clean up the Chroma client."""
        self._collection = None
        self._client = None
        self._initialized = False

    def health(self) -> HealthStatus:
        """Check if the Chroma collection is healthy."""
        if not self._initialized or self._collection is None:
            return HealthStatus.UNHEALTHY
        try:
            self._collection.count()
            return HealthStatus.HEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY

    def upsert(
        self,
        ids: List[str],
        vectors: List[List[float]],
        metadata: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> None:
        """
        Insert or update vectors.

        Args:
            ids: List of vector IDs.
            vectors: List of embedding vectors.
            metadata: Optional list of metadata dicts.

        Raises:
            ProviderError: If the operation fails.
        """
        if not self._initialized or self._collection is None:
            raise ProviderError("Provider not initialized")

        if len(ids) != len(vectors):
            raise ValueError("ids and vectors must have the same length")

        try:
            self._collection.upsert(
                ids=ids,
                embeddings=vectors,
                metadatas=metadata or [{}] * len(ids),
            )
        except Exception as e:
            raise ProviderError(f"Chroma upsert failed: {e}") from e

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
            top_k: Number of neighbors to return.
            filter: Optional metadata filter.

        Returns:
            List of results with id, score, and metadata.
        """
        if not self._initialized or self._collection is None:
            raise ProviderError("Provider not initialized")

        try:
            results = self._collection.query(
                query_embeddings=[vector],
                n_results=top_k,
                where=filter,
            )

            # Format results
            formatted_results = []
            if results["ids"]:
                for i, doc_id in enumerate(results["ids"][0]):
                    formatted_results.append({
                        "id": doc_id,
                        "score": float(results["distances"][0][i]) if results.get("distances") else 0.0,
                        "metadata": results["metadatas"][0][i] if results.get("metadatas") else {},
                    })
            return formatted_results
        except Exception as e:
            raise ProviderError(f"Chroma query failed: {e}") from e

    def delete(self, ids: List[str]) -> None:
        """
        Delete vectors by ID.

        Args:
            ids: List of vector IDs to delete.
        """
        if not self._initialized or self._collection is None:
            raise ProviderError("Provider not initialized")

        try:
            self._collection.delete(ids=ids)
        except Exception as e:
            raise ProviderError(f"Chroma delete failed: {e}") from e

    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a vector by ID.

        Args:
            id: The vector ID.

        Returns:
            Dict with id and metadata, or None if not found.
        """
        if not self._initialized or self._collection is None:
            raise ProviderError("Provider not initialized")

        try:
            results = self._collection.get(ids=[id])
            if results["ids"]:
                return {
                    "id": results["ids"][0],
                    "vector": results["embeddings"][0] if results.get("embeddings") else None,
                    "metadata": results["metadatas"][0] if results.get("metadatas") else {},
                }
            return None
        except Exception as e:
            raise ProviderError(f"Chroma get_by_id failed: {e}") from e

    def count(self) -> int:
        """
        Return the total number of vectors.

        Returns:
            The total count of vectors.
        """
        if not self._initialized or self._collection is None:
            return 0
        return self._collection.count()

    def dimension(self) -> int:
        """
        Return the vector dimension.

        Returns:
            The embedding dimension (must be known from context).
            Chroma doesn't enforce dimension, so we raise an error if not set.
        """
        raise NotImplementedError(
            "Chroma doesn't enforce dimension. Track this externally."
        )

    def clear(self) -> None:
        """
        Remove all vectors from the collection.
        """
        if not self._initialized or self._collection is None:
            raise ProviderError("Provider not initialized")

        try:
            # Get all IDs and delete them
            results = self._collection.get()
            if results["ids"]:
                self._collection.delete(ids=results["ids"])
            logger.info(f"Chroma collection '{self._collection_name}' cleared")
        except Exception as e:
            raise ProviderError(f"Chroma clear failed: {e}") from e
