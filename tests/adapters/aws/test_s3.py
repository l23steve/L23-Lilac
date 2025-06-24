from lilac.adapters.aws import s3
import pytest


class FakeClient:
    def __init__(self, buckets=None, fail=False):
        self.buckets = buckets or []
        self.fail = fail

    def list_buckets(self):
        if self.fail:
            raise Exception("failed")
        return {"Buckets": self.buckets}


def test_list_buckets(monkeypatch):
    fake = FakeClient(buckets=[{"Name": "one", "CreationDate": "today"}])
    monkeypatch.setattr(s3.boto3, "client", lambda service: fake)

    buckets = s3.list_buckets()

    assert buckets == [{"name": "one", "creation_date": "today"}]


def test_list_buckets_error(monkeypatch):
    fake = FakeClient(fail=True)
    monkeypatch.setattr(s3.boto3, "client", lambda service: fake)

    with pytest.raises(Exception):
        s3.list_buckets()
