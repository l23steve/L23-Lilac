from pathlib import Path

import pytest

from lilac.domain.models import Resource
from lilac.services.operations import (
    placeholder_service,
    validate_directory,
)


def test_placeholder_service() -> None:
    assert placeholder_service() is True


def test_validate_directory_success(tmp_path: Path) -> None:
    valid = tmp_path / "valid.yaml"
    valid.write_text(
        """
        type: s3-bucket
        namespace: default
        depends_on: []
        properties:
          name: bucket
        """
    )

    resources = validate_directory(tmp_path)

    assert len(resources) == 1
    assert isinstance(resources[0], Resource)
    assert resources[0].resource_type == "s3-bucket"


def test_validate_directory_failure(tmp_path: Path) -> None:
    invalid = tmp_path / "invalid.yaml"
    invalid.write_text(
        """
        type: s3-bucket
        namespace: default
        properties: {}
        """
    )

    with pytest.raises(ValueError):
        validate_directory(tmp_path)


def test_validate_directory_recursive(tmp_path: Path) -> None:
    nested = tmp_path / "nested"
    nested.mkdir()
    resource_file = nested / "res.yaml"
    resource_file.write_text(
        """
        type: s3-bucket
        namespace: default
        depends_on: []
        properties: {}
        """
    )

    resources = validate_directory(tmp_path)

    assert len(resources) == 1
    assert resources[0].resource_type == "s3-bucket"
