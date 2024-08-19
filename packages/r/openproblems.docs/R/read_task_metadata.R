#' Read the api files in a task
#'
#' This function reads the api files in a task and returns a list with the api info
#'
#' @param path Path to a src directory
#' @return A list with the api info
#'
#' @importFrom cli cli_inform cli_abort
#'
#' @export
#' @examples
#' path <- system.file("extdata", "example_project", package = "openproblems.docs")
#'
#' task_metadata <- read_task_metadata(path)
#'
#' task_metadata
read_task_metadata <- function(path) {
  cli::cli_inform("Looking for project root")
  project_path <- openproblems::find_project_root(path)

  cli::cli_inform(paste0("Project root found at '", project_path, "'"))
  api_dir <- file.path(path, "api")
  proj_conf_file <- file.path(project_path, "_viash.yaml")
  if (!dir.exists(api_dir)) {
    cli::cli_abort("No api directory found")
  }
  if (!file.exists(proj_conf_file)) {
    cli::cli_abort("No project config file found")
  }

  cli::cli_inform("Reading project config")
  proj_conf <- read_project_config(proj_conf_file)

  cli::cli_inform("Reading component yamls")
  comp_yamls <- list.files(api_dir, pattern = "comp_.*\\.ya?ml", full.names = TRUE)
  comps <- map(comp_yamls, read_component_spec)
  comp_info <- map_df(comps, "info")
  comp_args <- map_df(comps, "args")
  names(comps) <- comp_info$file_name

  cli::cli_inform("Reading file yamls")
  file_yamls <- openproblems:::resolve_path(
    path = na.omit(unique(comp_args$`__merge__`)),
    project_path = project_path,
    parent_path = api_dir
  )
  files <- map(file_yamls, read_file_format)
  file_info <- map_df(files, "info")
  file_slots <- map_df(files, "slots")
  names(files) <- file_info$file_name

  cli::cli_inform("Generating task graph")
  task_graph <- .task_graph_generate(file_info, comp_info, comp_args)
  task_graph_root <- .task_graph_get_root(task_graph)
  task_graph_order <- names(igraph::bfs(task_graph, task_graph_root)$order)

  list(
    proj_path = project_path,
    proj_conf = proj_conf,
    files = files,
    file_info = file_info,
    file_slots = file_slots,
    comps = comps,
    comp_info = comp_info,
    comp_args = comp_args,
    task_graph = task_graph,
    task_graph_root = task_graph_root,
    task_graph_order = task_graph_order
  )
}

.task_graph_generate <- function(file_info, comp_info, comp_args) {
  clean_id <- function(id) {
    gsub("graph", "graaf", id)
  }
  nodes <-
    bind_rows(
      file_info |>
        mutate(id = .data$file_name, is_comp = FALSE),
      comp_info |>
        mutate(id = .data$file_name, is_comp = TRUE)
    ) |>
    select("id", "label", everything()) |>
    mutate(str = paste0(
      "  ",
      clean_id(.data$id),
      ifelse(.data$is_comp, "[/\"", "(\""),
      .data$label,
      ifelse(.data$is_comp, "\"/]", "\")")
    ))
  edges <- bind_rows(
    comp_args |>
      filter(.data$type == "file", .data$direction == "input") |>
      mutate(
        from = .data$parent,
        to = .data$file_name,
        arrow = "---"
      ),
    comp_args |>
      filter(.data$type == "file", .data$direction == "output") |>
      mutate(
        from = .data$file_name,
        to = .data$parent,
        arrow = "-->"
      )
  ) |>
    select("from", "to", everything()) |>
    mutate(str = paste0("  ", clean_id(.data$from), .data$arrow, clean_id(.data$to)))

  igraph::graph_from_data_frame(
    edges,
    vertices = nodes,
    directed = TRUE
  )
}

.task_graph_get_root <- function(task_graph) {
  root <- names(which(igraph::degree(task_graph, mode = "in") == 0))
  if (length(root) > 1) {
    cli::cli_warn(paste0(
      "There should probably only be one node with in-degree equal to 0.\n",
      "  Nodes with in-degree == 0: ", paste(root, collapse = ", ")
    ))
  }
  root[[1]]
}
