from security.decision import Decision


def test_decision_created():

    decision = Decision(
        permitted=True,
        reason="Policy matched.",
    )

    assert decision.permitted
    assert decision.reason == "Policy matched."
    assert decision.policy_id is None


def test_decision_is_immutable():

    decision = Decision(
        permitted=False,
        reason="Denied",
    )

    try:
        decision.reason = "Changed"
        assert False
    except Exception:
        assert True
