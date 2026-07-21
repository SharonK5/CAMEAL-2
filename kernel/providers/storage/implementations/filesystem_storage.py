# kernel/providers/storage/implementations/filesystem_storage.py
"""
Filesystem storage provider.
"""

import os
from pathlib import Path
from typing import Any, Optional, List

from ..storage_provider import StorageProvider
from kernel.lifecycle import HealthStatus


class FilesystemStorageProvider(StorageProvider):
    """
    Storage provider using the local filesystem.

    This is a simple implementation useful for development, testing,
    and lightweight production use.

    All data is stored as files in a root directory.
    """

    def __init__(self, root_path: str = "./storage") -> None:
        """
        Initialize the filesystem storage provider.

        Args:
            root_path: Root directory where files will be stored.
        """
        self._root_path = Path(root_path)
        self._initialized = False

    def get(self) -> Path:
        """Return the root path as the underlying 'client'."""
        return self._root_path

    def start(self) -> None:
        """Create the root directory if it doesn't exist."""
        self._root_path.mkdir(parents=True, exist_ok=True)
        self._initialized = True

    def stop(self) -> None:
        """Mark as stopped (files are left intact)."""
        self._initialized = False

    def health(self) -> HealthStatus:
        """Check if the root directory exists and is writable."""
        if not self._initialized:
            return HealthStatus.UNHEALTHY
        if not self._root_path.exists():
            return HealthStatus.UNHEALTHY
        if not os.access(self._root_path, os.W_OK):
            return HealthStatus.UNHEALTHY
        return HealthStatus.HEALTHY

    def put(self, key: str, data: bytes, metadata: Optional[dict] = None) -> str:
        """
        Store data as a file.

        Args:
            key: Relative file path (will be created inside root).
            data: Binary data to write.
            metadata: Ignored for filesystem storage.

        Returns:
            The absolute file path.
        """
        file_path = self._root_path / key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(data)
        return str(file_path)

    def get_data(self, key: str) -> bytes:
        """
        Read data from a file.

        Args:
            key: Relative file path.

        Returns:
            The binary content of the file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        file_path = self._root_path / key
        if not file_path.exists():
            raise FileNotFoundError(f"Key '{key}' not found")
        return file_path.read_bytes()

    def delete(self, key: str) -> None:
        """
        Delete a file.

        Args:
            key: Relative file path.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        file_path = self._root_path / key
        if not file_path.exists():
            raise FileNotFoundError(f"Key '{key}' not found")
        file_path.unlink()

    def exists(self, key: str) -> bool:
        """
        Check if a file exists.

        Args:
            key: Relative file path.

        Returns:
            True if the file exists, False otherwise.
        """
        return (self._root_path / key).exists()

    def list(self, prefix: str = "") -> List[str]:
        """
        List all files under the root path, optionally filtered by prefix.

        Args:
            prefix: Optional prefix (subdirectory path).

        Returns:
            List of relative file paths.
        """
        if prefix:
            base_path = self._root_path / prefix
            if not base_path.exists():
                return []
            return [
                str(p.relative_to(self._root_path))
                for p in base_path.glob("**/*")
                if p.is_file()
            ]
        return [
            str(p.relative_to(self._root_path))
            for p in self._root_path.glob("**/*")
            if p.is_file()
        ]
