from __future__ import annotations


def resolve_path(path: str, project_path: str | None, parent_path: str) -> str:
    """
    Resolve a path relative to a parent path or project path

    This function will resolve a path to an absolute path. If
    the path is relative, it will be resolved relative to the
    parent path. If the path is absolute, it will be resolved
    relative to the project path.

    Args:
        path (str): The path to resolve
        project_path (str): The path to the root of the Viash project
        parent_path (str): The path to the parent directory

    Returns:
        str: The resolved path

    Example:

      ```python
      project_path <- "/path/to/project"
      parent_path <- "/path/to/project/subdir"

      resolve_path("./file.yaml", project_path, parent_path)
      # "/path/to/project/subdir/file.yaml"

      resolve_path("/file.yaml", project_path, parent_path)
      # "/path/to/project/file.yaml"
      ```
    """

    import os

    if path.startswith("/"):
        if project_path is None:
            raise ValueError(
                f"Cannot resolve '{path}' relative to the project root: "
                "no project root (_viash.yaml) was found"
            )
        # note: os.path.join() discards project_path if path starts with a "/"
        return os.path.abspath(os.path.join(project_path, path.lstrip("/")))
    else:
        return os.path.abspath(os.path.join(parent_path, path))
