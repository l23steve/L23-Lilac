from __future__ import annotations

from pathlib import Path

from lilac.adapters import cfnspec


class FakeResponse:
    def __init__(self, data: dict) -> None:
        self._data = data

    def raise_for_status(self) -> None:  # pragma: no cover - nothing to do
        pass

    def json(self) -> dict:
        return self._data


def test_load_spec_download_and_cache(monkeypatch, tmp_path: Path) -> None:
    data = {"ResourceTypes": {}}

    def fake_get(url: str, timeout: int = 10) -> FakeResponse:  # noqa: D401
        return FakeResponse(data)

    monkeypatch.setattr(cfnspec, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(cfnspec.requests, "get", fake_get)

    spec = cfnspec.load_spec("us-east-1")
    assert spec == data
    cache_file = tmp_path / "spec_us-east-1.json"
    assert cache_file.exists()

    # Second call should read from cache and not invoke requests.get
    monkeypatch.setattr(
        cfnspec.requests,
        "get",
        lambda *a, **k: (_ for _ in ()).throw(Exception("network")),
    )
    spec2 = cfnspec.load_spec("us-east-1")
    assert spec2 == data

