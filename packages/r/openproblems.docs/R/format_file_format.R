#' Format the file spec format
#'
#' @param spec file spec
#' @return string
#'
#' @noRd
format_file_format <- function(spec) {
  format_type <- spec$info$format$type
  if (format_type == "h5ad") {
    example <- spec$slots %>%
      group_by(.data$struct) %>%
      summarise(
        str = paste0(unique(.data$struct), ": ", paste0("'", .data$name, "'", collapse = ", "))
      ) %>%
      arrange(match(.data$struct, anndata_struct_names))

    c("    AnnData object", paste0("     ", example$str))
  } else if (format_type %in% c("csv", "tsv", "parquet")) {
    example <- spec$columns %>%
      summarise(
        str = paste0("'", .data$name, "'", collapse = ", ")
      )

    c("    Tabular data", paste0("     ", example$str))
  } else {
    ""
  }
}
