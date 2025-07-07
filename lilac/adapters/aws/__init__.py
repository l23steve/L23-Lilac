"""AWS adapter functions."""

from .s3 import list_buckets
from .ecr import list_repositories
from .ecs import list_services, list_tasks
from .ec2 import (
    list_instances,
    list_network_interfaces,
    list_security_groups,
    list_vpcs,
)
from .route53 import list_zones
from .cloudwatch import list_log_groups

__all__ = [
    "list_buckets",
    "list_repositories",
    "list_services",
    "list_tasks",
    "list_instances",
    "list_security_groups",
    "list_network_interfaces",
    "list_vpcs",
    "list_zones",
    "list_log_groups",
]
