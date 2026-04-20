from __future__ import annotations
import os
import re

ANNDATA_STRUCT_NAMES = ["X", "obs", "var", "obsm", "obsp", "varm", "varp", "layers", "uns"]
SPATIALDATA_ELEMENT_CATEGORIES = ["images", "labels", "points", "shapes", "tables", "coordinate_systems"]


def read_file_format(path: str) -> dict:
    """Read a file format spec from a ``file_*.yaml`` file.

    Args:
        path: Path to a file format yaml (usually ``src/api/file_*.yaml``).

    Returns:
        A dict with key ``info`` (dict) and optionally ``expected_format``
        (list of dicts) when the format type is known.
    """
    from .. import read_nested_yaml
    data = read_nested_yaml(path)

    out: dict = {"info": _process_info(data, path)}

    fmt = (data.get("info") or {}).get("format") or {}
    format_type = fmt.get("type")

    if format_type == "h5ad":
        out["expected_format"] = _process_h5ad(data, path, format_type)
    elif format_type in ("anndata_hdf5", "anndata_zarr"):
        out["expected_format"] = _process_h5ad(data, path, format_type)
    elif format_type in ("tabular", "csv", "tsv", "parquet"):
        out["expected_format"] = _process_tabular(data, path, format_type)
    elif format_type in ("json", "yaml"):
        out["expected_format"] = _process_keyed(data, path, format_type)
    elif format_type == "spatialdata_zarr":
        out["expected_format"] = _process_spatialdata(data, path)

    return out


def _process_info(data: dict, path: str) -> dict:
    file_name = re.sub(r"\.ya?ml$", "", os.path.basename(path))
    fmt = (data.get("info") or {}).get("format") or {}

    label = data.get("label")
    if label is None:
        example = data.get("example")
        if example:
            label = os.path.basename(str(example))

    return {
        "file_name": file_name,
        "file_type": fmt.get("type"),
        "label": label,
        "summary": data.get("summary"),
        "description": data.get("description"),
        "example": data.get("example"),
    }


def _process_h5ad(data: dict, path: str, format_type: str) -> list[dict]:
    file_name = re.sub(r"\.ya?ml$", "", os.path.basename(path))
    fmt = (data.get("info") or {}).get("format") or {}

    rows = []
    for struct_name in ANNDATA_STRUCT_NAMES:
        fields = fmt.get(struct_name)
        if not fields:
            continue
        if not isinstance(fields, list):
            fields = [fields]
        for field in fields:
            rows.append({
                "file_name": file_name,
                "struct": struct_name,
                "name": field.get("name", struct_name),
                "type": field.get("type", ""),
                "required": field.get("required", True),
                "multiple": field.get("multiple", False),
                "description": field.get("description"),
                "summary": field.get("summary"),
                "data_type": format_type,
            })
    return rows


def _process_tabular(data: dict, path: str, format_type: str) -> list[dict]:
    file_name = re.sub(r"\.ya?ml$", "", os.path.basename(path))
    columns = (data.get("info") or {}).get("format", {}).get("columns") or []

    return [
        {
            "file_name": file_name,
            "name": col.get("name", ""),
            "type": col.get("type", ""),
            "required": col.get("required", True),
            "description": col.get("description"),
            "summary": col.get("summary"),
            "data_type": format_type,
        }
        for col in columns
    ]


def _process_keyed(data: dict, path: str, format_type: str) -> list[dict]:
    file_name = re.sub(r"\.ya?ml$", "", os.path.basename(path))
    keys = (data.get("info") or {}).get("format", {}).get("keys") or []

    return [
        {
            "file_name": file_name,
            "name": k.get("name", ""),
            "type": k.get("type", ""),
            "required": k.get("required", True),
            "description": k.get("description"),
            "summary": k.get("summary"),
            "data_type": format_type,
        }
        for k in keys
    ]


def _process_spatialdata(data: dict, path: str) -> list[dict]:
    file_name = re.sub(r"\.ya?ml$", "", os.path.basename(path))
    fmt = (data.get("info") or {}).get("format") or {}
    rows = []
    for category in SPATIALDATA_ELEMENT_CATEGORIES:
        elements = fmt.get(category) or []
        for elem in elements:
            row: dict = {
                "file_name": file_name,
                "category": category,
                "name": elem.get("name", ""),
                "element_type": elem.get("type", ""),
                "required": elem.get("required", True),
                "description": elem.get("description"),
                "data_type": "spatialdata_zarr",
            }
            if category in ("points", "shapes"):
                row["columns"] = [
                    {
                        "name": col.get("name", ""),
                        "type": col.get("type", ""),
                        "required": col.get("required", True),
                        "description": col.get("description"),
                    }
                    for col in (elem.get("columns") or [])
                ]
            elif category == "tables":
                slots = []
                for struct_name in ANNDATA_STRUCT_NAMES:
                    fields = elem.get(struct_name)
                    if not fields:
                        continue
                    if not isinstance(fields, list):
                        fields = [fields]
                    for f in fields:
                        slots.append({
                            "struct": struct_name,
                            "name": f.get("name", struct_name),
                            "type": f.get("type", ""),
                            "required": f.get("required", True),
                            "description": f.get("description"),
                        })
                row["anndata_slots"] = slots
            rows.append(row)
    return rows
