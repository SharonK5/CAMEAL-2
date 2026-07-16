from query.execution.execution_context import ExecutionContext
from query.execution.context_keys import ContextKeys


def test_set_get():

    ctx = ExecutionContext()

    ctx.set("country", "Kenya")

    assert ctx.get("country") == "Kenya"


def test_default():

    ctx = ExecutionContext()

    assert ctx.get("missing") is None


def test_contains():

    ctx = ExecutionContext()

    ctx.set("a", 1)

    assert ctx.contains("a")

    assert not ctx.contains("b")


def test_remove():

    ctx = ExecutionContext()

    ctx.set("a", 10)

    ctx.remove("a")

    assert not ctx.contains("a")


def test_clear():

    ctx = ExecutionContext()

    ctx.set("a", 1)

    ctx.set("b", 2)

    ctx.clear()

    assert ctx.to_dict() == {}


def test_to_dict_returns_copy():

    ctx = ExecutionContext()

    ctx.set("x", 5)

    d = ctx.to_dict()

    d["x"] = 100

    assert ctx.get("x") == 5


# New test using ContextKeys constants
def test_store_using_context_keys():

    context = ExecutionContext()

    context.set(
        ContextKeys.VALIDATED,
        True,
    )

    assert context.get(
        ContextKeys.VALIDATED
    ) is True
