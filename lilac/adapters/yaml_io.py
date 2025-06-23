from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from lilac.domain.models import Resource

import yaml


REQUIRED_FIELDS: dict[str, type] = {
    "type": str,
    "namespace": str,
    "depends_on": list,
    "properties": dict,
}


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML file and return the raw mapping."""
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, Mapping):
        raise TypeError("YAML root must be a mapping")

    return dict(data)


def validate_resource(data: Mapping[str, Any]) -> None:
    """Validate that the resource dictionary contains required fields."""
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
        if not isinstance(data[field], expected_type):
            raise TypeError(
                f"Field '{field}' must be of type {expected_type.__name__}, "
                f"got {type(data[field]).__name__}"
            )


def load_resource(path: Path) -> Resource:
    """Load a single YAML file into a :class:`Resource`."""
    data = load_yaml(path)
    validate_resource(data)
    return Resource(
        resource_type=data["type"],
        namespace=data["namespace"],
        depends_on=list(data["depends_on"]),
        properties=dict(data["properties"]),
        ignore=data.get("ignore", False),
    )


def load_resources(directory: Path) -> list[Resource]:
    """Recursively load all ``.yaml`` files in ``directory`` as ``Resource`` objects."""
    resources: list[Resource] = []
    for file_path in Path(directory).rglob("*.yaml"):
        resources.append(load_resource(file_path))
    return resources

