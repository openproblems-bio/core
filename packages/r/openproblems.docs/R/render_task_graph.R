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
render_task_graph <- function(task_api) {
  root <- task_api$task_graph_root
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
