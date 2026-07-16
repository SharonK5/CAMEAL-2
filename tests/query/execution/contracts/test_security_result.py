from query.execution.contracts import SecurityResult


def test_allowed():

    result = SecurityResult(

        success=True,

        stage="security",

        allowed=True,

    )

    assert result.allowed

    assert not result.denied


def test_denied():

    result = SecurityResult(

        success=False,

        stage="security",

        allowed=False,

    )

    assert result.denied


def test_to_dict():

    result = SecurityResult(

        success=True,

        stage="security",

        allowed=True,

        risk_level="LOW",

        audit_identifier="AUD-1",

    )

    data = result.to_dict()

    assert data["allowed"]

    assert data["risk_level"] == "LOW"


def test_round_trip():

    result = SecurityResult(

        success=False,

        stage="security",

        allowed=False,

        risk_level="HIGH",

        audit_identifier="AUD-9",

    )

    restored = SecurityResult.from_dict(

        result.to_dict()

    )

    assert restored.allowed is False

    assert restored.risk_level == "HIGH"
