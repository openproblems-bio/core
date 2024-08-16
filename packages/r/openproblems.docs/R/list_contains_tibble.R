#' check if list contains tibble
#'#'
#' @param li list
#' @return boolean
#' 
#' @export
#' @examples
#' \dontrun{
#' list_contains_tibble(li)
#' }

list_contains_tibble <- function(li) {
  is.list(li) && any(sapply(li, is.atomic))
}
