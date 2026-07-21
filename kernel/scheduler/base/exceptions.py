# kernel/scheduler/base/exceptions.py


class SchedulerError(Exception):
    """Base exception for scheduler errors."""
    pass


class JobNotFoundError(SchedulerError):
    """Raised when a job is not found."""
    pass


class JobExecutionError(SchedulerError):
    """Raised when a job execution fails."""
    pass


class InvalidTriggerError(SchedulerError):
    """Raised when a trigger definition is invalid."""
    pass


class ScheduleError(SchedulerError):
    """Raised when a schedule operation fails."""
    pass
