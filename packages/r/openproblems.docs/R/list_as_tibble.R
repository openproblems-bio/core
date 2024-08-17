#' set list as tibble
#'
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
