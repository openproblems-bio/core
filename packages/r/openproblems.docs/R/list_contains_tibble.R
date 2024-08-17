#' Check if this list could be a data frame
#'
#' @param li list
#' @return whether the list could be a data frame
#'
#' @noRd
#' @examples
#' df <- list(
#'   a = c(1, 2, 3),
#'   b = c("a", "b", "c")
#' )
#' is_list_a_dataframe(df)
#' 
#' li <- list(
#' 
is_list_a_dataframe <- function(li) {
  is.list(li) && any(sapply(li, is.atomic))
}
