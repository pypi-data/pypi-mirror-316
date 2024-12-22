
def flatten(nest: list) -> list:
    """Flatten a nested list."""
    result = []
    for item in nest:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result