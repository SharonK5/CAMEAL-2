# security/trust/trust_provider.py
"""
Public API for trust providers.

This module re‑exports the base TrustProvider interface.
"""

from .provider import TrustProvider

__all__ = ["TrustProvider"]
