def coerce_numeric_fields(d: dict, keys: list[str]) -> dict:
    """Return a copy of d where keys are coerced to int if possible; ignore missing."""
    result = d.copy()
    for key in keys:
        if key in result:
            try:
                result[key] = int(result[key])
            except (ValueError, TypeError):
                pass
    return result
