import boto3
from typing import Any


def list_zones() -> list[dict[str, Any]]:
    """Return Route53 hosted zones."""
    client = boto3.client("route53")
    response = client.list_hosted_zones()
    return [
        {"id": zone.get("Id"), "name": zone.get("Name")}
        for zone in response.get("HostedZones", [])
    ]
