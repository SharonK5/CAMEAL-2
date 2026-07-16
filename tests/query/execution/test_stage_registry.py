import pytest
from unittest.mock import Mock

from query.execution import StageRegistry


def test_register_and_get():
    registry = StageRegistry()
    stage = Mock(name="test")
    stage.name = "test"
    registry.register(stage)  # uses stage.name as key
    assert registry.get("test") is stage


def test_register_duplicate_raises():
    registry = StageRegistry()
    stage1 = Mock(name="test")
    stage1.name = "test"
    stage2 = Mock(name="test")
    stage2.name = "test"
    registry.register(stage1)
    with pytest.raises(ValueError, match="already registered"):
        registry.register(stage2)


def test_unregister():
    registry = StageRegistry()
    stage = Mock(name="test")
    stage.name = "test"
    registry.register(stage)
    registry.unregister("test")
    assert registry.get("test") is None


def test_list_names():
    registry = StageRegistry()
    s1 = Mock(name="a"); s1.name = "a"
    s2 = Mock(name="b"); s2.name = "b"
    registry.register(s1)
    registry.register(s2)
    assert set(registry.identifiers()) == {"a", "b"}


def test_list_stages():
    registry = StageRegistry()
    s1 = Mock(name="a"); s1.name = "a"
    s2 = Mock(name="b"); s2.name = "b"
    registry.register(s1)
    registry.register(s2)
    assert tuple(registry.stages()) == (s1, s2)
