#' Read project config
#'
#' @param file Path to a project config file
#'
#' @importFrom cli cli_inform
#'
#' @export
#'
#' @examples
#' file <- system.file("extdata", "example_project", "_viash.yaml", package = "openproblems.docs")
#'
#' read_project_config(file)
read_project_config <- function(file) {
  project_config <- openproblems::read_nested_yaml(file)

  # ...?

  project_config
}
