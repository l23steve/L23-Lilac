from __future__ import annotations

import pytest

from lilac.domain.models import Resource
from lilac.domain.validation import validate_against_spec


def test_validate_against_spec_success() -> None:
    spec = {
        "ResourceTypes": {
            "AWS::S3::Bucket": {
                "Properties": {"BucketName": {}}
            }
        }
    }
    resource = Resource(
        resource_type="AWS::S3::Bucket",
        namespace="ns",
        depends_on=[],
        properties={"BucketName": "name"},
    )
    validate_against_spec(resource, spec)


def test_validate_against_spec_failure() -> None:
    spec = {
        "ResourceTypes": {
            "AWS::S3::Bucket": {
                "Properties": {"BucketName": {}}
            }
        }
    }
    resource = Resource(
        resource_type="AWS::S3::Bucket",
        namespace="ns",
        depends_on=[],
        properties={"Wrong": "x"},
    )
    with pytest.raises(ValueError):
        validate_against_spec(resource, spec)

