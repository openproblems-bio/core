#' Turn a list into a dataframe
#'
#' This will remove any non-atomic elements from the list and turn it into a dataframe.
#'
#' Note: this will only work if the list of atomic vectors are
#' of the same length or length 1.
#'
#' @param li A list
#' @return A tibble
#' 
#' @importFrom tibble as_tibble
#'
#' @export
#' @examples
#' li <- list(
#'   a = c(1, 2, 3),
#'   b = c("a", "b", "c")
#' )
#' list_as_tibble(li)
list_as_tibble <- function(li) {
  li_subset <- li[sapply(li, is.atomic)]
  as_tibble(as.data.frame(li_subset, check.names = FALSE))
}
