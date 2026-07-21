# kernel/providers/lifecycle/__init__.py
"""
Provider lifecycle management.

This package provides lifecycle coordination for all providers,
ensuring consistent start/stop/health management across the
entire provider layer.
"""

from .provider_lifecycle import ProviderLifecycle

__all__ = ["ProviderLifecycle"]
