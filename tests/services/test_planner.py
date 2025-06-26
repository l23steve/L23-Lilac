from lilac.domain.models import Resource
import pytest
import lilac.services.planner as planner


def test_plan(monkeypatch):
    desired = [Resource("type", "ns", [], {})]
    monkeypatch.setattr(planner, "load_resources", lambda d: desired)
    monkeypatch.setattr(planner, "scan_resources", lambda ns: [])

    actions = planner.plan("dir", "ns")

    assert len(actions) == 1
    assert actions[0].action == "create"


def test_plan_error(monkeypatch):
    def bad_scan(ns: str):
        raise RuntimeError("boom")

    monkeypatch.setattr(planner, "load_resources", lambda d: [])
    monkeypatch.setattr(planner, "scan_resources", bad_scan)

    with pytest.raises(RuntimeError):
        planner.plan("dir", "ns")
