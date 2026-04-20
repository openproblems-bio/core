from __future__ import annotations
import re


def render_component_spec(spec: dict | str) -> str:
    """Render a component spec as a Quarto/GFM markdown section.

    Args:
        spec: Either a ``comp_*.yaml`` path or a dict returned by
            :func:`read_component_spec`.

    Returns:
        A markdown string with an ``## Component type:`` heading, summary, and
        an arguments table.
    """
    if isinstance(spec, str):
        from .read_component_spec import read_component_spec

        spec = read_component_spec(spec)

    info = spec["info"]
    args_table = _format_arguments(spec["args"])

    lines = [
        f"## Component type: {info.get('label', '')}",
        "",
        info.get("summary", "") or "",
        "",
        "Arguments:",
        "",
        ":::{.small}",
        args_table,
        ":::",
        "",
    ]
    return "\n".join(lines)


def _format_arguments(args: list[dict]) -> str:
    from ._markdown import format_markdown_table

    file_args = [a for a in args if a.get("type") == "file"]
    if not file_args:
        return ""

    rows = []
    for arg in file_args:
        tags = []
        if not arg.get("required", True):
            tags.append("Optional")
        if arg.get("direction") == "output":
            tags.append("Output")
        tag_str = f"(_{', '.join(tags)}_) " if tags else ""

        summary = re.sub(r" *\n *", " ", (arg.get("summary") or "").strip()).rstrip(".")
        default = arg.get("default")
        default_str = f" Default: `{default}`." if default is not None else ""

        rows.append(
            [
                f"`--{arg['arg_name']}`",
                f"`{arg.get('type', '')}`",
                f"{tag_str}{summary}.{default_str}",
            ]
        )

    return format_markdown_table(
        ["Name", "Type", "Description"], rows, col_widths=[25, 8, 60]
    )
