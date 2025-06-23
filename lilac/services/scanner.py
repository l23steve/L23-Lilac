from __future__ import annotations

from lilac.adapters.aws import list_buckets
from lilac.domain.models import Resource


def scan(namespace: str) -> list[Resource]:
    """Discover AWS resources in the environment."""
    resources: list[Resource] = []
    for bucket in list_buckets():
        resources.append(
            Resource(
                resource_type="s3-bucket",
                namespace=namespace,
                properties={
                    "name": bucket.get("name"),
                    "creation_date": bucket.get("creation_date"),
                },
            )
        )
    return resources
