#' Read file specification
#'
#' @param path Path to yaml file
#' @return list with file info and slots
#'
#' @export
#' @examples
#' path <- system.file("extdata", "example_project", "api", "file_train_h5ad.yaml", package = "openproblems.docs")
#'
#' read_file_format(path)
read_file_format <- function(path) {
  spec <- openproblems::read_nested_yaml(path)
  out <- list(
    info = read_file_format_info(spec, path)
  )
  if (out$info$file_type == "h5ad" || "slots" %in% names(spec$info)) {
    out$info$file_type <- "h5ad"
    out$slots <- read_file_format__process_h5ad(spec, path)
  }
  if (out$info$file_type == "csv" || out$info$file_type == "tsv" || out$info$file_type == "parquet") {
    out$columns <- read_file_format__process_tabular(spec, path)
  }
  out
}

read_file_format_info <- function(spec, path) {
  # TEMP: make it readable
  spec$info$slots <- NULL
  df <- list_as_tibble(spec)
  if (is_list_a_dataframe(spec$info)) {
    df <- dplyr::bind_cols(df, list_as_tibble(spec$info))
  }
  df$file_name <- basename(path) %>% str_replace_all("\\.yaml", "")
  df$description <- df$description %||% NA_character_ %>% as.character()
  df$summary <- df$summary %||% NA_character_ %>% as.character()
  as_tibble(df)
}

read_file_format__process_h5ad <- function(spec, path) {
  map_df(
    anndata_struct_names,
    function(struct_name, slot) {
      slot <- spec$info$slots[[struct_name]]
      if (is.null(slot)) {
        return(NULL)
      }
      df <- map_df(slot, as.data.frame)
      df$struct <- struct_name
      df$file_name <- basename(path) %>% str_replace_all("\\.yaml", "")
      df$required <- df$required %||% TRUE %|% TRUE
      df$multiple <- df$multiple %||% FALSE %|% FALSE
      as_tibble(df)
    }
  )
}

#' Read columns from tabular file
#'
#' @param spec file spec
#' @param path Path to yaml file
#' @return tibble with columns
#'
#' @noRd
read_file_format__process_tabular <- function(spec, path) {
  map_df(
    spec$info$columns,
    function(column) {
      df <- list_as_tibble(column)
      df$file_name <- str_replace_all(path) %>% gsub("\\.yaml", "")
      df$required <- df$required %||% TRUE %|% TRUE
      df$multiple <- df$multiple %||% FALSE %|% FALSE
      as_tibble(df)
    }
  )
}
