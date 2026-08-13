from typing import Any


def deep_merge(obj1: Any, obj2: Any) -> Any:
    """Recursively merge two dictionaries or lists.

    Args:
        obj1 (any): The first dictionary or list.
        obj2 (any): The second dictionary or list.

    Keys keep the order of `obj1`, followed by the keys only found in `obj2`.

    Returns:
        dict: The merged dictionary.
    """
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        keys = list(obj1.keys()) + [k for k in obj2 if k not in obj1]
        out = {}
        for key in keys:
            if key in obj1:
                if key in obj2:
                    out[key] = deep_merge(obj1[key], obj2[key])
                else:
                    out[key] = obj1[key]
            else:
                out[key] = obj2[key]
        return out
    elif isinstance(obj1, list) and isinstance(obj2, list):
        return obj1 + obj2
    else:
        return obj2
