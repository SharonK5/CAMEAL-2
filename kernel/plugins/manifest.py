# kernel/plugins/manifest.py
"""
Plugin manifest data model.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class PluginManifest:
    """
    Describes a plugin's metadata and extension points.
    """

    name: str
    version: str
    module: str   # ✅ required: Python module containing the plugin class
    kernel_compatibility: str = ">=1.0.0"
    description: Optional[str] = None
    author: Optional[str] = None
    providers: List[Dict[str, Any]] = field(default_factory=list)
    engines: List[Dict[str, Any]] = field(default_factory=list)
    workflows: List[Dict[str, Any]] = field(default_factory=list)
    schedulers: List[Dict[str, Any]] = field(default_factory=list)
    event_handlers: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PluginManifest":
        """Create a PluginManifest from a dictionary (YAML)."""
        return cls(
            name=data.get("name"),
            version=data.get("version"),
            module=data.get("module"),   # ✅ added
            kernel_compatibility=data.get("kernel_compatibility", ">=1.0.0"),
            description=data.get("description"),
            author=data.get("author"),
            providers=data.get("providers", []),
            engines=data.get("engines", []),
            workflows=data.get("workflows", []),
            schedulers=data.get("schedulers", []),
            event_handlers=data.get("event_handlers", []),
            dependencies=data.get("dependencies", []),
        )
