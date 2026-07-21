# kernel/providers/storage/storage_provider.py
"""
Storage provider abstraction.
"""

from abc import abstractmethod
from typing import Any, Optional, List

from ..base.provider import Provider


class StorageProvider(Provider):
    """
    Base interface for storage providers.

    Storage providers handle object/file storage operations:
        - put: store data
        - get_data: retrieve data
        - delete: remove data
        - exists: check existence
        - list: enumerate keys

    Examples of implementations:
        - Local filesystem
        - S3-compatible object storage
        - Database blob storage
        - Cloud storage (AWS S3, GCS, Azure Blob)
    """

    @abstractmethod
    def get(self) -> Any:
        """Return the underlying storage client (e.g., boto3 client, filesystem path)."""
        pass

    @abstractmethod
    def put(self, key: str, data: bytes, metadata: Optional[dict] = None) -> str:
        """
        Store data and return the key/URI.

        Args:
            key: The storage key (path).
            data: The binary data to store.
            metadata: Optional metadata (implementation-specific).

        Returns:
            The full URI or path of the stored object.
        """
        pass

    @abstractmethod
    def get_data(self, key: str) -> bytes:
        """
        Retrieve data by key.

        Args:
            key: The storage key.

        Returns:
            The binary data.

        Raises:
            FileNotFoundError: If the key does not exist.
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Delete data by key.

        Args:
            key: The storage key.

        Raises:
            FileNotFoundError: If the key does not exist.
        """
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """
        Check if data exists for the given key.

        Args:
            key: The storage key.

        Returns:
            True if the key exists, False otherwise.
        """
        pass

    @abstractmethod
    def list(self, prefix: str = "") -> List[str]:
        """
        List all keys with the given prefix.

        Args:
            prefix: Optional prefix to filter keys.

        Returns:
            A list of keys (full paths).
        """
        pass
