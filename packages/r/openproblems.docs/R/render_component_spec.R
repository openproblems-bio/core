# path <- "src/datasets/api/comp_processor_knn.yaml"
#' Render component section
#'
#' @param spec file spec
#' @return string
#'
#' @export
#' @examples
#' path <- system.file("extdata", "example_project", "api", "comp_method.yaml", package = "openproblems.docs")
#'
#' render_component_spec(path)
render_component_spec <- function(spec) {
  if (is.character(spec)) {
    spec <- read_component_spec(spec)
  }

  openproblems::strip_margin(glue::glue("
    |## Component type: {spec$info$label}
    |
    |Path: [`src/{spec$info$namespace}`](https://github.com/openproblems-bio/openproblems-v2/tree/main/src/{spec$info$namespace})
    |
    |{spec$info$summary}
    |
    |Arguments:
    |
    |:::{{.small}}
    |{paste(format_comp_args_as_tibble(spec), collapse = '\n')}
    |:::
    |
    |"), symbol = "\\|")
}
