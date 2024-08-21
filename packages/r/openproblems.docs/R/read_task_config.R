#' Read project config
#'
#' @param file Path to a project config file
#'
#' @importFrom cli cli_inform
#' @importFrom openproblems.utils validate_object
#'
#' @export
#'
#' @examples
#' file <- system.file(
#'   "extdata", "example_project", "_viash.yaml",
#'   package = "openproblems.docs"
#' )
#'
#' read_task_config(file)
read_task_config <- function(file) {
  proj_conf <- openproblems::read_nested_yaml(file)

  tryCatch(
    {
      validate_object(proj_conf, obj_source = file, what = "task_config")
    },
    error = function(e) {
      cli::cli_warn(paste0("Project config validation failed: ", e$message))
    }
  )

  proj_conf
}
