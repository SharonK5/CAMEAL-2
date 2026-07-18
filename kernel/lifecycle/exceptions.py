# kernel/lifecycle/exceptions.py
"""
Lifecycle-specific exceptions.
"""


class LifecycleError(Exception):
    """
    Raised when an invalid lifecycle transition is attempted.

    Examples:
        - Starting a component that has not been initialized.
        - Pausing a component that is not running.
        - Disposing a component that has not been stopped.
    """

    def __init__(self, message: str, current_state: str = None, target_state: str = None) -> None:
        self.current_state = current_state
        self.target_state = target_state
        if current_state and target_state:
            full_message = f"Invalid transition from {current_state} to {target_state}: {message}"
        else:
            full_message = message
        super().__init__(full_message)
