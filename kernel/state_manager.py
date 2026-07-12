"""
kernel.state_manager
====================

Runtime state management for the CAMEAL Kernel.

The State Manager maintains transient system state during execution.
Persistent information belongs in the Repository or Storage modules.

Responsibilities
----------------
- Session state
- Workflow state
- Context state
- Runtime resources
- Event history
- Temporary execution data

The state manager is intentionally lightweight and thread-safe.
"""

from __future__ import annotations

import logging
from copy import deepcopy
from threading import RLock
from typing import Any

logger = logging.getLogger(__name__)


class StateManager:
    """
    Central runtime state manager.
    """

    def __init__(self) -> None:

        self._lock = RLock()

        self._state: dict[str, Any] = {
            "session": {},
            "workflow": {},
            "context": {},
            "runtime": {},
            "resources": {},
            "events": [],
            "temporary": {}
        }

    def get(self, section: str) -> Any:
        """
        Return an entire state section.
        """

        with self._lock:

            return deepcopy(self._state.get(section))

    def set(self, section: str, value: Any) -> None:
        """
        Replace an entire state section.
        """

        with self._lock:

            self._state[section] = deepcopy(value)

            logger.debug("Updated state section '%s'", section)

    def update(self, section: str, key: str, value: Any) -> None:
        """
        Update one value within a section.
        """

        with self._lock:

            if section not in self._state:
                self._state[section] = {}

            if not isinstance(self._state[section], dict):
                raise TypeError(
                    f"State section '{section}' is not a dictionary."
                )

            self._state[section][key] = value

    def append_event(self, event: dict[str, Any]) -> None:
        """
        Append a runtime event.
        """

        with self._lock:

            self._state["events"].append(event)

    def snapshot(self) -> dict[str, Any]:
        """
        Return a full copy of runtime state.
        """

        with self._lock:

            return deepcopy(self._state)

    def clear(self) -> None:
        """
        Reset runtime state.
        """

        with self._lock:

            self.__init__()

            logger.info("Runtime state reset.")

    def health(self) -> dict[str, Any]:
        """
        Return state health information.
        """

        with self._lock:

            return {
                "sections": list(self._state.keys()),
                "events": len(self._state["events"]),
            }


state = StateManager()
