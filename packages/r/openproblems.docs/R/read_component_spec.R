#' read component spec
#'
#' @param path path to comp yaml
#' @return a list with compontent info and arguments
#'
#' @export
#' @examples
#' path <- system.file("extdata", "example_project", "api", "comp_method.yaml", package = "openproblems.docs")
#'
#' read_component_spec(path)
read_component_spec <- function(path) {
  spec_yaml <- openproblems::read_nested_yaml(path)
  list(
    info = read_component_spec_info(spec_yaml, path),
    args = read_component_spec_arguments(spec_yaml, path)
  )
}

read_component_spec_info <- function(spec_yaml, path) {
  # TEMP: make it readable
  spec_yaml$arguments <- NULL
  spec_yaml$argument_groups <- NULL

  df <- list_as_tibble(spec_yaml)
  if (is_list_a_dataframe(spec_yaml$info)) {
    df <- dplyr::bind_cols(df, list_as_tibble(spec_yaml$info))
  }
  if (is_list_a_dataframe(spec_yaml$info$type_info)) {
    df <- dplyr::bind_cols(df, list_as_tibble(spec_yaml$info$type_info))
  }
  df$file_name <- basename(path) %>% str_replace_all("\\.yaml", "")
  as_tibble(df)
}

read_component_spec_arguments <- function(spec_yaml, path) {
  arguments <- spec_yaml$arguments
  for (arg_group in spec_yaml$argument_groups) {
    arguments <- c(arguments, arg_group$arguments)
  }
  map_df(arguments, function(arg) {
    df <- list_as_tibble(arg)
    if (is_list_a_dataframe(arg$info)) {
      df <- dplyr::bind_cols(df, list_as_tibble(arg$info))
    }
    df$file_name <- basename(path) %>% str_replace_all("\\.yaml", "")
    df$arg_name <- str_replace_all(arg$name, "^-*", "")
    df$direction <- df$direction %||% "input" %|% "input"
    df$parent <- df$`__merge__` %||% NA_character_ %>%
      basename() %>%
      str_replace_all("\\.yaml", "")
    df$required <- df$required %||% FALSE %|% FALSE
    df$default <- df$default %||% NA_character_ %>% as.character()
    df$example <- df$example %||% NA_character_ %>% as.character()
    df$description <- df$description %||% NA_character_ %>% as.character()
    df$summary <- df$summary %||% NA_character_ %>% as.character()
    df
  })
}
