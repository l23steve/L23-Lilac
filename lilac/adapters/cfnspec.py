from __future__ import annotations

import json
from pathlib import Path

import requests


CACHE_DIR = Path.home() / ".lilac"
CACHE_DIR.mkdir(exist_ok=True)

SPEC_URL = (
    "https://d1uauaxba7bl26.cloudfront.net/latest/gzip/{region}/"
    "CloudFormationResourceSpecification.json"
)


def _spec_path(region: str) -> Path:
    """Return the local cache path for a region."""
    return CACHE_DIR / f"spec_{region}.json"


def download_spec(region: str) -> dict:
    """Download the CloudFormation spec for ``region``."""
    url = SPEC_URL.format(region=region)
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def load_spec(region: str) -> dict:
    """Load the CloudFormation spec for ``region`` from cache or download."""
    path = _spec_path(region)
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    spec = download_spec(region)
    with path.open("w", encoding="utf-8") as f:
        json.dump(spec, f)
    return spec

