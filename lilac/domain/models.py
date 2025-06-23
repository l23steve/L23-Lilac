from dataclasses import dataclass, field
from typing import Any


class BaseModel:
    """Domain model placeholder."""

    pass


@dataclass(slots=True)
class Resource(BaseModel):
    """Domain representation of a configuration resource."""

    resource_type: str
    namespace: str
    depends_on: list[str] = field(default_factory=list)
    properties: dict[str, Any] = field(default_factory=dict)
    ignore: bool = False

    @property
    def type(self) -> str:
        """Return the deprecated ``type`` field for backwards compatibility."""
        return self.resource_type

