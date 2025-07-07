import boto3
from typing import Any


def list_services() -> list[dict[str, Any]]:
    """Return ECS service ARNs grouped by cluster."""
    client = boto3.client("ecs")
    clusters = client.list_clusters().get("clusterArns", [])
    services: list[dict[str, Any]] = []
    for cluster in clusters:
        response = client.list_services(cluster=cluster)
        for arn in response.get("serviceArns", []):
            services.append({"serviceArn": arn, "clusterArn": cluster})
    return services


def list_tasks() -> list[dict[str, Any]]:
    """Return ECS task ARNs grouped by cluster."""
    client = boto3.client("ecs")
    clusters = client.list_clusters().get("clusterArns", [])
    tasks: list[dict[str, Any]] = []
    for cluster in clusters:
        response = client.list_tasks(cluster=cluster)
        for arn in response.get("taskArns", []):
            tasks.append({"taskArn": arn, "clusterArn": cluster})
    return tasks
