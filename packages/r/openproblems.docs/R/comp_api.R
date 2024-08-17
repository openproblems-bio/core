#' read component spec
#'
#' @param path path to comp yaml
#' @return a list with compontent info and arguments
#' 
#' @examples
#' \dontrun{
#' read_comp_spec("src/path/to/comp.yaml")
#' }

read_comp_spec <- function(path) {
  spec_yaml <- openproblems::read_nested_yaml(path)
  list(
    info = read_comp_info(spec_yaml, path),
    args = read_comp_args(spec_yaml, path)
  )
}

#' read component spec
#'
#' @param spec_yaml comp yaml
#' @param path path to comp yaml
#' @return A tibble with component info
#' 
#' @examples
#' \dontrun{
#' read_comp_info(spec_yaml, "src/path/to/comp.yaml")
#' }

read_comp_info <- function(spec_yaml, path) {
  # TEMP: make it readable
  spec_yaml$arguments <- NULL
  spec_yaml$argument_groups <- NULL
  
  df <- list_as_tibble(spec_yaml)
  if (list_contains_tibble(spec_yaml$info)) {
    df <- dplyr::bind_cols(df, list_as_tibble(spec_yaml$info))
  }
  if (list_contains_tibble(spec_yaml$info$type_info)) {
    df <- dplyr::bind_cols(df, list_as_tibble(spec_yaml$info$type_info))
  }
  df$file_name <- basename(path) %>% gsub("\\.yaml", "", .)
  as_tibble(df)
}

#' read component arguments
#'
#' @param spec_yaml comp yaml
#' @param path path to comp yaml
#' @return a df with component arguments
#' 
#' @examples
#' \dontrun{
#' read_comp_args(spec_yaml, "src/path/to/comp.yaml")
#' }

read_comp_args <- function(spec_yaml, path) {
  arguments <- spec_yaml$arguments
  for (arg_group in spec_yaml$argument_groups) {
    arguments <- c(arguments, arg_group$arguments)
  }
  map_df(arguments, function(arg) {
    df <- list_as_tibble(arg)
    if (list_contains_tibble(arg$info)) {
      df <- dplyr::bind_cols(df, list_as_tibble(arg$info))
    }
    df$file_name <- basename(path) %>% gsub("\\.yaml", "", .)
    df$arg_name <- gsub("^-*", "", arg$name)
    df$direction <- df$direction %||% "input" %|% "input"
    df$parent <- df$`__merge__` %||% NA_character_ %>% basename() %>% gsub("\\.yaml", "", .)
    df$required <- df$required %||% FALSE %|% FALSE
    df$default <- df$default %||% NA_character_ %>% as.character
    df$example <- df$example %||% NA_character_ %>% as.character
    df$description <- df$description %||% NA_character_ %>% as.character
    df$summary <- df$summary %||% NA_character_ %>% as.character
    df
  })
}