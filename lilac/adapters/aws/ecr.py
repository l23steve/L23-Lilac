import boto3
from typing import Any


def list_repositories() -> list[dict[str, Any]]:
    """Return detailed information about all ECR repositories."""
    client = boto3.client("ecr")
    paginator = client.get_paginator("describe_repositories")
    repositories: list[dict[str, Any]] = []
    for page in paginator.paginate():
        repos = page.get("repositories", [])
        for repo in repos:
            try:
                tag_resp = client.list_tags_for_resource(
                    resourceArn=repo.get("repositoryArn")
                )
                tag_set = tag_resp.get("tags", [])
                tags = {t["Key"]: t["Value"] for t in tag_set}
            except Exception:  # pragma: no cover - network issues
                tags = {}
            repositories.append(
                {
                    "name": repo.get("repositoryName"),
                    "arn": repo.get("repositoryArn"),
                    "uri": repo.get("repositoryUri"),
                    "tags": tags,
                    "details": repo,
                }
            )
    return repositories
