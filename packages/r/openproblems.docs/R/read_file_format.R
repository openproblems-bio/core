#' Read file format
#'
#' This function reads a file format spec from a yaml file.
#'
#' @param path Path to a file format yaml, usually in `src/api/file_*.yaml`
#' @return A list with file format info and slots/columns
#'
#' @export
#' @examples
#' path <- system.file(
#'   "extdata", "example_project", "api", "file_train_h5ad.yaml",
#'   package = "openproblems.docs"
#' )
#'
#' read_file_format(path)
read_file_format <- function(path) {
  spec <- openproblems::read_nested_yaml(path)
  out <- list(
    info = read_file_format__process_info(spec, path)
  )
  # TODO: update
  format_type <- spec$info$format$type

  if (format_type == "h5ad") {
    out$info$file_type <- "h5ad"
    out$slots <- read_file_format__process_h5ad(spec, path)
  }
  if (format_type %in% c("tabular", "csv", "tsv")) {
    out$columns <- read_file_format__process_tabular(spec, path)
  }
  out
}

#' @importFrom openproblems.utils list_as_data_frame is_list_a_dataframe
read_file_format__process_info <- function(spec, path) {
  df <- list_as_data_frame(spec)

  # make sure some fields are always present
  df$file_name <- basename(path) |> str_replace_all("\\.yaml", "")
  df$file_type <- spec$info$format$type %||% NA_character_ |> as.character()
  df$description <- df$description %||% NA_character_ |> as.character()
  df$summary <- df$summary %||% NA_character_ |> as.character()

  as_tibble(df)
}

read_file_format__process_h5ad <- function(spec, path) {
  map_df(
    anndata_struct_names,
    function(struct_name) {
      fields <- spec$info$format[[struct_name]]
      if (is.null(fields)) {
        return(NULL)
      }
      df <- map_df(fields, as.data.frame)

      # make sure some fields are always present
      df$struct <- struct_name
      df$file_name <- basename(path) |> str_replace_all("\\.yaml", "")
      df$required <- df$required %||% TRUE %|% TRUE
      df$multiple <- df$multiple %||% FALSE %|% FALSE
      df$description <- df$description %||% NA_character_ |> as.character()
      df$summary <- df$summary %||% NA_character_ |> as.character()

      as_tibble(df)
    }
  )
}

read_file_format__process_tabular <- function(spec, path) { # nolint object_length_linter
  map_df(
    spec$info$columns,
    function(column) {
      df <- list_as_data_frame(column)

      # make sure some fields are always present
      df$file_name <- str_replace_all(path) |> gsub("\\.yaml", "")
      df$required <- df$required %||% TRUE %|% TRUE
      df$multiple <- df$multiple %||% FALSE %|% FALSE
      df$description <- df$description %||% NA_character_ |> as.character()
      df$summary <- df$summary %||% NA_character_ |> as.character()

      as_tibble(df)
    }
  )
}
