import pytest
from lilac.services.scanner import scan, scan_resources
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


def test_scan_resources(monkeypatch):
    monkeypatch.setattr(
        scanner,
        "list_buckets",
        lambda: [{"name": "one", "creation_date": "today"}],
    )

    resources = scan_resources("ns")

    assert len(resources) == 1
    assert isinstance(resources[0], Resource)
    assert resources[0].properties["name"] == "one"

    
def test_scan_resources_empty(monkeypatch):
    monkeypatch.setattr(scanner, "list_buckets", lambda: [])

    resources = scan_resources("ns")

    assert resources == []


def test_scan_resources_error(monkeypatch):
    def bad_list() -> list[dict]:
        raise RuntimeError("boom")

    monkeypatch.setattr(scanner, "list_buckets", bad_list)

    with pytest.raises(RuntimeError):
        scan_resources("ns")
