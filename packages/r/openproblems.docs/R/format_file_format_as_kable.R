#' Format file spec format as kable
#'
#' @param spec file spec
#' @return table
#'
#' @noRd
format_file_format_as_kable <- function(spec) {
  if (spec$info$file_type == "h5ad") {
    spec$slots %>%
      mutate(
        tag_str = pmap_chr(lst(required), function(required) {
          out <- c()
          if (!required) {
            out <- c(out, "Optional")
          }
          if (length(out) == 0) {
            ""
          } else {
            paste0("(_", paste(out, collapse = ", "), "_) ")
          }
        })
      ) %>%
      transmute(
        Slot = paste0("`", struct, "[\"", name, "\"]`"),
        Type = paste0("`", type, "`"),
        Description = paste0(
          tag_str,
          description %>% str_replace_all(" *\n *", " ") %>% str_replace_all("\\. *$", ""),
          "."
        )
      ) %>%
      knitr::kable()
  } else if (spec$info$file_type == "csv" || spec$info$file_type == "tsv" || spec$info$file_type == "parquet") {
    spec$columns %>%
      mutate(
        tag_str = pmap_chr(lst(required), function(required) {
          out <- c()
          if (!required) {
            out <- c(out, "Optional")
          }
          if (length(out) == 0) {
            ""
          } else {
            paste0("(_", paste(out, collapse = ", "), "_) ")
          }
        })
      ) %>%
      transmute(
        Column = paste0("`", name, "`"),
        Type = paste0("`", type, "`"),
        Description = paste0(
          tag_str,
          description %>% str_replace_all(" *\n *", " ") %>% str_replace_all("\\. *$", ""),
          "."
        )
      ) %>%
      knitr::kable()
  } else {
    ""
  }
}
