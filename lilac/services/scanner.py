from __future__ import annotations

from typing import List

import boto3

from lilac.adapters.aws import list_buckets
from lilac.domain.models import Resource


def scan_resources(namespace: str) -> List[Resource]:
    """Return ``Resource`` models discovered via direct AWS API calls."""
    s3 = boto3.client("s3")
    result = s3.list_buckets()
    resources: List[Resource] = []
    for bucket in result.get("Buckets", []):
        resources.append(
            Resource(
                resource_type="s3-bucket",
                namespace=namespace,
                depends_on=[],
                properties={
                    "name": bucket.get("Name"),
                    "creation_date": bucket.get("CreationDate"),
                },
            )
        )
    return resources

def scan(namespace: str) -> list[Resource]:
    """High level scanner that relies on adapter utilities for discovery."""
    resources: list[Resource] = []
    for bucket in list_buckets():
        resources.append(
            Resource(
                resource_type="s3-bucket",
                namespace=namespace,
                depends_on=[],
                properties={
                    "name": bucket.get("name"),
                    "creation_date": bucket.get("creation_date"),
                },
            )
        )
    return resources
