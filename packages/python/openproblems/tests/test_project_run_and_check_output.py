import pytest

from openproblems.project.component_tests.run_and_check_output import (
    check_format,
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


@pytest.fixture
def mudata_store(tmp_path):
    ad = pytest.importorskip("anndata")
    md = pytest.importorskip("mudata")
    np = pytest.importorskip("numpy")

    counts = np.ones((3, 2), dtype=np.int32)
    rna = ad.AnnData(layers={"counts": counts}, shape=counts.shape)
    prot = ad.AnnData(layers={"counts": counts}, shape=counts.shape)
    mdata = md.MuData({"rna": rna, "prot": prot})
    mdata.obs["cell_type"] = ["a", "b", "c"]
    mdata.uns["dataset_id"] = "test"
    path = tmp_path / "dataset.mudata.zarr"
    mdata.write_zarr(path)
    return str(path)


def _mudata_arg(path, **format_spec):
    fmt = {
        "type": "mudata_zarr",
        "obs": [{"name": "cell_type"}],
        "uns": [{"name": "dataset_id"}],
        "mod": {
            "rna": {"layers": [{"name": "counts"}]},
            "prot": {"required": False, "layers": [{"name": "counts"}]},
            "atac": {"required": False, "layers": [{"name": "counts"}]},
        },
    }
    fmt.update(format_spec)
    return _arg(value=path, info={"format": fmt})


def test_check_format_mudata_passes(mudata_store):
    check_format(_mudata_arg(mudata_store))


def test_check_format_mudata_missing_required_modality(mudata_store):
    arg = _mudata_arg(mudata_store, mod={"atac": {"layers": [{"name": "counts"}]}})
    with pytest.raises(AssertionError, match=r"missing modality \.mod\['atac'\]"):
        check_format(arg)


def test_check_format_mudata_missing_global_obs(mudata_store):
    arg = _mudata_arg(mudata_store, obs=[{"name": "batch"}])
    with pytest.raises(AssertionError, match=r"missing slot \.obs\['batch'\]"):
        check_format(arg)


def test_check_format_mudata_missing_modality_slot(mudata_store):
    arg = _mudata_arg(mudata_store, mod={"rna": {"layers": [{"name": "normalized"}]}})
    with pytest.raises(
        AssertionError,
        match=r"\.mod\['rna'\] is missing slot \.layers\['normalized'\]",
    ):
        check_format(arg)


@pytest.fixture
def spatialdata_store(tmp_path):
    ad = pytest.importorskip("anndata")
    np = pytest.importorskip("numpy")
    sd = pytest.importorskip("spatialdata")

    counts = np.ones((3, 2), dtype=np.int32)
    table = ad.AnnData(layers={"counts": counts}, shape=counts.shape)
    spots = sd.models.ShapesModel.parse(np.zeros((3, 2)), geometry=0, radius=np.ones(3))
    sdata = sd.SpatialData(
        shapes={"spots": spots},
        tables={"table": sd.models.TableModel.parse(table)},
        attrs={"dataset_id": "test"},
    )
    path = tmp_path / "dataset.spatialdata.zarr"
    sdata.write(path)
    return str(path)


def _spatialdata_arg(path, **format_spec):
    fmt = {
        "type": "spatialdata_zarr",
        "attrs": [{"name": "dataset_id"}],
        "coordinate_systems": [{"name": "global"}],
        "shapes": [{"name": "spots"}],
        "tables": [{"name": "table", "layers": [{"name": "counts"}]}],
    }
    fmt.update(format_spec)
    return _arg(value=path, info={"format": fmt})


def test_check_format_spatialdata_passes(spatialdata_store):
    check_format(_spatialdata_arg(spatialdata_store))


def test_check_format_spatialdata_missing_attr(spatialdata_store):
    arg = _spatialdata_arg(spatialdata_store, attrs=[{"name": "dataset_name"}])
    with pytest.raises(AssertionError, match=r"missing attrs\['dataset_name'\]"):
        check_format(arg)


def test_check_format_spatialdata_missing_coordinate_system(spatialdata_store):
    arg = _spatialdata_arg(spatialdata_store, coordinate_systems=[{"name": "aligned"}])
    with pytest.raises(AssertionError, match="missing coordinate system 'aligned'"):
        check_format(arg)


def test_check_format_spatialdata_optional_absent(spatialdata_store):
    arg = _spatialdata_arg(
        spatialdata_store,
        attrs=[{"name": "dataset_id"}, {"name": "dataset_url", "required": False}],
        images=[{"name": "he_image", "required": False}],
    )
    check_format(arg)
