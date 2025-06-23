from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from lilac.adapters import load_resources as adapter_load_resources


@dataclass
class Resource:
    """Simple resource representation."""

    type: str
    namespace: str
    depends_on: list[str]
    properties: dict[str, Any]


def placeholder_service() -> bool:
    """Service placeholder."""
    return True


def load_resources(directory: Path) -> list[Resource]:
    """Load and validate all YAML resources in ``directory``."""

    if not directory.is_dir():
        raise NotADirectoryError(directory)

    resources: list[Resource] = []
    for parsed in adapter_load_resources(directory):
        resources.append(
            Resource(
                type=parsed.resource_type,
                namespace=parsed.namespace,
                depends_on=parsed.depends_on,
                properties=parsed.properties,
            )
        )
    return resources


def validate_directory(path: Path) -> list[Resource]:
    """Validate all resource files in a directory."""

    resources = load_resources(path)
    if not resources:
        raise ValueError("no resources found")
    return resources
