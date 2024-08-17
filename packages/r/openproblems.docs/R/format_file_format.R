#' Format the file spec format
#'
#' @param spec file spec
#' @return string
#'
#' @examples
#' \dontrun{
#' format_file_format(spec)
#' }
format_file_format <- function(spec) {
  if (spec$info$file_type == "h5ad") {
    example <- spec$slots %>%
      group_by(struct) %>%
      summarise(
        str = paste0(unique(struct), ": ", paste0("'", name, "'", collapse = ", "))
      ) %>%
      arrange(match(struct, anndata_struct_names))

    c("    AnnData object", paste0("     ", example$str))
  } else if (spec$info$file_type == "csv" || spec$info$file_type == "tsv" || spec$info$file_type == "parquet") {
    example <- spec$columns %>%
      summarise(
        str = paste0("'", name, "'", collapse = ", ")
      )

    c("    Tabular data", paste0("     ", example$str))
  } else {
    ""
  }
}
