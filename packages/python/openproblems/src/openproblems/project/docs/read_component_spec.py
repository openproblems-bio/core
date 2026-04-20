from __future__ import annotations
import os
import re


def read_component_spec(path: str) -> dict:
    """Read a component spec from a ``comp_*.yaml`` file.

    Args:
        path: Path to a component spec yaml (usually ``src/api/comp_*.yaml``).

    Returns:
        A dict with keys ``info`` (dict) and ``args`` (list of dicts).
    """
    from .. import read_nested_yaml

    data = read_nested_yaml(path)
    return {
        "info": _process_info(data, path),
        "args": _process_arguments(data, path),
    }


def _process_info(data: dict, path: str) -> dict:
    file_name = re.sub(r"\.ya?ml$", "", os.path.basename(path))
    info: dict = {"file_name": file_name}

    # Top-level fields
    for key in ("label", "summary", "description", "namespace"):
        info[key] = data.get(key)

    # Merge info block (may override Nones above)
    for key, val in (data.get("info") or {}).items():
        if info.get(key) is None:
            info[key] = val

    # Merge info.type_info
    for key, val in ((data.get("info") or {}).get("type_info") or {}).items():
        if info.get(key) is None:
            info[key] = val

    return info


def _process_arguments(data: dict, path: str) -> list[dict]:
    file_name = re.sub(r"\.ya?ml$", "", os.path.basename(path))

    arguments = list(data.get("arguments") or [])
    for arg_group in data.get("argument_groups") or []:
        arguments.extend(arg_group.get("arguments") or [])

    result = []
    for arg in arguments:
        arg_info = arg.get("info") or {}
        merge_ref = arg.get("__merge__")
        parent = (
            re.sub(r"\.ya?ml$", "", os.path.basename(merge_ref)) if merge_ref else None
        )

        default = arg.get("default")
        example = arg.get("example")
        if isinstance(example, list):
            example = example[0] if example else None

        result.append(
            {
                "file_name": file_name,
                "arg_name": re.sub(r"^-+", "", arg.get("name", "")),
                "type": arg.get("type", ""),
                "direction": arg.get("direction") or "input",
                "required": bool(arg.get("required"))
                if arg.get("required") is not None
                else False,
                "default": str(default) if default is not None else None,
                "example": str(example) if example is not None else None,
                "description": arg.get("description") or arg_info.get("description"),
                "summary": arg.get("summary") or arg_info.get("summary"),
                "parent": parent,
            }
        )

    return result
