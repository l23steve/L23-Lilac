from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

import yaml


REQUIRED_FIELDS: dict[str, type] = {
    "type": str,
    "namespace": str,
    "depends_on": list,
    "properties": dict,
}


def load_yaml(path: str | Path) -> Any:
    """Load a YAML file and return the parsed data."""
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


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

