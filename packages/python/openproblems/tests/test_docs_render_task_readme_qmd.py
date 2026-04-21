import os
import pytest

EXAMPLE_PROJECT = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "data/example_project",
    )
)


@pytest.fixture(scope="module")
def task_metadata():
    from openproblems.project.docs import read_task_metadata

    return read_task_metadata(EXAMPLE_PROJECT)


def test_read_task_metadata_keys(task_metadata):
    for key in (
        "proj_path",
        "proj_conf",
        "files",
        "comps",
        "task_graph",
        "task_graph_order",
    ):
        assert key in task_metadata


def test_read_task_metadata_graph_nodes(task_metadata):
    G = task_metadata["task_graph"]
    assert "comp_method" in G.nodes
    assert "comp_metric" in G.nodes
    assert "file_train" in G.nodes
    assert "file_prediction" in G.nodes


def test_read_task_metadata_graph_edges(task_metadata):
    G = task_metadata["task_graph"]
    # file -> comp (input)
    assert G.has_edge("file_train", "comp_method")
    # comp -> file (output)
    assert G.has_edge("comp_method", "file_prediction")


def test_render_task_readme_qmd_structure(task_metadata):
    from openproblems.project import render_task_readme_qmd

    result = render_task_readme_qmd(task_metadata)

    assert '---\ntitle: "Template"\nformat: gfm\n---' in result
    assert "## Description" in result
    assert "## Authors & contributors" in result
    assert "## API" in result
    assert "```mermaid" in result
    assert "flowchart TB" in result
    assert "```" in result


def test_render_task_readme_qmd_components(task_metadata):
    from openproblems.project import render_task_readme_qmd

    result = render_task_readme_qmd(task_metadata)

    assert "## Component type: Method" in result
    assert "## Component type: Metric" in result


def test_render_task_readme_qmd_file_formats(task_metadata):
    from openproblems.project import render_task_readme_qmd

    result = render_task_readme_qmd(task_metadata)

    assert "## File format: Training data" in result
    assert "## File format: Predicted data" in result


def test_render_task_readme_qmd_instructions(task_metadata):
    from openproblems.project import render_task_readme_qmd

    without = render_task_readme_qmd(task_metadata, add_instructions=False)
    with_inst = render_task_readme_qmd(task_metadata, add_instructions=True)

    assert "### Installation" not in without
    assert "### Installation" in with_inst


def test_render_task_readme_qmd_from_path():
    from openproblems.project import render_task_readme_qmd

    result = render_task_readme_qmd(EXAMPLE_PROJECT)
    assert "## API" in result
