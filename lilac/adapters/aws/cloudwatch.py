import boto3
from typing import Any


def list_log_groups() -> list[dict[str, Any]]:
    """Return CloudWatch log groups."""
    client = boto3.client("logs")
    response = client.describe_log_groups()
    groups = []
    for group in response.get("logGroups", []):
        name = group.get("logGroupName")
        try:
            tag_resp = client.list_tags_log_group(logGroupName=name)
            tags = tag_resp.get("tags", {})
        except Exception:  # pragma: no cover - network issues
            tags = {}
        groups.append(
            {
                "name": name,
                "arn": group.get("arn"),
                "retention": group.get("retentionInDays"),
                "tags": tags,
                "details": group,
            }
        )
    return groups
