from __future__ import annotations

from pathlib import Path
from typing import Any, List

import boto3

from lilac.domain.plan import PlanAction
from lilac.services.planner import plan as plan_changes


def deploy(
    directory: str | Path,
    namespace: str,
    dry_run: bool = False,
) -> List[PlanAction]:
    """Generate a plan and optionally apply it.

    When ``dry_run`` is ``True`` the function simply returns the planned
    actions without applying them. Otherwise each action is executed using
    boto3 calls. Currently only a subset of resources is supported.
    """

    actions = plan_changes(directory, namespace)
    if dry_run:
        return actions

    for action in actions:
        _apply_action(action)

    return actions


def _apply_action(action: PlanAction) -> None:
    """Apply a single ``PlanAction`` using boto3."""
    res = action.resource
    if res.resource_type == "s3-bucket":
        _apply_s3(action.action, res.properties)
    # Other resource types could be handled here in the future.


def _apply_s3(action: str, props: dict[str, Any]) -> None:
    client = boto3.client("s3")
    name = props.get("name")
    if not name:
        return

    if action == "create":
        region = props.get("region")
        extra: dict[str, Any] = {}
        if region and region != "us-east-1":
            extra["CreateBucketConfiguration"] = {
                "LocationConstraint": region
            }
        client.create_bucket(Bucket=name, **extra)
    elif action == "delete":
        client.delete_bucket(Bucket=name)
    elif action == "update":
        # Basic tag update example; extend as needed
        tags = props.get("tags")
        if tags:
            tagset = [
                {"Key": k, "Value": v} for k, v in tags.items()
            ]
            client.put_bucket_tagging(
                Bucket=name,
                Tagging={"TagSet": tagset},
            )
