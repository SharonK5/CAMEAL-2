# kernel/providers/storage/implementations/database_storage.py
"""
SQLite-backed storage provider.
"""

import json
import sqlite3
from typing import Any, Optional, List
from pathlib import Path

from ..storage_provider import StorageProvider
from kernel.lifecycle import HealthStatus


class DatabaseStorageProvider(StorageProvider):
    """
    Storage provider using SQLite database.

    Stores binary data and optional metadata in a table.
    Ideal for small to medium datasets and testing.

    Table schema:
        CREATE TABLE IF NOT EXISTS storage (
            key TEXT PRIMARY KEY,
            data BLOB NOT NULL,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """

    def __init__(self, db_path: str = "./storage.db") -> None:
        """
        Initialize the SQLite storage provider.

        Args:
            db_path: Path to the SQLite database file.
        """
        self._db_path = Path(db_path)
        self._connection: Optional[sqlite3.Connection] = None
        self._initialized = False

    def get(self) -> sqlite3.Connection:
        """Return the underlying database connection."""
        return self._connection

    def start(self) -> None:
        """Open the database connection and create the table if it doesn't exist."""
        # Ensure the directory exists
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        self._connection = sqlite3.connect(str(self._db_path))
        self._connection.row_factory = sqlite3.Row

        # Create table
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS storage (
                key TEXT PRIMARY KEY,
                data BLOB NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self._connection.commit()
        self._initialized = True

    def stop(self) -> None:
        """Close the database connection."""
        if self._connection:
            self._connection.close()
        self._connection = None
        self._initialized = False

    def health(self) -> HealthStatus:
        """Check if the database is accessible and healthy."""
        if not self._initialized or self._connection is None:
            return HealthStatus.UNHEALTHY
        try:
            # Simple check: execute a dummy query
            self._connection.execute("SELECT 1").fetchone()
            return HealthStatus.HEALTHY
        except sqlite3.Error:
            return HealthStatus.UNHEALTHY

    def put(self, key: str, data: bytes, metadata: Optional[dict] = None) -> str:
        """
        Store data in the database.

        Args:
            key: Unique identifier.
            data: Binary data to store.
            metadata: Optional dictionary (stored as JSON).

        Returns:
            The key (unchanged).

        Raises:
            sqlite3.Error: On database errors.
        """
        if self._connection is None:
            raise RuntimeError("Provider not started")

        metadata_json = json.dumps(metadata) if metadata else None
        self._connection.execute(
            """
            INSERT OR REPLACE INTO storage (key, data, metadata, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (key, data, metadata_json)
        )
        self._connection.commit()
        return key

    def get_data(self, key: str) -> bytes:
        """
        Retrieve data by key.

        Args:
            key: The storage key.

        Returns:
            The binary data.

        Raises:
            FileNotFoundError: If the key does not exist.
            sqlite3.Error: On database errors.
        """
        if self._connection is None:
            raise RuntimeError("Provider not started")

        row = self._connection.execute(
            "SELECT data FROM storage WHERE key = ?",
            (key,)
        ).fetchone()

        if row is None:
            raise FileNotFoundError(f"Key '{key}' not found")
        return row[0]

    def delete(self, key: str) -> None:
        """
        Delete data by key.

        Args:
            key: The storage key.

        Raises:
            FileNotFoundError: If the key does not exist.
            sqlite3.Error: On database errors.
        """
        if self._connection is None:
            raise RuntimeError("Provider not started")

        cursor = self._connection.execute(
            "DELETE FROM storage WHERE key = ?",
            (key,)
        )
        self._connection.commit()
        if cursor.rowcount == 0:
            raise FileNotFoundError(f"Key '{key}' not found")

    def exists(self, key: str) -> bool:
        """
        Check if data exists for the given key.

        Args:
            key: The storage key.

        Returns:
            True if the key exists, False otherwise.
        """
        if self._connection is None:
            return False

        row = self._connection.execute(
            "SELECT 1 FROM storage WHERE key = ?",
            (key,)
        ).fetchone()
        return row is not None

    def list(self, prefix: str = "") -> List[str]:
        """
        List all keys with the given prefix.

        Args:
            prefix: Optional prefix to filter keys.

        Returns:
            A list of keys.
        """
        if self._connection is None:
            return []

        if prefix:
            rows = self._connection.execute(
                "SELECT key FROM storage WHERE key LIKE ?",
                (f"{prefix}%",)
            ).fetchall()
        else:
            rows = self._connection.execute(
                "SELECT key FROM storage ORDER BY key"
            ).fetchall()
        return [row[0] for row in rows]
