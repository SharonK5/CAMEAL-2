import pytest
from unittest.mock import Mock

from query.execution import RepositoryStage, ExecutionContext, ContextKeys
from query.execution.contracts import RepositoryResult
from query.query_request import QueryRequest
from query.query_intent import QueryIntent


class DummyRepositoryManager:
    def get(self, identifier):
        return Mock(name=identifier)


def test_repository_stage():
    manager = DummyRepositoryManager()
    stage = RepositoryStage(manager)
    request = QueryRequest(
        identifier="1",
        intent=QueryIntent.RETRIEVE,
        query="climate",
        repositories=("repo1", "repo2"),
    )
    context = ExecutionContext()

    result = stage.execute(request, context)

    assert result.success
    assert isinstance(result, RepositoryResult)
    assert result.count == 2
    assert len(result.repositories) == 2
    stored_repos = context.get(ContextKeys.REPOSITORIES)
    assert stored_repos is not None
    assert len(stored_repos) == 2


def test_repository_stage_name():
    manager = DummyRepositoryManager()
    stage = RepositoryStage(manager)
    assert stage.name == "repository"
