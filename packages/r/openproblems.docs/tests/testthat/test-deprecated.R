test_that(".deprecate_docs points at the Python replacement", {
  # a name unused elsewhere, so the once-per-session cache does not swallow it
  expect_warning(
    .deprecate_docs("a_superseded_function"),
    class = "deprecatedWarning"
  )
})

test_that(".deprecate_docs handles a missing replacement", {
  expect_warning(
    .deprecate_docs("a_function_without_replacement", replacement = NULL),
    "no replacement"
  )
})
