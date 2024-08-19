test_that("render_json_schema_example works", {
  path <- system.file("extdata", "example_schema.json", package = "openproblems.docs")
  schema <- openproblems::read_nested_yaml(path)
  out <- render_json_schema_example(schema)
  expect_type(out, "character")
})