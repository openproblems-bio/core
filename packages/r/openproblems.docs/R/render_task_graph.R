#' get task graph root
#'
#' @param task_api The task api filepath
#' @return string with root of the task graph
#'
#' @examples
#' \dontrun{
#' .task_graph_get_root(task_api)
#' }
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

#' Render the task graph
#'
#' @param task_api the task api filepath
#' @param root root of the task graph
#' @return igraph
#'
#' @export
#' @examples
#' \dontrun{
#' render_task_graph(task_api)
#' }
render_task_graph <- function(task_api, root = .task_graph_get_root(task_api)) {
  order <- names(igraph::bfs(task_api$task_graph, root)$order)

  vdf <- igraph::as_data_frame(task_api$task_graph, "vertices") %>%
    arrange(match(name, order))
  edf <- igraph::as_data_frame(task_api$task_graph, "edges") %>%
    arrange(match(from, order), match(to, order))

  openproblems::strip_margin(glue::glue("
    |```mermaid
    |flowchart LR
    |{paste(vdf$str, collapse = '\n')}
    |{paste(edf$str, collapse = '\n')}
    |```
    |"), symbol = "\\|")
}
