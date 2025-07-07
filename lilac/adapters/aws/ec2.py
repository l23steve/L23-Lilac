import boto3
from typing import Any


def list_instances() -> list[dict[str, Any]]:
    """Return information about EC2 instances."""
    client = boto3.client("ec2")
    response = client.describe_instances()
    instances: list[dict[str, Any]] = []
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            instances.append(
                {
                    "id": instance.get("InstanceId"),
                    "type": instance.get("InstanceType"),
                }
            )
    return instances


def list_security_groups() -> list[dict[str, Any]]:
    """Return security groups."""
    client = boto3.client("ec2")
    response = client.describe_security_groups()
    return [
        {"id": sg.get("GroupId"), "name": sg.get("GroupName")}
        for sg in response.get("SecurityGroups", [])
    ]


def list_network_interfaces() -> list[dict[str, Any]]:
    """Return network interfaces."""
    client = boto3.client("ec2")
    response = client.describe_network_interfaces()
    return [
        {"id": ni.get("NetworkInterfaceId")}
        for ni in response.get("NetworkInterfaces", [])
    ]


def list_vpcs() -> list[dict[str, Any]]:
    """Return VPCs."""
    client = boto3.client("ec2")
    response = client.describe_vpcs()
    return [
        {"id": vpc.get("VpcId")}
        for vpc in response.get("Vpcs", [])
    ]
