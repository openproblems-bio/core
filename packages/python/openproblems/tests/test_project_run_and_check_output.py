import pytest

from openproblems.project.component_tests.run_and_check_output import (
    check_output_files,
    generate_cmd_args,
    get_argument_sets,
)


def _arg(**kwargs):
    arg = {
        "name": "--output",
        "clean_name": "output",
        "type": "file",
        "direction": "output",
        "required": False,
        "must_exist": True,
        "multiple": False,
        "multiple_sep": ";",
    }
    arg.update(kwargs)
    return arg


def test_check_output_files_skips_arguments_without_a_value():
    # an optional output without a default or example never gets a value, so
    # there is no file to read
    arg = _arg(info={"format": {"type": "h5ad", "obs": [{"name": "label"}]}})
    check_output_files([arg])


def test_check_output_files_requires_required_outputs():
    arg = _arg(required=True, info={})
    with pytest.raises(AssertionError, match="is missing a value"):
        check_output_files([arg])


def test_get_argument_sets_leaves_valueless_arguments_alone():
    config = {
        "argument_groups": [{"name": "Arguments", "arguments": [_arg(info={})]}],
        "all_arguments": [_arg(info={})],
    }
    argument_sets = get_argument_sets(config, "resources")

    assert "value" not in argument_sets["run"][0]
    assert generate_cmd_args(argument_sets["run"]) == []
