from __future__ import annotations
import re

ANNDATA_STRUCT_NAMES = [
    "X",
    "obs",
    "var",
    "obsm",
    "obsp",
    "varm",
    "varp",
    "layers",
    "uns",
]
SPATIALDATA_ELEMENT_CATEGORIES = [
    "images",
    "labels",
    "points",
    "shapes",
    "tables",
    "coordinate_systems",
]


def render_file_format(spec: dict | str) -> str:
    """Render a file format spec as a Quarto/GFM markdown section.

    Args:
        spec: Either a ``file_*.yaml`` path or a dict returned by
            :func:`read_file_format`.

    Returns:
        A markdown string with a ``## File format:`` heading, summary,
        example path, description, and a format/data-structure table.
    """
    if isinstance(spec, str):
        from .read_file_format import read_file_format

        spec = read_file_format(spec)

    info = spec["info"]
    label = info.get("label") or ""
    summary = (info.get("summary") or "").strip()
    description = (info.get("description") or "").strip()
    example = info.get("example")

    example_str = f"Example file: `{example}`" if example else ""
    description_str = f"Description:\n\n{description}" if description else ""

    expected_format = spec.get("expected_format")
    expected_format_str = ""
    if expected_format:
        format_example_lines = _render_format_example(spec)
        format_table_lines = _render_format_table(spec)
        expected_format_str = "\n".join(
            [
                "Format:",
                "",
                ":::{.small}",
                *format_example_lines,
                ":::",
                "",
                "Data structure:",
                "",
                ":::{.small}",
                *format_table_lines,
                ":::",
            ]
        )

    parts = [
        f"## File format: {label}",
        "",
        summary,
        "",
        example_str,
        "",
        description_str,
        "",
        expected_format_str,
    ]

    # Trim trailing blank lines, keep one trailing newline
    while parts and parts[-1] == "":
        parts.pop()
    return "\n".join(parts) + "\n"


def _render_format_example(spec: dict) -> list[str]:
    fmt_type = spec["info"].get("file_type")
    expected_format = spec.get("expected_format") or []

    if fmt_type in ("h5ad", "anndata_hdf5", "anndata_zarr"):
        structs: dict[str, list[str]] = {}
        for row in expected_format:
            structs.setdefault(row["struct"], []).append(f"'{row['name']}'")
        lines = ["    AnnData object"]
        for struct_name in ANNDATA_STRUCT_NAMES:
            if struct_name in structs:
                lines.append(f"     {struct_name}: {', '.join(structs[struct_name])}")
        return lines

    if fmt_type in ("csv", "tsv", "parquet"):
        names = ", ".join(f"'{row['name']}'" for row in expected_format)
        return ["    Tabular data", f"     {names}"]

    if fmt_type in ("json", "yaml"):
        names = ", ".join(f"'{row['name']}'" for row in expected_format)
        ext = fmt_type.upper()
        return [f"    {ext} object", f"     {names}"]

    if fmt_type == "spatialdata_zarr":
        by_category: dict[str, list[str]] = {}
        for row in expected_format:
            by_category.setdefault(row["category"], []).append(f"'{row['name']}'")
        lines = ["    SpatialData object"]
        for cat in SPATIALDATA_ELEMENT_CATEGORIES:
            if cat in by_category:
                lines.append(f"     {cat}: {', '.join(by_category[cat])}")
        return lines

    return [""]


def _render_format_table(spec: dict) -> list[str]:
    from ._markdown import format_markdown_table

    fmt_type = spec["info"].get("file_type")
    expected_format = spec.get("expected_format") or []

    def _tag_str(row: dict) -> str:
        tags = []
        if not row.get("required", True):
            tags.append("Optional")
        return f"(_{', '.join(tags)}_) " if tags else ""

    def _clean_desc(row: dict) -> str:
        desc = re.sub(r" *\n *", " ", (row.get("description") or "").strip()).rstrip(
            "."
        )
        return desc

    if fmt_type in ("h5ad", "anndata_hdf5", "anndata_zarr"):
        rows = [
            [
                f'`{row["struct"]}["{row["name"]}"]`',
                f'`{row.get("type", "")}`',
                f"{_tag_str(row)}{_clean_desc(row)}.",
            ]
            for row in expected_format
        ]
        return [
            format_markdown_table(
                ["Slot", "Type", "Description"], rows, col_widths=[25, 8, 60]
            )
        ]

    if fmt_type in ("csv", "tsv", "parquet"):
        rows = [
            [
                f'`{row["name"]}`',
                f'`{row.get("type", "")}`',
                f"{_tag_str(row)}{_clean_desc(row)}.",
            ]
            for row in expected_format
        ]
        return [
            format_markdown_table(
                ["Column", "Type", "Description"], rows, col_widths=[25, 8, 60]
            )
        ]

    if fmt_type in ("json", "yaml"):
        rows = [
            [
                f'`{row["name"]}`',
                f'`{row.get("type", "")}`',
                f"{_tag_str(row)}{_clean_desc(row)}.",
            ]
            for row in expected_format
        ]
        return [
            format_markdown_table(
                ["Key", "Type", "Description"], rows, col_widths=[25, 8, 60]
            )
        ]

    if fmt_type == "spatialdata_zarr":
        lines = []
        by_category: dict[str, list[dict]] = {}
        for row in expected_format:
            by_category.setdefault(row["category"], []).append(row)

        for cat in SPATIALDATA_ELEMENT_CATEGORIES:
            elements = by_category.get(cat)
            if not elements:
                continue
            lines.append(f"*{cat}*")
            lines.append("")

            if cat in ("images", "labels", "coordinate_systems"):
                elem_rows = [
                    [f'`{e["name"]}`', f"{_tag_str(e)}{_clean_desc(e)}."]
                    for e in elements
                ]
                lines.append(
                    format_markdown_table(
                        ["Name", "Description"], elem_rows, col_widths=[25, 68]
                    )
                )

            elif cat in ("points", "shapes"):
                for elem in elements:
                    lines.append(f"`{elem['name']}`: {_clean_desc(elem)}.")
                    lines.append("")
                    col_rows = [
                        [
                            f'`{c["name"]}`',
                            f'`{c.get("type", "")}`',
                            f"{_tag_str(c)}{_clean_desc(c)}.",
                        ]
                        for c in (elem.get("columns") or [])
                    ]
                    if col_rows:
                        lines.append(
                            format_markdown_table(
                                ["Column", "Type", "Description"],
                                col_rows,
                                col_widths=[25, 8, 60],
                            )
                        )

            elif cat == "tables":
                for elem in elements:
                    lines.append(f"`{elem['name']}`: {_clean_desc(elem)}.")
                    lines.append("")
                    slot_rows = [
                        [
                            f'`{s["struct"]}["{s["name"]}"]`',
                            f'`{s.get("type", "")}`',
                            f"{_tag_str(s)}{_clean_desc(s)}.",
                        ]
                        for s in (elem.get("anndata_slots") or [])
                    ]
                    if slot_rows:
                        lines.append(
                            format_markdown_table(
                                ["Slot", "Type", "Description"],
                                slot_rows,
                                col_widths=[25, 8, 60],
                            )
                        )

            lines.append("")

        # remove trailing blank line
        while lines and lines[-1] == "":
            lines.pop()
        return lines

    return [""]
