import json
from pathlib import Path

import anndata
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import tempfile

## VIASH START
meta = {
    "temp_dir": tempfile.gettempdir(),
}
## VIASH END

# Define the path for the temporary H5AD file
h5ad_path = f"{meta['temp_dir']}/test_anndata.h5ad"

# Create an AnnData object
adata1 = anndata.AnnData(
    X=np.random.randn(10, 10),
    obs=pd.DataFrame(
        {"cell_type": pd.Categorical(np.repeat(["A", "B"], 5))},
        index=[f"cell_{i}" for i in range(10)],
    ),
)

# Write the AnnData object to an H5AD file
adata1.write_h5ad(h5ad_path)

# Read the H5AD file back into a new AnnData object
adata2 = anndata.read_h5ad(h5ad_path)

# Assert that the observational metadata (.obs) is the same
assert_frame_equal(adata1.obs, adata2.obs)

# Write the AnnData object to zarr, which should be zarr v3 with sharded arrays
zarr_path = Path(meta["temp_dir"]) / "test_anndata.zarr"
adata1.write_zarr(zarr_path)
x_meta = json.loads((zarr_path / "X" / "zarr.json").read_text())
assert x_meta["zarr_format"] == 3, f"Expected zarr v3, got {x_meta['zarr_format']}"
codecs = [codec["name"] for codec in x_meta["codecs"]]
assert codecs == ["sharding_indexed"], f"Expected a sharded array, got codecs {codecs}"

adata3 = anndata.read_zarr(zarr_path)
assert_frame_equal(adata1.obs, adata3.obs)
np.testing.assert_array_equal(adata1.X, adata3.X)

print("Test passed!", flush=True)