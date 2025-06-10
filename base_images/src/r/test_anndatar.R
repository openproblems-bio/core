requireNamespace("anndata")
requireNamespace("anndataR")
library(testthat)

## VIASH START
meta <- list(
  temp_dir = tempfile()
)
dir.create(meta$temp_dir)
## VIASH END

test_that("anndata and anndataR are both working", {
  h5ad_path <- paste0(meta$temp_dir, "/test.h5ad")

  # Create h5ad using anndata
  adata1 <- anndata::AnnData(
    X = matrix(rnorm(100), nrow = 10),
    obs = data.frame(
      cell_type = factor(rep(c("A", "B"), each = 5))
    )
  )

  adata1$write_h5ad(h5ad_path)

  # Read h5ad using anndataR
  adata2 <- anndataR::read_h5ad(h5ad_path)

  expect_equivalent(adata1$obs, adata2$obs)
})
