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

print("Test passed!", flush=True)