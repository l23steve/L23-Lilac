import boto3
from typing import Any


def list_instances() -> list[dict[str, Any]]:
    """Return information about EC2 instances."""
    client = boto3.client("ec2")
    response = client.describe_instances()
    instances: list[dict[str, Any]] = []
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            tag_set = instance.get("Tags", [])
            tags = {t["Key"]: t["Value"] for t in tag_set}
            inst = {
                "id": instance.get("InstanceId"),
                "type": instance.get("InstanceType"),
                "state": instance.get("State", {}).get("Name"),
                "tags": tags,
                "details": instance,
            }
            instances.append(inst)
    return instances


def list_security_groups() -> list[dict[str, Any]]:
    """Return security groups."""
    client = boto3.client("ec2")
    response = client.describe_security_groups()
    groups = []
    for sg in response.get("SecurityGroups", []):
        tag_set = sg.get("Tags", [])
        tags = {t["Key"]: t["Value"] for t in tag_set}
        groups.append(
            {
                "id": sg.get("GroupId"),
                "name": sg.get("GroupName"),
                "description": sg.get("Description"),
                "tags": tags,
                "details": sg,
            }
        )
    return groups


def list_network_interfaces() -> list[dict[str, Any]]:
    """Return network interfaces."""
    client = boto3.client("ec2")
    response = client.describe_network_interfaces()
    interfaces = []
    for ni in response.get("NetworkInterfaces", []):
        tag_set = ni.get("TagSet", [])
        tags = {t["Key"]: t["Value"] for t in tag_set}
        interfaces.append(
            {
                "id": ni.get("NetworkInterfaceId"),
                "subnet_id": ni.get("SubnetId"),
                "tags": tags,
                "details": ni,
            }
        )
    return interfaces


def list_vpcs() -> list[dict[str, Any]]:
    """Return VPCs."""
    client = boto3.client("ec2")
    response = client.describe_vpcs()
    vpcs = []
    for vpc in response.get("Vpcs", []):
        tag_set = vpc.get("Tags", [])
        tags = {t["Key"]: t["Value"] for t in tag_set}
        vpcs.append(
            {
                "id": vpc.get("VpcId"),
                "cidr_block": vpc.get("CidrBlock"),
                "tags": tags,
                "details": vpc,
            }
        )
    return vpcs
