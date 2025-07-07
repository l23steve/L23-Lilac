import boto3
from typing import Any


def list_log_groups() -> list[dict[str, Any]]:
    """Return CloudWatch log groups."""
    client = boto3.client("logs")
    response = client.describe_log_groups()
    return [
        {"name": group.get("logGroupName")}
        for group in response.get("logGroups", [])
    ]
