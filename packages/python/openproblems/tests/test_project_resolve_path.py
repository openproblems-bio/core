import pytest
from openproblems.project.resolve_path import resolve_path

PROJECT = "/path/to/project"
PARENT = "/path/to/project/src/api"


def test_resolve_path_relative_to_parent():
    assert resolve_path("file.yaml", PROJECT, PARENT) == PARENT + "/file.yaml"
    assert resolve_path("./file.yaml", PROJECT, PARENT) == PARENT + "/file.yaml"
    assert (
        resolve_path("../file.yaml", PROJECT, PARENT)
        == "/path/to/project/src/file.yaml"
    )


def test_resolve_path_absolute_is_relative_to_project():
    # a leading slash means "relative to the _viash.yaml", not to the filesystem
    assert (
        resolve_path("/src/api/file_dataset.yaml", PROJECT, PARENT)
        == PROJECT + "/src/api/file_dataset.yaml"
    )


def test_resolve_path_absolute_without_project_root():
    with pytest.raises(ValueError, match="no project root"):
        resolve_path("/src/api/file_dataset.yaml", None, PARENT)
