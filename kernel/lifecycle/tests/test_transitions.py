# kernel/lifecycle/tests/test_transitions.py
from ..transitions import (
    is_valid_transition,
    is_valid_pause_transition,
    get_allowed_transitions,
    get_allowed_pause_transitions,
)
from ..states import LifecycleState


class TestTransitions:
    def test_valid_transitions(self):
        assert is_valid_transition(LifecycleState.CREATED, LifecycleState.INITIALIZED) is True
        assert is_valid_transition(LifecycleState.INITIALIZED, LifecycleState.VALIDATED) is True
        assert is_valid_transition(LifecycleState.VALIDATED, LifecycleState.BOOTED) is True
        assert is_valid_transition(LifecycleState.BOOTED, LifecycleState.STARTED) is True
        assert is_valid_transition(LifecycleState.STARTED, LifecycleState.RUNNING) is True
        assert is_valid_transition(LifecycleState.RUNNING, LifecycleState.STOPPING) is True
        assert is_valid_transition(LifecycleState.STOPPING, LifecycleState.STOPPED) is True
        assert is_valid_transition(LifecycleState.STOPPED, LifecycleState.SHUTDOWN) is True
        assert is_valid_transition(LifecycleState.SHUTDOWN, LifecycleState.DISPOSED) is True
        assert is_valid_transition(LifecycleState.FAILED, LifecycleState.DISPOSED) is True

    def test_invalid_transitions(self):
        assert is_valid_transition(LifecycleState.CREATED, LifecycleState.RUNNING) is False
        assert is_valid_transition(LifecycleState.RUNNING, LifecycleState.DISPOSED) is False
        assert is_valid_transition(LifecycleState.DISPOSED, LifecycleState.RUNNING) is False
        assert is_valid_transition(LifecycleState.FAILED, LifecycleState.RUNNING) is False

    def test_pause_transitions(self):
        assert is_valid_pause_transition(LifecycleState.RUNNING, LifecycleState.PAUSED) is True
        assert is_valid_pause_transition(LifecycleState.PAUSED, LifecycleState.RUNNING) is True
        assert is_valid_pause_transition(LifecycleState.CREATED, LifecycleState.PAUSED) is False

    def test_get_allowed_transitions(self):
        allowed = get_allowed_transitions(LifecycleState.RUNNING)
        assert LifecycleState.STOPPING in allowed
        assert LifecycleState.FAILED in allowed
        assert LifecycleState.DISPOSED not in allowed

    def test_get_allowed_pause_transitions(self):
        allowed = get_allowed_pause_transitions(LifecycleState.RUNNING)
        assert LifecycleState.PAUSED in allowed
        allowed = get_allowed_pause_transitions(LifecycleState.PAUSED)
        assert LifecycleState.RUNNING in allowed
        assert LifecycleState.STOPPING in allowed
        assert LifecycleState.FAILED in allowed
