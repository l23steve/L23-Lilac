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
        info = {
            "name": name,
            "creation_date": b.get("CreationDate"),
            "region": location,
        }
        info["details"] = {**b, "region": location}
        results.append(info)
    return results
