#' Read project config
#'
#' @param path Path to a project config file
#'
#' @section Deprecated:
#' Superseded by `openproblems.project.docs.read_task_config()` in the Python
#' `openproblems` package, which is what `create_task_readme` runs.
#'
#' @importFrom cli cli_inform
#' @importFrom openproblems.utils validate_object
#'
#' @export
#'
#' @examples
#' path <- system.file(
#'   "extdata", "example_project", "_viash.yaml",
#'   package = "openproblems.docs"
#' )
#'
#' read_task_config(path)
read_task_config <- function(path) {
  .deprecate_docs("read_task_config")

  proj_conf <- openproblems::read_nested_yaml(path)

  tryCatch(
    {
      validate_object(proj_conf, obj_source = path, what = "task_config")
    },
    error = function(e) {
      cli::cli_warn(paste0("Project config validation failed: ", e$message))
    }
  )

  proj_conf
}
