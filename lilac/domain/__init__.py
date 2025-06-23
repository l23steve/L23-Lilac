"""Domain models for Lilac."""

from .models import BaseModel, Resource
from .validation import validate_against_spec

__all__ = [
    "BaseModel",
    "Resource",
    "validate_against_spec",
]
