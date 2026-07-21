# kernel/bootstrap/tests/test_dependency_graph.py
import pytest

from kernel.bootstrap.dependency_graph import DependencyGraph
from kernel.bootstrap.exceptions import DependencyError


class TestDependencyGraph:
    def test_order(self):
        graph = DependencyGraph()
        graph.add_node("a", ["b"])
        graph.add_node("b", ["c"])
        graph.add_node("c", [])
        order = graph.get_order()
        # c should come before b before a
        assert order.index("c") < order.index("b")
        assert order.index("b") < order.index("a")

    def test_circular_dependency(self):
        graph = DependencyGraph()
        graph.add_node("a", ["b"])
        graph.add_node("b", ["a"])
        with pytest.raises(DependencyError, match="Circular"):
            graph.get_order()

    def test_missing_dependency(self):
        graph = DependencyGraph()
        graph.add_node("a", ["missing"])
        # Should not raise, but the missing dependency will be skipped
        order = graph.get_order()
        assert "a" in order
