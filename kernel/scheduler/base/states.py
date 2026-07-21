# kernel/scheduler/base/states.py
"""
Explicit job state model for the scheduler.
"""

from enum import Enum, auto


class JobState(Enum):
    """Represents the state of a scheduled job."""
    PENDING = auto()      # Job created but not yet scheduled
    SCHEDULED = auto()    # Job has a next run time set
    READY = auto()        # Job is ready to run (due)
    RUNNING = auto()      # Job is currently executing
    RETRYING = auto()     # Job is retrying after a failure
    COMPLETED = auto()    # Job completed successfully
    FAILED = auto()       # Job failed (retries exhausted)
    CANCELLED = auto()    # Job was cancelled
    PAUSED = auto()       # Job is temporarily suspended

    @classmethod
    def is_terminal(cls, state: "JobState") -> bool:
        """Return True if the state is terminal (no further transitions)."""
        return state in (cls.COMPLETED, cls.FAILED, cls.CANCELLED)

    @classmethod
    def is_active(cls, state: "JobState") -> bool:
        """Return True if the job is active (not terminal or paused)."""
        return state not in (cls.COMPLETED, cls.FAILED, cls.CANCELLED, cls.PAUSED)
