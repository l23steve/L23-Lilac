from lilac.domain.models import Resource
from lilac.domain.plan import PlanAction
import lilac.services.deployer as deployer
import pytest


class FakeS3Client:
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.created: list[tuple[str, dict]] = []
        self.deleted: list[str] = []

    def create_bucket(self, Bucket: str, **kwargs) -> None:
        if self.fail:
            raise Exception("fail")
        self.created.append((Bucket, kwargs))

    def delete_bucket(self, Bucket: str) -> None:
        if self.fail:
            raise Exception("fail")
        self.deleted.append(Bucket)

    def put_bucket_tagging(self, Bucket: str, Tagging: dict) -> None:
        if self.fail:
            raise Exception("fail")


def test_deploy_dry_run(monkeypatch):
    res = Resource("s3-bucket", "ns", [], {"name": "b"})
    monkeypatch.setattr(
        deployer,
        "plan_changes",
        lambda d, ns: [PlanAction("create", res)],
    )
    monkeypatch.setattr(
        deployer.boto3,
        "client",
        lambda service: FakeS3Client(fail=True),
    )
    actions = deployer.deploy("dir", "ns", dry_run=True)
    assert len(actions) == 1
    assert actions[0].action == "create"


def test_deploy_apply(monkeypatch):
    res = Resource("s3-bucket", "ns", [], {"name": "b"})
    monkeypatch.setattr(
        deployer,
        "plan_changes",
        lambda d, ns: [PlanAction("create", res)],
    )
    fake = FakeS3Client()
    monkeypatch.setattr(deployer.boto3, "client", lambda service: fake)
    actions = deployer.deploy("dir", "ns", dry_run=False)
    assert len(actions) == 1
    assert fake.created[0][0] == "b"


def test_deploy_apply_error(monkeypatch):
    res = Resource("s3-bucket", "ns", [], {"name": "b"})
    monkeypatch.setattr(
        deployer,
        "plan_changes",
        lambda d, ns: [PlanAction("create", res)],
    )
    fake = FakeS3Client(fail=True)
    monkeypatch.setattr(deployer.boto3, "client", lambda service: fake)
    with pytest.raises(Exception):
        deployer.deploy("dir", "ns", dry_run=False)
