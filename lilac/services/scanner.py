from __future__ import annotations

from typing import List, Mapping

from lilac.adapters.aws import (
    list_buckets,
    list_instances,
    list_log_groups,
    list_network_interfaces,
    list_repositories,
    list_services,
    list_tasks,
    list_security_groups,
    list_vpcs,
    list_zones,
)
from lilac.domain.models import Resource


def _tag_matches(tags: Mapping[str, str] | None, namespace: str) -> bool:
    """Return ``True`` if ``tags`` contains the requested ``namespace`` tag."""
    if not tags:
        return False
    return tags.get("namespace") == namespace


def scan_resources(namespace: str) -> List[Resource]:
    """Scan AWS for resources matching ``namespace`` tag."""
    resources: List[Resource] = []
    for bucket in list_buckets():
        tags = bucket.get("tags") or bucket.get("details", {}).get("tags")
        if not _tag_matches(tags, namespace):
            continue
        resources.append(
            Resource(
                resource_type="s3-bucket",
                namespace=namespace,
                depends_on=[],
                properties={
                    "name": bucket.get("name"),
                    "creation_date": bucket.get("creation_date"),
                    "region": bucket.get("region"),
                    "tags": tags,
                    "details": bucket.get("details"),
                },
            )
        )

    for repo in list_repositories():
        tags = repo.get("tags") or repo.get("details", {}).get("tags")
        if not _tag_matches(tags, namespace):
            continue
        resources.append(
            Resource(
                resource_type="ecr-repo",
                namespace=namespace,
                depends_on=[],
                properties={
                    "name": repo.get("name"),
                    "arn": repo.get("arn"),
                    "uri": repo.get("uri"),
                    "tags": tags,
                    "details": repo.get("details"),
                },
            )
        )

    for svc in list_services():
        tags = svc.get("tags") or svc.get("details", {}).get("tags")
        if not _tag_matches(tags, namespace):
            continue
        resources.append(
            Resource(
                resource_type="ecs-service",
                namespace=namespace,
                depends_on=[],
                properties={
                    "arn": svc.get("serviceArn"),
                    "cluster": svc.get("clusterArn"),
                    "tags": tags,
                    "details": svc.get("details"),
                },
            )
        )

    for task in list_tasks():
        tags = task.get("tags") or task.get("details", {}).get("tags")
        if not _tag_matches(tags, namespace):
            continue
        resources.append(
            Resource(
                resource_type="ecs-task",
                namespace=namespace,
                depends_on=[],
                properties={
                    "arn": task.get("taskArn"),
                    "cluster": task.get("clusterArn"),
                    "tags": tags,
                    "details": task.get("details"),
                },
            )
        )

    for inst in list_instances():
        tags = inst.get("tags") or inst.get("details", {}).get("tags")
        if not _tag_matches(tags, namespace):
            continue
        resources.append(
            Resource(
                resource_type="ec2-instance",
                namespace=namespace,
                depends_on=[],
                properties={
                    "id": inst.get("id"),
                    "type": inst.get("type"),
                    "state": inst.get("state"),
                    "tags": tags,
                    "details": inst.get("details"),
                },
            )
        )

    for sg in list_security_groups():
        tags = sg.get("tags") or sg.get("details", {}).get("tags")
        if not _tag_matches(tags, namespace):
            continue
        resources.append(
            Resource(
                resource_type="security-group",
                namespace=namespace,
                depends_on=[],
                properties={
                    "id": sg.get("id"),
                    "name": sg.get("name"),
                    "description": sg.get("description"),
                    "tags": tags,
                    "details": sg.get("details"),
                },
            )
        )

    for ni in list_network_interfaces():
        tags = ni.get("tags") or ni.get("details", {}).get("tags")
        if not _tag_matches(tags, namespace):
            continue
        resources.append(
            Resource(
                resource_type="network-interface",
                namespace=namespace,
                depends_on=[],
                properties={
                    "id": ni.get("id"),
                    "subnet_id": ni.get("subnet_id"),
                    "tags": tags,
                    "details": ni.get("details"),
                },
            )
        )

    for vpc in list_vpcs():
        tags = vpc.get("tags") or vpc.get("details", {}).get("tags")
        if not _tag_matches(tags, namespace):
            continue
        resources.append(
            Resource(
                resource_type="vpc",
                namespace=namespace,
                depends_on=[],
                properties={
                    "id": vpc.get("id"),
                    "cidr_block": vpc.get("cidr_block"),
                    "tags": tags,
                    "details": vpc.get("details"),
                },
            )
        )

    for zone in list_zones():
        tags = zone.get("tags") or zone.get("details", {}).get("tags")
        if not _tag_matches(tags, namespace):
            continue
        resources.append(
            Resource(
                resource_type="route53-zone",
                namespace=namespace,
                depends_on=[],
                properties={
                    "id": zone.get("id"),
                    "name": zone.get("name"),
                    "record_set_count": zone.get("record_set_count"),
                    "tags": tags,
                    "details": zone.get("details"),
                },
            )
        )

    for group in list_log_groups():
        tags = group.get("tags") or group.get("details", {}).get("tags")
        if not _tag_matches(tags, namespace):
            continue
        resources.append(
            Resource(
                resource_type="cloudwatch-log-group",
                namespace=namespace,
                depends_on=[],
                properties={
                    "name": group.get("name"),
                    "arn": group.get("arn"),
                    "retention": group.get("retention"),
                    "tags": tags,
                    "details": group.get("details"),
                },
            )
        )

    return resources


def scan(namespace: str) -> list[Resource]:
    """High level scanner that relies on adapter utilities for discovery."""
    return scan_resources(namespace)
