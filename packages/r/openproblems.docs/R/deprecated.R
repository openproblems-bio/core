#' Warn that a documentation helper is deprecated
#'
#' The README rendering pipeline (`common/scripts/create_task_readme`) runs the
#' Python implementation, so this package is no longer the source of truth.
#'
#' @param what Name of the deprecated function
#' @param replacement Name of the Python function that supersedes it, or `NULL`
#'   if there is none
#'
#' @noRd
.deprecate_docs <- function(what, replacement = what) {
  advice <-
    if (is.null(replacement)) {
      "It has no replacement in the Python `openproblems` package."
    } else {
      paste0("Use `openproblems.project.docs.", replacement, "()` from the Python `openproblems` package instead.")
    }

  rlang::warn(
    c(
      paste0("`", what, "()` is deprecated and will be removed in a future release."),
      i = advice
    ),
    class = "deprecatedWarning",
    .frequency = "once",
    .frequency_id = paste0("openproblems.docs::", what)
  )
}
