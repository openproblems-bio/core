#' Render file section
#'
#' @param spec file spec
#' @return string
#' 
#' @export
#' @examples
#' \dontrun{
#' render_file(spec, 'path/to/yaml')
#' }

render_file <- function(spec) {
  if (is.character(spec)) {
    spec <- read_file_spec(spec)
  }

  if (!"label" %in% names(spec$info)) {
    spec$info$label <- basename(spec$info$example)
  }

  example <-
    if (is.null(spec$info$example) || is.na(spec$info$example)) {
      ""
    } else {
      paste0("Example file: `", spec$info$example, "`")
    }

  description <-
    if (is.null(spec$info$description) || is.na(spec$info$description)) {
      ""
    } else {
      paste0("Description:\n\n", spec$info$description)
    }

  strip_margin(glue::glue("
    §## File format: {spec$info$label}
    §
    §{spec$info$summary %||% ''}
    §
    §{example}
    §
    §{description}
    §
    §Format:
    §
    §:::{{.small}}
    §{paste(format_file_format(spec), collapse = '\n')}
    §:::
    §
    §Slot description:
    §
    §:::{{.small}}
    §{paste(format_file_format_as_kable(spec), collapse = '\n')}
    §:::
    §
    §"), symbol = "§")
}