#' Read component spec
#'
#' This function reads a component spec from a yaml file.
#'
#' @param path Path to a component spec yaml, usually in `src/api/comp_*.yaml`
#' @return A list with compontent info and arguments
#'
#' @export
#' @examples
#' path <- system.file(
#'   "extdata", "example_project", "api", "comp_method.yaml",
#'   package = "openproblems.docs"
#' )
#'
#' read_component_spec(path)
read_component_spec <- function(path) {
  spec_yaml <- openproblems::read_nested_yaml(path)
  list(
    info = read_component_spec__process_info(spec_yaml, path),
    args = read_component_spec_arguments(spec_yaml, path)
  )
}

#' @importFrom openproblems.utils list_as_data_frame is_list_a_dataframe
read_component_spec__process_info <- function(spec_yaml, path) { # nolint object_length_linter
  df <- list_as_data_frame(spec_yaml)
  if (is_list_a_dataframe(spec_yaml$info)) {
    df <- dplyr::bind_cols(df, list_as_data_frame(spec_yaml$info))
  }
  if (is_list_a_dataframe(spec_yaml$info$type_info)) {
    df <- dplyr::bind_cols(df, list_as_data_frame(spec_yaml$info$type_info))
  }
  df$file_name <- basename(path) |> str_replace_all("\\.yaml", "")
  as_tibble(df)
}

read_component_spec_arguments <- function(spec_yaml, path) {
  arguments <- spec_yaml$arguments
  for (arg_group in spec_yaml$argument_groups) {
    arguments <- c(arguments, arg_group$arguments)
  }
  map_dfr(arguments, function(arg) {
    df <- list_as_data_frame(arg)
    if (is_list_a_dataframe(arg$info)) {
      df <- dplyr::bind_cols(df, list_as_data_frame(arg$info))
    }
    df$file_name <- basename(path) |> str_replace_all("\\.yaml", "")
    df$arg_name <- str_replace_all(arg$name, "^-*", "")
    df$direction <- df$direction %||% "input" %|% "input"
    df$parent <- df$`__merge__` %||% NA_character_ |>
      basename() |>
      str_replace_all("\\.yaml", "")
    df$required <- df$required %||% FALSE %|% FALSE
    df$default <- df$default %||% NA_character_ |> as.character()
    df$example <- df$example %||% NA_character_ |> as.character()
    df$description <- df$description %||% NA_character_ |> as.character()
    df$summary <- df$summary %||% NA_character_ |> as.character()
    as_tibble(df)
  })
}
