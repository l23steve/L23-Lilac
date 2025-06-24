import boto3
from typing import Any


def list_buckets() -> list[dict[str, Any]]:
    """Return basic information about all S3 buckets."""
    client = boto3.client("s3")
    response = client.list_buckets()
    buckets = response.get("Buckets", [])
    return [
        {"name": b.get("Name"), "creation_date": b.get("CreationDate")}
        for b in buckets
    ]
