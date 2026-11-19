requireNamespace("anndataR")
library(testthat)

## VIASH START
meta <- list(
  temp_dir = tempfile()
)
dir.create(meta$temp_dir)
## VIASH END

obs <- data.frame(
  cell_type = factor(rep(c("A", "B"), each = 5)),
  row.names = paste0("cell_", 1:10)
)
var <- data.frame(row.names = paste0("gene_", 1:10))
X <- matrix(rnorm(100), nrow = 10, dimnames = list(rownames(obs), rownames(var)))

test_that("anndataR reads and writes h5ad", {
  h5ad_path <- file.path(meta$temp_dir, "test.h5ad")
  adata1 <- anndataR::AnnData(X = X, obs = obs)
  anndataR::write_h5ad(adata1, h5ad_path)

  adata2 <- anndataR::read_h5ad(h5ad_path)
  expect_equal(adata2$obs, obs)
  expect_equal(adata2$X, X)
})

write_zarr_with_python <- function(path, shard) {
  main <- reticulate::import_main(convert = FALSE)
  main$args <- reticulate::r_to_py(list(X = X, obs = obs, var = var, path = path, shard = shard))
  reticulate::py_run_string(paste0(
    "import anndata\n",
    "anndata.settings.auto_shard_zarr_v3 = args['shard']\n",
    "anndata.AnnData(X=args['X'], obs=args['obs'], var=args['var']).write_zarr(args['path'])"
  ))
}

test_that("anndataR reads zarr v3 written by python anndata", {
  zarr_path <- file.path(meta$temp_dir, "test.zarr")
  write_zarr_with_python(zarr_path, shard = FALSE)

  adata <- anndataR::read_zarr(zarr_path)
  expect_equal(adata$obs, obs)
  expect_equal(adata$X, X)
})

test_that("anndataR reads sharded zarr v3 written by python anndata", {
  skip("Rarr does not support the sharding_indexed codec yet")
  zarr_path <- file.path(meta$temp_dir, "test_sharded.zarr")
  write_zarr_with_python(zarr_path, shard = TRUE)

  adata <- anndataR::read_zarr(zarr_path)
  expect_equal(adata$obs, obs)
  expect_equal(adata$X, X)
})
