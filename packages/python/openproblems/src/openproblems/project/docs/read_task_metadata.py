from __future__ import annotations
import glob
import os
import re
import warnings
from collections import deque


def read_task_metadata(path: str) -> dict:
    """Read all API files in a task directory and return structured metadata.

    Scans ``path`` recursively for ``comp_*.yaml`` and ``file_*.yaml`` files,
    builds a directed task graph, and runs a BFS to determine render order.

    Args:
        path: Path to the task directory (or ``api/`` subdirectory).  A
            ``_viash.yaml`` must exist somewhere above this path.

    Returns:
        A dict with the following keys:

        * ``proj_path`` – path to the project root
        * ``proj_conf`` – parsed ``_viash.yaml``
        * ``files`` / ``comps`` – dicts keyed by ``file_name``
        * ``file_info`` / ``comp_info`` – flat lists of info dicts
        * ``file_expected_format`` / ``comp_args`` – flat lists
        * ``task_graph`` – ``networkx.DiGraph``
        * ``task_graph_root`` – name of the root node
        * ``task_graph_order`` – BFS-ordered list of node names
    """
    from .. import find_project_root
    from .read_task_config import read_task_config
    from .read_component_spec import read_component_spec
    from .read_file_format import read_file_format

    project_path = find_project_root(path)
    if project_path is None:
        raise ValueError(f"No project root (_viash.yaml) found from '{path}'")

    proj_conf_file = os.path.join(project_path, "_viash.yaml")
    if not os.path.exists(proj_conf_file):
        raise ValueError(f"No _viash.yaml found in project root '{project_path}'")

    proj_conf = read_task_config(proj_conf_file)

    comp_paths = sorted(
        glob.glob(os.path.join(path, "**/comp_*.yaml"), recursive=True)
        + glob.glob(os.path.join(path, "**/comp_*.yml"), recursive=True)
    )
    comps = {
        re.sub(r"\.ya?ml$", "", os.path.basename(p)): read_component_spec(p)
        for p in comp_paths
    }

    file_paths = sorted(
        glob.glob(os.path.join(path, "**/file_*.yaml"), recursive=True)
        + glob.glob(os.path.join(path, "**/file_*.yml"), recursive=True)
    )
    files = {
        re.sub(r"\.ya?ml$", "", os.path.basename(p)): read_file_format(p)
        for p in file_paths
    }

    task_graph = _build_graph(files, comps)
    task_graph_root = _get_root(task_graph)
    task_graph_order = _bfs_order(task_graph, task_graph_root)

    comp_info = [c["info"] for c in comps.values()]
    comp_args = [arg for c in comps.values() for arg in c["args"]]
    file_info = [f["info"] for f in files.values()]
    file_expected_format = [
        row for f in files.values() for row in (f.get("expected_format") or [])
    ]

    return {
        "proj_path": project_path,
        "proj_conf": proj_conf,
        "files": files,
        "file_info": file_info,
        "file_expected_format": file_expected_format,
        "comps": comps,
        "comp_info": comp_info,
        "comp_args": comp_args,
        "task_graph": task_graph,
        "task_graph_root": task_graph_root,
        "task_graph_order": task_graph_order,
    }


def _build_graph(files: dict, comps: dict):
    import networkx as nx

    G = nx.DiGraph()

    for name, f in files.items():
        G.add_node(name, label=f["info"].get("label") or name, is_comp=False)

    for name, c in comps.items():
        G.add_node(name, label=c["info"].get("label") or name, is_comp=True)

    for comp_name, c in comps.items():
        for arg in c["args"]:
            if arg.get("type") != "file" or not arg.get("parent"):
                continue
            parent = arg["parent"]
            if parent not in G:
                continue
            required = bool(arg.get("required", False))
            if arg.get("direction") == "input":
                G.add_edge(parent, comp_name, from_to="file_to_comp", required=required)
            elif arg.get("direction") == "output":
                G.add_edge(comp_name, parent, from_to="comp_to_file", required=required)

    return G


def _get_root(G) -> str:
    roots = [n for n, d in G.in_degree() if d == 0]
    if not roots:
        return next(iter(G.nodes()))
    if len(roots) > 1:
        warnings.warn(
            f"Multiple root nodes with in-degree 0: {roots}. Using first.",
            stacklevel=4,
        )
    return roots[0]


def _bfs_order(G, root: str) -> list[str]:
    """BFS from root; unreachable nodes are appended afterwards (mirrors igraph)."""
    visited: list[str] = []
    seen: set[str] = set()
    queue: deque[str] = deque([root])
    while queue:
        node = queue.popleft()
        if node not in seen:
            seen.add(node)
            visited.append(node)
            for nbr in G.successors(node):
                if nbr not in seen:
                    queue.append(nbr)
    for node in G.nodes():
        if node not in seen:
            visited.append(node)
    return visited
