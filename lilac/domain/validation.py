from __future__ import annotations

from lilac.domain.models import Resource

TYPE_MAPPING = {
    "String": str,
    "Integer": int,
    "Long": int,
    "Double": (int, float),
    "Boolean": bool,
    "Json": dict,
    "List": list,
    "Map": dict,
}


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

    for name, prop_spec in properties_spec.items():
        if prop_spec.get("Required") and name not in resource.properties:
            raise ValueError(
                f"Missing required property '{name}' for {resource.resource_type}"
            )

    for name, value in resource.properties.items():
        spec_details = properties_spec.get(name, {})
        spec_type = spec_details.get("Type") or spec_details.get("PrimitiveType")
        expected = TYPE_MAPPING.get(spec_type)
        if expected and not isinstance(value, expected):
            raise TypeError(
                f"Property '{name}' should be of type {spec_type}"
            )

