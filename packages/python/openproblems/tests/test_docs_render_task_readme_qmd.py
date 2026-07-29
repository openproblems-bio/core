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


def test_task_graph_order_is_topological(task_metadata):
    G = task_metadata["task_graph"]
    order = task_metadata["task_graph_order"]

    assert sorted(order) == sorted(G.nodes)
    for node in order:
        for pred in G.predecessors(node):
            msg = f"{node} is rendered before its input {pred}"
            assert order.index(pred) < order.index(node), msg


def test_task_graph_order_keeps_multiple_roots_up_front():
    import networkx as nx
    from openproblems.project.docs.read_task_metadata import (
        _get_roots,
        _topological_order,
    )

    # a multimodal task: two raw datasets feeding a single processor
    G = nx.DiGraph()
    G.add_edges_from(
        [
            ("file_mod1", "comp_process"),
            ("file_mod2", "comp_process"),
            ("comp_process", "file_train"),
        ]
    )

    roots = _get_roots(G)
    order = _topological_order(G, roots)

    assert roots == ["file_mod1", "file_mod2"]
    assert order == ["file_mod1", "file_mod2", "comp_process", "file_train"]


def test_task_graph_order_includes_cyclic_nodes():
    import networkx as nx
    from openproblems.project.docs.read_task_metadata import (
        _get_roots,
        _topological_order,
    )

    G = nx.DiGraph()
    G.add_edges_from([("a", "b"), ("b", "c"), ("c", "b")])

    order = _topological_order(G, _get_roots(G))

    assert sorted(order) == ["a", "b", "c"]
    assert order[0] == "a"


def test_render_component_spec_non_file_arguments(task_metadata):
    from openproblems.project.docs import render_component_spec

    result = render_component_spec(task_metadata["comps"]["comp_data_processor"])

    # non-file arguments are part of the API too, and describe themselves
    # through `description` rather than the `summary` a __merge__ pulls in
    assert "`--seed`" in result
    assert "The seed for determining the train/test split" in result
    assert "Default: `1`" in result
