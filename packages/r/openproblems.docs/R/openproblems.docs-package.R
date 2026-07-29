#' @keywords internal
#'
#' @section Deprecated:
#' This package is deprecated and will be removed in a future release. The
#' README rendering pipeline (`common/scripts/create_task_readme`) runs the
#' Python `openproblems` package, so `openproblems.project.docs` is the source
#' of truth for task documentation.
"_PACKAGE"

## usethis namespace: start
#' @importFrom dplyr bind_rows select mutate everything filter transmute group_by summarise arrange case_when
#' @importFrom purrr map_dfr map2_chr map_chr map
#' @importFrom rlang .data %|% %||%
#' @importFrom stats na.omit
#' @importFrom tibble as_tibble rownames_to_column
#' @importFrom stringr str_replace_all
#' @importFrom glue glue
#' @importFrom openproblems.utils strip_margin validate_object
## usethis namespace: end
NULL
