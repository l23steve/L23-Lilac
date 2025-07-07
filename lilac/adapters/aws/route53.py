import boto3
from typing import Any


def list_zones() -> list[dict[str, Any]]:
    """Return Route53 hosted zones."""
    client = boto3.client("route53")
    response = client.list_hosted_zones()
    zones = []
    for zone in response.get("HostedZones", []):
        zone_id = zone.get("Id")
        try:
            tag_resp = client.list_tags_for_resource(
                ResourceType="hostedzone",
                ResourceId=zone_id.replace("/hostedzone/", ""),
            )
            tag_set = tag_resp.get("ResourceTagSet", {}).get("Tags", [])
            tags = {t["Key"]: t["Value"] for t in tag_set}
        except Exception:  # pragma: no cover - network issues
            tags = {}
        zones.append(
            {
                "id": zone_id,
                "name": zone.get("Name"),
                "record_set_count": zone.get("ResourceRecordSetCount"),
                "tags": tags,
                "details": zone,
            }
        )
    return zones
