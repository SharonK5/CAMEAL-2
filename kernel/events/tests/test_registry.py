# kernel/events/tests/test_registry.py
import pytest

from kernel.events.registry import Registry
from kernel.events.exceptions import EventSubscriptionError


class TestRegistry:
    def test_subscribe(self):
        registry = Registry()
        registry.subscribe("test", lambda: None)
        subs = registry.get_subscriptions("test")
        assert len(subs) == 1

    def test_unsubscribe(self):
        registry = Registry()
        registry.subscribe("test", lambda: None, name="test_sub")
        sub_id = registry.get_subscriptions("test")[0].subscription_id
        assert registry.unsubscribe(str(sub_id)) is True
        assert len(registry.get_subscriptions("test")) == 0

    def test_clear(self):
        registry = Registry()
        registry.subscribe("test", lambda: None)
        registry.clear()
        assert len(registry.get_subscriptions("test")) == 0
