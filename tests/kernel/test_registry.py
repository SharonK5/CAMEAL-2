import pytest

from kernel.registry import registry


class Dummy:
    pass


def test_register_component():
    component = Dummy()
    registry.register("dummy", component)
    assert registry.resolve("dummy") is component


def test_unregister():
    registry.unregister("dummy")
    with pytest.raises(KeyError):
        registry.resolve("dummy")
