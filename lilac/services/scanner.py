from __future__ import annotations

from lilac.domain.models import Resource
from lilac.adapters.aws import list_buckets


def scan_resources(namespace: str) -> list[Resource]:
    """Scan AWS for resources matching ``namespace``."""
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

def scan(namespace: str) -> list[Resource]:
    """Discover AWS resources in the environment."""
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
