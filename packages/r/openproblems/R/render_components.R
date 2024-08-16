# path <- "src/datasets/api/comp_processor_knn.yaml"
#' Render component section
#'
#' @param spec file spec

#' @return string
#' 
#' @export
#' @examples
#' \dontrun{
#' render_component(spec)
#' }

render_component <- function(spec) {
  if (is.character(spec)) {
    spec <- read_comp_spec(spec)
  }

  strip_margin(glue::glue("
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