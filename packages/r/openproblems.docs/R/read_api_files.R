#' Read the api files in a task
#'
#' @param path Path to a src directory
#' @return A list with the api info
#'
#' @export
#' @examples
#' \dontrun{
#' read_api_files("src")
#' }
read_api_files <- function(path) {
  cli::cli_inform("Looking for project root")
  project_path <- openproblems::find_project_root(path)
  api_dir <- paste0(path, "/api")

  cli::cli_inform("Reading component yamls")
  comp_yamls <- list.files(api_dir, pattern = "comp_.*\\.ya?ml", full.names = TRUE)
  comps <- map(comp_yamls, read_comp_spec)
  comp_info <- map_df(comps, "info")
  comp_args <- map_df(comps, "args")
  names(comps) <- basename(comp_yamls) %>% gsub("\\..*$", "", .)

  cli::cli_inform("Reading file yamls")
  file_yamls <- openproblems:::resolve_path(
    path = na.omit(unique(comp_args$`__merge__`)),
    project_path = project_path,
    parent_path = api_dir
  )
  files <- map(file_yamls, read_file_spec)
  names(files) <- basename(file_yamls) %>% gsub("\\..*$", "", .)
  file_info <- map_df(files, "info")
  file_slots <- map_df(files, "slots")

  cli::cli_inform("Generating task graph")
  task_graph <- create_task_graph(file_info, comp_info, comp_args)

  list(
    file_specs = files,
    file_info = file_info,
    file_slots = file_slots,
    comp_specs = comps,
    comp_info = comp_info,
    comp_args = comp_args,
    task_graph = task_graph
  )
}
