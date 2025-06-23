from pathlib import Path

import pytest

from lilac.adapters.yaml_io import (
    load_resource,
    load_resources,
    load_yaml,
    validate_resource,
)


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


def test_load_resource(tmp_path: Path) -> None:
    content = """
    type: s3-bucket
    namespace: default
    depends_on: []
    properties:
      key: value
    """
    file = tmp_path / "resource.yaml"
    file.write_text(content)

    resource = load_resource(file)

    assert resource.resource_type == "s3-bucket"
    assert resource.namespace == "default"
    assert resource.depends_on == []
    assert resource.properties == {"key": "value"}


def test_load_resource_invalid(tmp_path: Path) -> None:
    content = """
    type: s3-bucket
    namespace: default
    properties: {}
    """
    file = tmp_path / "invalid.yaml"
    file.write_text(content)

    with pytest.raises(ValueError):
        load_resource(file)


def test_load_resources_multiple(tmp_path: Path) -> None:
    content1 = """
    type: type1
    namespace: ns
    depends_on: []
    properties: {}
    """
    content2 = """
    type: type2
    namespace: ns
    depends_on: []
    properties: {}
    """
    dir_path = tmp_path / "dir"
    dir_path.mkdir()
    (dir_path / "one.yaml").write_text(content1)
    (dir_path / "two.yaml").write_text(content2)

    resources = load_resources(dir_path)

    assert {r.resource_type for r in resources} == {"type1", "type2"}

