"""
===============================================================================
Module: security.hashing

Password hashing utilities for the CAMEAL Security subsystem.

Responsibilities
----------------
- Secure password hashing
- Password verification
- Salt generation
- Constant-time comparison

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PasswordHash:
    """
    Represents a hashed password.
    """

    algorithm: str

    iterations: int

    salt: str

    digest: str

    def encode(self) -> str:
        """
        Serialize password hash for storage.
        """

        return (
            f"{self.algorithm}$"
            f"{self.iterations}$"
            f"{self.salt}$"
            f"{self.digest}"
        )

    @staticmethod
    def decode(value: str) -> "PasswordHash":
        """
        Deserialize stored password hash.
        """

        algorithm, iterations, salt, digest = value.split("$")

        return PasswordHash(
            algorithm=algorithm,
            iterations=int(iterations),
            salt=salt,
            digest=digest,
        )


class HashingService:
    """
    Password hashing service.
    """

    DEFAULT_ITERATIONS = 600_000

    ALGORITHM = "pbkdf2_sha256"

    @staticmethod
    def hash_password(
        password: str,
    ) -> str:
        """
        Hash a password.
        """

        salt = secrets.token_hex(16)

        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            HashingService.DEFAULT_ITERATIONS,
        ).hex()

        return PasswordHash(
            algorithm=HashingService.ALGORITHM,
            iterations=HashingService.DEFAULT_ITERATIONS,
            salt=salt,
            digest=digest,
        ).encode()

    @staticmethod
    def verify_password(
        password: str,
        stored_hash: str,
    ) -> bool:
        """
        Verify a password.
        """

        stored = PasswordHash.decode(stored_hash)

        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            stored.salt.encode("utf-8"),
            stored.iterations,
        ).hex()

        return hmac.compare_digest(
            digest,
            stored.digest,
        )
