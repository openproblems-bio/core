
test_that("find_project_root works", {
  # create a temporary directory with a _viash.yaml file
  # test_find_project_root/
  # ├── src/
  # |   ├── config.vsh.yaml
  # |   └── script.R
  # └── _viash.yaml

  temp_dir <- as.character(fs::path_temp())

  # remove on test end
  on.exit(fs::dir_delete(temp_dir))

  fs::dir_create(fs::path(temp_dir, "src"))
  fs::file_create(fs::path(temp_dir, "_viash.yaml"))
  fs::file_create(fs::path(temp_dir, "src", "config.vsh.yaml"))
  fs::file_create(fs::path(temp_dir, "src", "script.R"))

  expect_equal(
    find_project_root(fs::path(temp_dir, "src", "config.vsh.yaml")),
    temp_dir
  )
  expect_equal(
    find_project_root(fs::path(temp_dir, "src", "script.R")),
    temp_dir
  )
  expect_equal(
    find_project_root(fs::path(temp_dir, "_viash.yaml")),
    temp_dir
  )
})