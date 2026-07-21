# kernel/plugins/exceptions.py
"""
Plugin-related exceptions.
"""


class PluginError(Exception):
    """Base exception for all plugin errors."""
    pass


class PluginLoadError(PluginError):
    """Raised when a plugin fails to load."""
    pass


class PluginDiscoveryError(PluginError):
    """Raised when plugin discovery fails."""
    pass


class PluginRegistrationError(PluginError):
    """Raised when a plugin fails to register its components."""
    pass


class PluginManifestError(PluginError):
    """Raised when a plugin manifest is invalid or malformed."""
    pass


class PluginNotFoundError(PluginError):
    """Raised when a plugin is not found."""
    pass
