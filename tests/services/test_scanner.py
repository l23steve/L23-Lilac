from lilac.services.scanner import scan
from lilac.domain.models import Resource
import lilac.services.scanner as scanner


def test_scan(monkeypatch):
    monkeypatch.setattr(
        scanner,
        "list_buckets",
        lambda: [{"name": "one", "creation_date": "today"}],
    )

    resources = scan("default")

    assert len(resources) == 1
    assert isinstance(resources[0], Resource)
    assert resources[0].properties["name"] == "one"


def test_scan_empty(monkeypatch):
    monkeypatch.setattr(scanner, "list_buckets", lambda: [])

    resources = scan("ns")

    assert resources == []
