"""
System permissions.
"""

from enum import Enum


class Permission(str, Enum):

    READ = "read"

    WRITE = "write"

    DELETE = "delete"

    QUERY = "query"

    ANALYZE = "analyze"

    INGEST = "ingest"

    EXPORT = "export"

    CONFIGURE = "configure"

    ADMIN = "admin"

    GOVERN = "govern"

    REVIEW = "review"
