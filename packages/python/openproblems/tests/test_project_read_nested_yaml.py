import os
import yaml
from openproblems.project import read_nested_yaml

EXAMPLE_PROJECT = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "data/example_project",
    )
)


def test_read_nested_yaml_preserves_key_order():
    # the rendered README lists author info in the order the keys appear in
    # the yaml, so the merge must not reshuffle them
    path = os.path.join(EXAMPLE_PROJECT, "_viash.yaml")
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    conf = read_nested_yaml(path)

    assert list(conf.keys()) == list(raw.keys())
    for i, author in enumerate(conf["authors"]):
        assert list(author["info"].keys()) == list(raw["authors"][i]["info"].keys())


def test_read_nested_yaml_resolves_merges():
    path = os.path.join(EXAMPLE_PROJECT, "api", "comp_method.yaml")
    conf = read_nested_yaml(path)

    train_arg = next(arg for arg in conf["arguments"] if arg["name"] == "--input_train")
    # pulled in from file_train.yaml
    assert train_arg["type"] == "file"
    assert train_arg["label"] == "Training data"
