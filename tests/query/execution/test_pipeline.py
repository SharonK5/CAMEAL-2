import pytest

from query.execution.pipeline import ExecutionPipeline
from query.execution.stage import ExecutionStage
from query.execution.execution_context import ExecutionContext
from query.execution.exceptions import DuplicateStageError

from query.query_request import QueryRequest
from query.query_response import QueryResponse
from query.query_intent import QueryIntent


def make_request():

    return QueryRequest(
        identifier="q1",
        intent=QueryIntent.RETRIEVE,
        query="Retrieve policy",
    )


class FirstStage(ExecutionStage):

    @property
    def name(self):

        return "first"

    def execute(self, request, context):

        context.set("first", True)

        return None


class FinalStage(ExecutionStage):

    @property
    def name(self):

        return "final"

    def execute(self, request, context):

        return QueryResponse(
            identifier=request.identifier,
            success=True,
            message="Done",
        )


def test_add_stage():

    pipeline = ExecutionPipeline()

    pipeline.add_stage(FirstStage())

    assert len(pipeline.stages) == 1


def test_duplicate_stage():

    pipeline = ExecutionPipeline()

    pipeline.add_stage(FirstStage())

    with pytest.raises(DuplicateStageError):

        pipeline.add_stage(FirstStage())


def test_remove_stage():

    pipeline = ExecutionPipeline()

    pipeline.add_stage(FirstStage())

    pipeline.remove_stage("first")

    assert len(pipeline.stages) == 0


def test_clear():

    pipeline = ExecutionPipeline()

    pipeline.add_stage(FirstStage())

    pipeline.clear()

    assert pipeline.stages == ()


def test_execute_pipeline():

    pipeline = ExecutionPipeline()

    pipeline.add_stage(FirstStage())

    pipeline.add_stage(FinalStage())

    # Create an explicit context to pass to the pipeline
    context = ExecutionContext()

    response = pipeline.execute(
        make_request(),
        context=context,
    )

    assert response.success
    # Optionally verify that the context was modified by FirstStage
    assert context.get("first") is True


def test_empty_pipeline():

    pipeline = ExecutionPipeline()

    # For an empty pipeline, we still pass a context (though it won't be used)
    context = ExecutionContext()

    assert pipeline.execute(
        make_request(),
        context=context,
    ) is None
