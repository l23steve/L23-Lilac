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
            services.append(
                {
                    "serviceArn": svc.get("serviceArn"),
                    "clusterArn": cluster,
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
            tasks.append(
                {
                    "taskArn": task.get("taskArn"),
                    "clusterArn": cluster,
                    "details": task,
                }
            )
    return tasks
