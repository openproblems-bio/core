#' Create the task graph
#'
#' @param file_info tibble with file info
#' @param comp_info tibble with component info
#' @param comp_args tibble with component arguments
#' @return igraph
#'
#' @export
#' @examples
#' \dontrun{
#' create_task_graph(file_info, comp_info, comp_args)
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
