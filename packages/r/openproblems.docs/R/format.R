#' Format the arguments of a component as a tibble
#'
#' @param spec file spec
#' @return tibble with file info
#' 
#' @examples
#' \dontrun{
#' format_comp_args_as_tibble(spec)
#' }

format_comp_args_as_tibble <- function(spec) {
  if (nrow(spec$args) == 0) return("")
  spec$args %>%
    mutate(
      tag_str = pmap_chr(lst(required, direction), function(required, direction) {
        out <- c()
        if (!required) {
          out <- c(out, "Optional")
        }
        if (direction == "output") {
          out <- c(out, "Output")
        }
        if (length(out) == 0) {
          ""
        } else {
          paste0("(_", paste(out, collapse = ", "), "_) ")
        }
      })
    ) %>%
    transmute(
      Name = paste0("`--", arg_name, "`"),
      Type = paste0("`", type, "`"),
      Description = paste0(
        tag_str,
        (summary %|% description) %>% gsub(" *\n *", " ", .) %>% gsub("\\. *$", "", .), 
        ".",
        ifelse(!is.na(default), paste0(" Default: `", default, "`."), "")
      )
    ) %>%
    knitr::kable()
}

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

#' Format file spec format as kable
#'
#' @param spec file spec
#' @return table
#' 
#' @examples
#' \dontrun{
#' format_file_format_as_kable(spec)
#' }

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
          description %>% gsub(" *\n *", " ", .) %>% gsub("\\. *$", "", .), 
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
          description %>% gsub(" *\n *", " ", .) %>% gsub("\\. *$", "", .), 
          "."
        )
      ) %>%
      knitr::kable()
  } else {
    ""
  }
}