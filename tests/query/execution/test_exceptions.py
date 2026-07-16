from query.execution.exceptions import (
    ExecutionError,
    StageExecutionError,
    PipelineExecutionError,
    StageRegistrationError,
    DuplicateStageError,
    StageNotFoundError,
)


def test_execution_error():

    assert issubclass(
        ExecutionError,
        Exception,
    )


def test_stage_execution_error():

    assert issubclass(
        StageExecutionError,
        ExecutionError,
    )


def test_pipeline_execution_error():

    assert issubclass(
        PipelineExecutionError,
        ExecutionError,
    )


def test_stage_registration_error():

    assert issubclass(
        StageRegistrationError,
        ExecutionError,
    )


def test_duplicate_stage_error():

    assert issubclass(
        DuplicateStageError,
        StageRegistrationError,
    )


def test_stage_not_found_error():

    assert issubclass(
        StageNotFoundError,
        ExecutionError,
    )
