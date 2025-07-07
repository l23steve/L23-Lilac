import boto3
from typing import Any


def list_repositories() -> list[dict[str, Any]]:
    """Return basic information about all ECR repositories."""
    client = boto3.client("ecr")
    paginator = client.get_paginator("describe_repositories")
    repositories: list[dict[str, Any]] = []
    for page in paginator.paginate():
        repos = page.get("repositories", [])
        for repo in repos:
            repositories.append({
                "name": repo.get("repositoryName"),
                "arn": repo.get("repositoryArn"),
            })
    return repositories
