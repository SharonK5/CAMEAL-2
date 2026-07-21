# kernel/providers/vector/implementations/faiss_vector_store.py
"""
FAISS vector store provider.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, List, Dict, Optional, Tuple
import numpy as np

from ..vector_provider import VectorProvider
from kernel.lifecycle import HealthStatus
from ...base.exceptions import ProviderInitializationError, ProviderError

logger = logging.getLogger(__name__)


class FAISSVectorStoreProvider(VectorProvider):
    """
    Vector store using FAISS.
    """

    def __init__(
        self,
        dimension: int,
        index_type: str = "Flat",
        metric: str = "cosine",
        persist_path: Optional[str] = None,
        normalize: bool = True,
    ) -> None:
        self._dimension = dimension
        self._index_type = index_type
        self._metric = metric
        self._persist_path = persist_path
        self._normalize = normalize
        self._index = None
        self._metadata = {}
        self._id_to_index = {}
        self._index_to_id = {}
        self._initialized = False
        self._next_id = 0
        self._faiss = None

    def get(self) -> Any:
        return self._index

    def start(self) -> None:
        try:
            import faiss
        except ImportError as e:
            raise ProviderInitializationError(
                "FAISS library not installed. Install with: pip install faiss-cpu"
            ) from e

        self._faiss = faiss

        if self._metric == "cosine":
            index = faiss.IndexFlatIP(self._dimension)
        else:
            index = faiss.IndexFlatL2(self._dimension)

        self._index = faiss.IndexIDMap(index)

        if self._persist_path and os.path.exists(self._persist_path):
            try:
                self._load_from_disk()
                logger.info(f"Loaded FAISS index from {self._persist_path}")
            except Exception as e:
                logger.warning(f"Failed to load index from {self._persist_path}: {e}")

        self._initialized = True
        logger.info(
            f"FAISS index initialized: dimension={self._dimension}, "
            f"type={self._index_type}, metric={self._metric}"
        )

    def stop(self) -> None:
        if self._persist_path and self._initialized:
            try:
                self._save_to_disk()
                logger.info(f"Saved FAISS index to {self._persist_path}")
            except Exception as e:
                logger.error(f"Failed to save index: {e}")

        self._index = None
        self._metadata = {}
        self._id_to_index = {}
        self._index_to_id = {}
        self._initialized = False

    def health(self) -> HealthStatus:
        if not self._initialized or self._index is None:
            return HealthStatus.UNHEALTHY
        return HealthStatus.HEALTHY

    def _on_health(self) -> bool:
        """Lifecycle health check implementation."""
        return self.health() == HealthStatus.HEALTHY

    def upsert(
        self,
        ids: List[str],
        vectors: List[List[float]],
        metadata: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> None:
        if not self._initialized or self._index is None:
            raise ProviderError("Provider not initialized")

        if len(ids) != len(vectors):
            raise ValueError("ids and vectors must have the same length")

        if metadata and len(metadata) != len(ids):
            raise ValueError("metadata and ids must have the same length")

        vectors_np = np.array(vectors).astype(np.float32)

        if self._normalize:
            self._faiss.normalize_L2(vectors_np)

        for i, (vec_id, vec) in enumerate(zip(ids, vectors_np)):
            self._index.add_with_ids(
                vec.reshape(1, -1),
                np.array([self._next_id], dtype=np.int64)
            )
            self._id_to_index[vec_id] = self._next_id
            self._index_to_id[self._next_id] = vec_id

            if metadata and i < len(metadata):
                self._metadata[vec_id] = metadata[i]
            else:
                self._metadata[vec_id] = {}

            self._next_id += 1

    def query(
        self,
        vector: List[float],
        top_k: int = 10,
        filter: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        if not self._initialized or self._index is None:
            raise ProviderError("Provider not initialized")

        if self._index.ntotal == 0:
            return []

        query_vec = np.array(vector).astype(np.float32).reshape(1, -1)

        if self._normalize:
            self._faiss.normalize_L2(query_vec)

        k = min(top_k, self._index.ntotal)
        scores, indices = self._index.search(query_vec, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            vec_id = self._index_to_id.get(int(idx))
            if vec_id:
                results.append({
                    "id": vec_id,
                    "score": float(score),
                    "metadata": self._metadata.get(vec_id, {}),
                })
        return results

    def delete(self, ids: List[str]) -> None:
        if not self._initialized:
            raise ProviderError("Provider not initialized")

        for vec_id in ids:
            if vec_id in self._id_to_index:
                idx = self._id_to_index[vec_id]
                del self._id_to_index[vec_id]
                del self._index_to_id[idx]
                if vec_id in self._metadata:
                    del self._metadata[vec_id]

        logger.warning(
            "FAISS doesn't support direct deletion. "
            "Vectors removed from metadata but remain in the index."
        )

    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        if not self._initialized or self._index is None:
            raise ProviderError("Provider not initialized")

        if id not in self._id_to_index:
            return None

        return {
            "id": id,
            "vector": None,
            "metadata": self._metadata.get(id, {}),
        }

    def count(self) -> int:
        if not self._initialized or self._index is None:
            return 0
        return self._index.ntotal

    def dimension(self) -> int:
        return self._dimension

    def clear(self) -> None:
        if not self._initialized or self._index is None:
            raise ProviderError("Provider not initialized")

        self._index.reset()
        self._metadata = {}
        self._id_to_index = {}
        self._index_to_id = {}
        self._next_id = 0
        logger.info("FAISS index cleared")

    def _save_to_disk(self) -> None:
        if self._index is None or self._persist_path is None:
            return

        os.makedirs(os.path.dirname(self._persist_path), exist_ok=True)
        self._faiss.write_index(self._index, self._persist_path)

        metadata_path = f"{self._persist_path}.meta"
        with open(metadata_path, "w") as f:
            json.dump({
                "metadata": self._metadata,
                "id_to_index": self._id_to_index,
                "index_to_id": self._index_to_id,
                "next_id": self._next_id,
            }, f)

    def _load_from_disk(self) -> None:
        if self._persist_path is None or not os.path.exists(self._persist_path):
            return

        self._index = self._faiss.read_index(self._persist_path)

        metadata_path = f"{self._persist_path}.meta"
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                data = json.load(f)
                self._metadata = data.get("metadata", {})
                self._id_to_index = data.get("id_to_index", {})
                self._index_to_id = data.get("index_to_id", {})
                self._next_id = data.get("next_id", 0)
