from lilac.domain.models import Resource
from lilac.domain.plan import PlanAction
import lilac.services.deployer as deployer


def test_deploy_dry_run(monkeypatch):
    res = Resource("s3-bucket", "ns", [], {})
    monkeypatch.setattr(
        deployer,
        "plan_changes",
        lambda d, ns: [PlanAction("create", res)],
    )
    actions = deployer.deploy("dir", "ns", dry_run=True)
    assert len(actions) == 1
    assert actions[0].action == "create"


def test_deploy_apply(monkeypatch):
    res = Resource("s3-bucket", "ns", [], {})
    monkeypatch.setattr(
        deployer,
        "plan_changes",
        lambda d, ns: [PlanAction("create", res)],
    )
    actions = deployer.deploy("dir", "ns", dry_run=False)
    assert len(actions) == 1
    assert actions[0].resource == res
