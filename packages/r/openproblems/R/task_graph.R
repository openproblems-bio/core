#' Read the api files in a task
#'#'
#' @param path Path to a src directory
#' @return A list with the api info
#' 
#' @export
#' @examples
#' \dontrun{
#' read_api_files("src)
#' }

create_task_graph <- function(file_info, comp_info, comp_args) {
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

.task_graph_get_root <- function(task_api) {
  root <- names(which(igraph::degree(task_api$task_graph, mode = "in") == 0))
  if (length(root) > 1) {
    warning(
      "There should probably only be one node with in-degree equal to 0.\n",
      "  Nodes with in-degree == 0: ", paste(root, collapse = ", ")
    )
  }
  root[[1]]
}

render_task_graph <- function(task_api, root = .task_graph_get_root(task_api)) {
  order <- names(igraph::bfs(task_api$task_graph, root)$order)

  vdf <- igraph::as_data_frame(task_api$task_graph, "vertices") %>%
    arrange(match(name, order))
  edf <- igraph::as_data_frame(task_api$task_graph, "edges") %>%
    arrange(match(from, order), match(to, order))

  openproblems::strip_margin(glue::glue("
    §```mermaid
    §flowchart LR
    §{paste(vdf$str, collapse = '\n')}
    §{paste(edf$str, collapse = '\n')}
    §```
    §"), symbol = "§")
}