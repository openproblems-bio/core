def format_markdown_table(headers, rows, col_widths=None):
    """Format a GitHub-Flavored Markdown pipe table.

    Args:
        headers: Column header names.
        rows: List of rows, each a list of cell values.
        col_widths: Optional list of exact dash-counts for the separator row
            (matches R's ``align_kable_widths`` behaviour).

    Returns:
        A GFM pipe table string, or an empty string when ``rows`` is empty.
    """
    if not rows:
        return ""

    header_line = "| " + " | ".join(str(h) for h in headers) + " |"

    if col_widths is not None:
        sep_line = "|" + "".join(f":{'-' * w}|" for w in col_widths)
    else:
        sep_line = (
            "| " + " | ".join(f":{'-' * max(len(str(h)), 3)}" for h in headers) + " |"
        )

    data_lines = ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]

    return "\n".join([header_line, sep_line] + data_lines)
