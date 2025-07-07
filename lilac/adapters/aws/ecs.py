import boto3
from typing import Any


def list_services() -> list[dict[str, Any]]:
    """Return ECS services with full configuration."""
    client = boto3.client("ecs")
    clusters = client.list_clusters().get("clusterArns", [])
    services: list[dict[str, Any]] = []
    for cluster in clusters:
        response = client.list_services(cluster=cluster)
        arns = response.get("serviceArns", [])
        if not arns:
            continue
        details = client.describe_services(cluster=cluster, services=arns)
        for svc in details.get("services", []):
            try:
                tag_resp = client.list_tags_for_resource(
                    resourceArn=svc.get("serviceArn")
                )
                tag_set = tag_resp.get("tags", [])
                tags = {t["Key"]: t["Value"] for t in tag_set}
            except Exception:  # pragma: no cover - network issues
                tags = {}
            services.append(
                {
                    "serviceArn": svc.get("serviceArn"),
                    "clusterArn": cluster,
                    "tags": tags,
                    "details": svc,
                }
            )
    return services


def list_tasks() -> list[dict[str, Any]]:
    """Return ECS tasks with full configuration."""
    client = boto3.client("ecs")
    clusters = client.list_clusters().get("clusterArns", [])
    tasks: list[dict[str, Any]] = []
    for cluster in clusters:
        response = client.list_tasks(cluster=cluster)
        arns = response.get("taskArns", [])
        if not arns:
            continue
        details = client.describe_tasks(cluster=cluster, tasks=arns)
        for task in details.get("tasks", []):
            try:
                tag_resp = client.list_tags_for_resource(
                    resourceArn=task.get("taskArn")
                )
                tag_set = tag_resp.get("tags", [])
                tags = {t["Key"]: t["Value"] for t in tag_set}
            except Exception:  # pragma: no cover - network issues
                tags = {}
            tasks.append(
                {
                    "taskArn": task.get("taskArn"),
                    "clusterArn": cluster,
                    "tags": tags,
                    "details": task,
                }
            )
    return tasks
