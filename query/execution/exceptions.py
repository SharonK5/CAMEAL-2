"""
===============================================================================
Module: query.execution.exceptions

Execution framework exceptions.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations


class ExecutionError(Exception):
    """
    Base exception for execution failures.
    """


class StageExecutionError(ExecutionError):
    """
    Raised when an execution stage fails.
    """


class PipelineExecutionError(ExecutionError):
    """
    Raised when pipeline execution cannot continue.
    """


class StageRegistrationError(ExecutionError):
    """
    Raised when an invalid stage is registered.
    """


class DuplicateStageError(StageRegistrationError):
    """
    Raised when duplicate stage names are registered.
    """


class StageNotFoundError(ExecutionError):
    """
    Raised when a requested stage cannot be found.
    """
