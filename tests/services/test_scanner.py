import pytest
from lilac.services.scanner import scan, scan_resources
from lilac.domain.models import Resource
import lilac.services.scanner as scanner


def _patch_all_empty(monkeypatch) -> None:
    monkeypatch.setattr(scanner, "list_repositories", lambda: [])
    monkeypatch.setattr(scanner, "list_services", lambda: [])
    monkeypatch.setattr(scanner, "list_tasks", lambda: [])
    monkeypatch.setattr(scanner, "list_instances", lambda: [])
    monkeypatch.setattr(scanner, "list_security_groups", lambda: [])
    monkeypatch.setattr(scanner, "list_network_interfaces", lambda: [])
    monkeypatch.setattr(scanner, "list_vpcs", lambda: [])
    monkeypatch.setattr(scanner, "list_zones", lambda: [])
    monkeypatch.setattr(scanner, "list_log_groups", lambda: [])


def test_scan(monkeypatch):
    _patch_all_empty(monkeypatch)
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
    _patch_all_empty(monkeypatch)
    monkeypatch.setattr(scanner, "list_buckets", lambda: [])

    resources = scan("ns")

    assert resources == []


def test_scan_resources(monkeypatch):
    _patch_all_empty(monkeypatch)
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
    _patch_all_empty(monkeypatch)
    monkeypatch.setattr(scanner, "list_buckets", lambda: [])

    resources = scan_resources("ns")

    assert resources == []


def test_scan_resources_error(monkeypatch):
    _patch_all_empty(monkeypatch)
    def bad_list() -> list[dict]:
        raise RuntimeError("boom")

    monkeypatch.setattr(scanner, "list_buckets", bad_list)

    with pytest.raises(RuntimeError):
        scan_resources("ns")


def test_scan_additional_services(monkeypatch):
    _patch_all_empty(monkeypatch)
    monkeypatch.setattr(scanner, "list_buckets", lambda: [])
    monkeypatch.setattr(
        scanner, "list_repositories", lambda: [{"name": "repo", "arn": "arn"}]
    )

    resources = scan("ns")

    assert any(r.resource_type == "ecr-repo" for r in resources)
