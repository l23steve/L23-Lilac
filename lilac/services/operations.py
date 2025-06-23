from __future__ import annotations

from pathlib import Path
from lilac.domain.models import Resource

from lilac.adapters import load_yaml, validate_resource

def placeholder_service() -> bool:
    """Service placeholder."""
    return True


def load_resources(directory: Path) -> list[Resource]:
    """Load and validate all YAML resources in ``directory``."""

    if not directory.is_dir():
        raise NotADirectoryError(directory)

    resources: list[Resource] = []
    for path in directory.glob("*.yaml"):
        data = load_yaml(path)
        validate_resource(data)
        resources.append(
            Resource(
                resource_type=data["type"],
                namespace=data["namespace"],
                depends_on=list(data["depends_on"]),
                properties=dict(data["properties"]),
            )
        )
    return resources


def validate_directory(path: Path) -> list[Resource]:
    """Validate all resource files in a directory."""

    resources = load_resources(path)
    if not resources:
        raise ValueError("no resources found")
    return resources
