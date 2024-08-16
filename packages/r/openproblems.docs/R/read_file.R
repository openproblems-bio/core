#' Read file specification
#'
#' @param path Path to yaml file
#' @return list with file info and slots
#' 
#' @examples
#' \dontrun{
#' read_file_spec('path/to/yaml')
#' }

read_file_spec <- function(path) {
  spec <- openproblems::read_and_merge_yaml(path)
  out <- list(
    info = read_file_info(spec, path)
  )
  if (out$info$file_type == "h5ad" || "slots" %in% names(spec$info)) {
    out$info$file_type <- "h5ad"
    out$slots <- read_anndata_slots(spec, path)
  }
  if (out$info$file_type == "csv" || out$info$file_type == "tsv" || out$info$file_type == "parquet") {
    out$columns <- read_tabular_columns(spec, path)
  }
  out
}

#' Read file info
#'
#' @param spec file spec
#' @param path Path to yaml file
#' @return tibble with file info
#' 
#' @examples
#' \dontrun{
#' read_file_info(spec, 'path/to/yaml')
#' }

read_file_info <- function(spec, path) {
  # TEMP: make it readable
  spec$info$slots <- NULL
  df <- list_as_tibble(spec)
  if (list_contains_tibble(spec$info)) {
    df <- dplyr::bind_cols(df, list_as_tibble(spec$info))
  }
  df$file_name <- basename(path) %>% gsub("\\.yaml", "", .)
  df$description <- df$description %||% NA_character_ %>% as.character
  df$summary <- df$summary %||% NA_character_ %>% as.character
  as_tibble(df)
}

#' Read anndata slots
#'
#' @param spec file spec
#' @param path Path to yaml file
#' @return tibble with file slots
#' 
#' @examples
#' \dontrun{
#' read_anndata_slots(spec, 'path/to/yaml')
#' }



read_anndata_slots <- function(spec, path) {
  map_df(
    anndata_struct_names,
    function(struct_name, slot) {
      slot <- spec$info$slots[[struct_name]]
      if (is.null(slot)) return(NULL)
      df <- map_df(slot, as.data.frame)
      df$struct <- struct_name
      df$file_name <- basename(path) %>% gsub("\\.yaml", "", .)
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
#' @examples
#' \dontrun{
#' read_tabular_columns(spec, 'path/to/yaml')
#' }

read_tabular_columns <- function(spec, path) {
  map_df(
    spec$info$columns,
    function(column) {
      df <- list_as_tibble(column)
      df$file_name <- basename(path) %>% gsub("\\.yaml", "", .)
      df$required <- df$required %||% TRUE %|% TRUE
      df$multiple <- df$multiple %||% FALSE %|% FALSE
      as_tibble(df)
    }
  )
}