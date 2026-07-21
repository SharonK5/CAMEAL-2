# kernel/scheduler/base/trigger.py
from abc import ABC, abstractmethod
from datetime import datetime


class Trigger(ABC):
    """Base class for all triggers."""

    @abstractmethod
    def next_run(self, from_time: datetime) -> datetime:
        """Return the next run time after the given time."""
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
