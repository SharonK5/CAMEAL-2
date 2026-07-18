# kernel/lifecycle/transitions.py
from typing import Dict, Set
from .states import LifecycleState


# Core valid state transitions
VALID_TRANSITIONS: Dict[LifecycleState, Set[LifecycleState]] = {
    LifecycleState.CREATED: {LifecycleState.INITIALIZED},
    LifecycleState.INITIALIZED: {LifecycleState.VALIDATED},
    LifecycleState.VALIDATED: {LifecycleState.BOOTED},
    LifecycleState.BOOTED: {LifecycleState.STARTED},
    LifecycleState.STARTED: {LifecycleState.RUNNING},
    LifecycleState.RUNNING: {LifecycleState.STOPPING, LifecycleState.FAILED},
    LifecycleState.STOPPING: {LifecycleState.STOPPED, LifecycleState.FAILED},
    LifecycleState.STOPPED: {LifecycleState.SHUTDOWN},
    LifecycleState.SHUTDOWN: {LifecycleState.DISPOSED},
    LifecycleState.DISPOSED: set(),
    LifecycleState.FAILED: {LifecycleState.DISPOSED},
}

# Pause/resume transitions (only for components implementing Pausable)
PAUSE_TRANSITIONS: Dict[LifecycleState, Set[LifecycleState]] = {
    LifecycleState.RUNNING: {LifecycleState.PAUSED},
    LifecycleState.PAUSED: {LifecycleState.RUNNING, LifecycleState.STOPPING, LifecycleState.FAILED},
}


def is_valid_transition(current: LifecycleState, target: LifecycleState) -> bool:
    """Check if a core state transition is valid."""
    return target in VALID_TRANSITIONS.get(current, set())


def is_valid_pause_transition(current: LifecycleState, target: LifecycleState) -> bool:
    """Check if a pause/resume transition is valid."""
    return target in PAUSE_TRANSITIONS.get(current, set())


def get_allowed_transitions(state: LifecycleState) -> Set[LifecycleState]:
    """Return all allowed next states for a given state."""
    return VALID_TRANSITIONS.get(state, set())


def get_allowed_pause_transitions(state: LifecycleState) -> Set[LifecycleState]:
    """Return allowed pause/resume transitions for a given state."""
    return PAUSE_TRANSITIONS.get(state, set())
