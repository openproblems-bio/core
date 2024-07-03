#' Find the root of a Viash project
#' 
#' This function will recursively search for a `_viash.yaml` file
#' in the parent directories of the given path.
#' 
#' @param path Path to a file or directory
#' @return The path to the root of the Viash project, or NULL if not found
#' 
#' @export
#' @examples
#' \dontrun{
#' find_project_root("/path/to/project/subdir")
#' }
find_project_root <- function(path) {
  path <- normalizePath(path, mustWork = FALSE)
  check <- paste0(dirname(path), "/_viash.yaml")
  if (file.exists(check)) {
    dirname(check)
  } else if (check == "//_viash.yaml") {
    NULL
  } else {
    find_project_root(dirname(check))
  }
}