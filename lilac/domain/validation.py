from __future__ import annotations

from lilac.domain.models import Resource


def validate_against_spec(resource: Resource, spec: dict) -> None:
    """Validate a Resource against the CloudFormation specification."""
    resource_types = spec.get("ResourceTypes", {})
    if resource.resource_type not in resource_types:
        raise ValueError(f"Unknown resource type: {resource.resource_type}")

    properties_spec = resource_types[resource.resource_type].get("Properties", {})
    for prop in resource.properties:
        if prop not in properties_spec:
            raise ValueError(
                f"Unknown property '{prop}' for {resource.resource_type}"
            )

