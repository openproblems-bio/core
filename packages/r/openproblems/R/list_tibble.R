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

#' set list as tibble
#'#'
#' @param li list
#' @return dataframe of list
#' 
#' @export
#' @examples
#' \dontrun{
#' list_as_tibble(li)
#' }


list_as_tibble <- function(li) {
  as.data.frame(li[sapply(li, is.atomic)], check.names = FALSE)
}