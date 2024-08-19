#' Read the api files in a task
#'
#' @param path Path to a src directory
#' @return A list with the api info
#'
#' @importFrom cli cli_inform
#' @export
#' @examples
#' path <- system.file("extdata", "example_project", package = "openproblems.docs")
#'
#' read_task_metadata(path)
read_task_metadata <- function(path) {
  cli::cli_inform("Looking for project root")
  project_path <- openproblems::find_project_root(path)
  api_dir <- file.path(path, "api")

  cli::cli_inform("Reading project config")
  # TODO: read _viash.yaml

  cli::cli_inform("Reading component yamls")
  comp_yamls <- list.files(api_dir, pattern = "comp_.*\\.ya?ml", full.names = TRUE)
  comps <- map(comp_yamls, read_component_spec)
  comp_info <- map_df(comps, "info")
  comp_args <- map_df(comps, "args")

  cli::cli_inform("Reading file yamls")
  file_yamls <- openproblems:::resolve_path(
    path = na.omit(unique(comp_args$`__merge__`)),
    project_path = project_path,
    parent_path = api_dir
  )
  files <- map(file_yamls, read_file_format)
  file_info <- map_df(files, "info")
  file_slots <- map_df(files, "slots")

  cli::cli_inform("Generating task graph")
  task_graph <- .task_graph_generate(file_info, comp_info, comp_args)
  task_graph_root <- .task_graph_get_root(task_graph)

  list(
    file_info = file_info,
    file_slots = file_slots,
    comp_info = comp_info,
    comp_args = comp_args,
    task_graph = task_graph,
    task_graph_root = task_graph_root
  )
}

.task_graph_generate <- function(file_info, comp_info, comp_args) {
  clean_id <- function(id) {
    gsub("graph", "graaf", id)
  }
  nodes <-
    bind_rows(
      file_info %>%
        mutate(id = file_name, label = label, is_comp = FALSE),
      comp_info %>%
        mutate(id = file_name, label = label, is_comp = TRUE)
    ) %>%
    select(id, label, everything()) %>%
    mutate(str = paste0(
      "  ",
      clean_id(id),
      ifelse(is_comp, "[/\"", "(\""),
      label,
      ifelse(is_comp, "\"/]", "\")")
    ))
  edges <- bind_rows(
    comp_args %>%
      filter(type == "file", direction == "input") %>%
      mutate(
        from = parent,
        to = file_name,
        arrow = "---"
      ),
    comp_args %>%
      filter(type == "file", direction == "output") %>%
      mutate(
        from = file_name,
        to = parent,
        arrow = "-->"
      )
  ) %>%
    select(from, to, everything()) %>%
    mutate(str = paste0("  ", clean_id(from), arrow, clean_id(to)))

  igraph::graph_from_data_frame(
    edges,
    vertices = nodes,
    directed = TRUE
  )
}

.task_graph_get_root <- function(task_graph) {
  root <- names(which(igraph::degree(task_graph, mode = "in") == 0))
  if (length(root) > 1) {
    cli::cli_warn(
      "There should probably only be one node with in-degree equal to 0.\n",
      "  Nodes with in-degree == 0: ", paste(root, collapse = ", ")
    )
  }
  root[[1]]
}