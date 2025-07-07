import boto3
from typing import Any


def list_buckets() -> list[dict[str, Any]]:
    """Return detailed information about all S3 buckets."""
    client = boto3.client("s3")
    response = client.list_buckets()
    buckets = response.get("Buckets", [])
    results: list[dict[str, Any]] = []
    for b in buckets:
        name = b.get("Name")
        try:
            loc_resp = client.get_bucket_location(Bucket=name)
            location = loc_resp.get("LocationConstraint") or "us-east-1"
        except Exception:  # pragma: no cover - network issues
            location = None
        try:
            tag_resp = client.get_bucket_tagging(Bucket=name)
            tag_set = tag_resp.get("TagSet", [])
            tags = {t["Key"]: t["Value"] for t in tag_set}
        except Exception:  # pragma: no cover - network issues
            tags = {}
        info = {
            "name": name,
            "creation_date": b.get("CreationDate"),
            "region": location,
            "tags": tags,
        }
        info["details"] = {**b, "region": location, "tags": tags}
        results.append(info)
    return results
