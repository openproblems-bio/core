def read_task_config(path):
    """Read and return a task config (_viash.yaml) file.

    Args:
        path: Path to a ``_viash.yaml`` project config file.

    Returns:
        The parsed config as a dict.
    """
    from .. import read_nested_yaml
    return read_nested_yaml(path)
