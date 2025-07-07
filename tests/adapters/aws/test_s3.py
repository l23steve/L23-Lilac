from lilac.adapters.aws import s3
import pytest


class FakeClient:
    def __init__(self, buckets=None, locations=None, tags=None, fail=False):
        self.buckets = buckets or []
        self.locations = locations or {}
        self.tags = tags or {}
        self.fail = fail

    def list_buckets(self):
        if self.fail:
            raise Exception("failed")
        return {"Buckets": self.buckets}

    def get_bucket_location(self, Bucket):
        if self.fail:
            raise Exception("failed")
        return {"LocationConstraint": self.locations.get(Bucket)}

    def get_bucket_tagging(self, Bucket):
        if self.fail:
            raise Exception("failed")
        tag_set = [
            {"Key": k, "Value": v} for k, v in self.tags.get(Bucket, {}).items()
        ]
        return {"TagSet": tag_set}


def test_list_buckets(monkeypatch):
    fake = FakeClient(
        buckets=[{"Name": "one", "CreationDate": "today"}],
        locations={"one": "us-west-2"},
        tags={"one": {"env": "prod"}},
    )
    monkeypatch.setattr(s3.boto3, "client", lambda service: fake)

    buckets = s3.list_buckets()

    assert buckets[0]["name"] == "one"
    assert buckets[0]["region"] == "us-west-2"
    assert buckets[0]["tags"] == {"env": "prod"}
    assert "details" in buckets[0]


def test_list_buckets_error(monkeypatch):
    fake = FakeClient(fail=True)
    monkeypatch.setattr(s3.boto3, "client", lambda service: fake)

    with pytest.raises(Exception):
        s3.list_buckets()
