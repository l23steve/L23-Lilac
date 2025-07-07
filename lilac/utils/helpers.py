def helper() -> bool:
    """Utility helper placeholder."""
    return True


def sanitize_filename(name: str) -> str:
    """Return ``name`` converted to a bash-safe filename."""
    safe = name.replace("/", "_").replace(" ", "_")
    return safe
