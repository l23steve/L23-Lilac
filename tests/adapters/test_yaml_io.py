from pathlib import Path

import pytest

from lilac.adapters.yaml_io import load_yaml, validate_resource


def test_load_and_validate_yaml(tmp_path: Path) -> None:
    content = """
    type: s3-bucket
    namespace: default
    depends_on:
      - another
    properties:
      key: value
    """
    file = tmp_path / "resource.yaml"
    file.write_text(content)

    data = load_yaml(file)
    validate_resource(data)

    assert data["type"] == "s3-bucket"


def test_validate_yaml_missing_field(tmp_path: Path) -> None:
    content = """
    type: s3-bucket
    namespace: default
    properties: {}
    """
    file = tmp_path / "bad.yaml"
    file.write_text(content)

    data = load_yaml(file)
    with pytest.raises(ValueError):
        validate_resource(data)


def test_validate_yaml_wrong_type(tmp_path: Path) -> None:
    content = """
    type: s3-bucket
    namespace: default
    depends_on: other
    properties: {}
    """
    file = tmp_path / "wrong.yaml"
    file.write_text(content)

    data = load_yaml(file)
    with pytest.raises(TypeError):
        validate_resource(data)

