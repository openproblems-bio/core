import pytest
from openproblems.project.docs import render_file_format

COLUMNS = [
    {"name": "cell_id", "type": "string", "required": True, "description": "Cell id"},
    {"name": "score", "type": "double", "required": False, "description": "The score"},
]


def _spec(file_type):
    return {
        "info": {
            "file_name": "file_scores",
            "file_type": file_type,
            "label": "Scores",
            "summary": "A table of scores.",
        },
        "expected_format": COLUMNS,
    }


@pytest.mark.parametrize("file_type", ["tabular", "csv", "tsv", "parquet"])
def test_render_file_format_tabular(file_type):
    result = render_file_format(_spec(file_type))

    assert "## File format: Scores" in result
    assert "Tabular data" in result
    assert "'cell_id', 'score'" in result
    assert "| Column | Type | Description |" in result
    assert "`cell_id`" in result
    assert "(_Optional_)" in result
