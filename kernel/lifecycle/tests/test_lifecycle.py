# kernel/lifecycle/tests/test_lifecycle.py
import pytest
from ..lifecycle import Lifecycle
from ..states import LifecycleState
from ..health import HealthStatus
from ..exceptions import LifecycleError
from .conftest import DummyComponent, PausableDummyComponent


class TestLifecycle:
    # ... (other tests unchanged)

    def test_invalid_transition(self, dummy_component):
        with pytest.raises(LifecycleError, match="Invalid transition from created to started"):
            dummy_component.start()

    # ... rest of the tests unchanged
