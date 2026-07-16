from query.execution.contracts import StageResult


def test_create():

    result = StageResult(

        success=True,

        stage="validation",

    )

    assert result.success

    assert result.stage == "validation"


def test_metadata():

    result = StageResult(

        success=True,

        stage="validation",

        metadata=(

            ("engine", "pytest"),

        ),

    )

    assert result.contains_metadata("engine")

    assert result.get_metadata("engine") == "pytest"

    assert result.get_metadata("missing") is None


def test_to_dict():

    result = StageResult(

        success=True,

        stage="validation",

    )

    data = result.to_dict()

    assert data["success"] is True

    assert data["stage"] == "validation"


def test_round_trip():

    result = StageResult(

        success=False,

        stage="security",

        metadata=(

            ("reason", "denied"),

        ),

    )

    restored = StageResult.from_dict(

        result.to_dict()

    )

    assert restored.success is False

    assert restored.stage == "security"

    assert restored.get_metadata("reason") == "denied"
