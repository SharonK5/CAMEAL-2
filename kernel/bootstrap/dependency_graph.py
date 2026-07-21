# kernel/bootstrap/dependency_graph.py
"""
Dependency graph for component ordering.
"""

from typing import Dict, List, Set, Type, Any

from .exceptions import DependencyError


class DependencyGraph:
    """
    Computes dependency ordering for components.
    """

    def __init__(self) -> None:
        self._nodes: Dict[str, Set[str]] = {}

    def add_node(self, name: str, dependencies: List[str]) -> None:
        """Add a node with its dependencies."""
        self._nodes[name] = set(dependencies)

    def get_order(self) -> List[str]:
        """
        Get a topological ordering of nodes.

        Returns nodes in order where dependencies appear before dependents.
        """
        visited: Set[str] = set()
        visiting: Set[str] = set()
        result: List[str] = []

        def dfs(name: str) -> None:
            if name in visiting:
                raise DependencyError(f"Circular dependency detected: {name}")
            if name in visited:
                return

            visiting.add(name)
            for dep in self._nodes.get(name, []):
                if dep not in visited:
                    dfs(dep)
            visiting.remove(name)
            visited.add(name)
            result.append(name)

        for name in self._nodes:
            if name not in visited:
                dfs(name)

        return result

    def has_node(self, name: str) -> bool:
        return name in self._nodes
