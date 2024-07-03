def find_project_root(path: str) -> str | None:
    """
    Find the root of a Viash project

    This function will recursively search for a `_viash.yaml` file
    in the parent directories of the given path.

    Args:
        path (str): Path to a file or directory

    Returns:
        str: The path to the root of the Viash project, or None if not found
    """

    import os

    path = os.path.normpath(path)
    check = os.path.join(os.path.dirname(path), "_viash.yaml")
    if os.path.exists(check):
        return os.path.dirname(check)
    elif check == "//_viash.yaml":
        return None
    else:
        return find_project_root(os.path.dirname(check))
