from __future__ import annotations

from typing import List
from lilac.domain.models import Resource
import boto3


def scan_resources(namespace: str) -> List[Resource]:
    """Scan AWS for resources matching ``namespace``."""
    s3 = boto3.client("s3")
    result = s3.list_buckets()
    resources: List[Resource] = []
    for idx, bucket in enumerate(result.get("Buckets", [])):
        resources.append(
            Resource(
                resource_type="s3-bucket",
                namespace=namespace,
                depends_on=[],
                properties={"name": bucket["Name"]},
            )
        )
    return resources
