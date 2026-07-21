import pytest
from datetime import datetime, timedelta
from kernel.scheduler.triggers import CronTrigger, IntervalTrigger, OnceTrigger
from kernel.scheduler.base.exceptions import InvalidTriggerError


def test_cron_trigger():
    t = CronTrigger("0 0 * * *")
    now = datetime.now()
    next_run = t.next_run(now)
    assert next_run > now
    assert next_run.hour == 0
    assert next_run.minute == 0


def test_interval_trigger():
    t = IntervalTrigger(60)
    now = datetime.now()
    next_run = t.next_run(now)
    assert next_run == now + timedelta(seconds=60)


def test_once_trigger():
    run_at = datetime.now() + timedelta(hours=1)
    t = OnceTrigger(run_at)
    now = datetime.now()
    assert t.next_run(now) == run_at
    past = run_at + timedelta(seconds=1)
    assert t.next_run(past) is None


def test_invalid_cron():
    with pytest.raises(InvalidTriggerError):
        CronTrigger("invalid")
