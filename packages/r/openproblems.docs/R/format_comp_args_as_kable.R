#' Format the arguments of a component as a tibble
#'
#' @param spec file spec
#' @return tibble with file info
#'
#' @examples
#' \dontrun{
#' format_comp_args_as_tibble(spec)
#' }
format_comp_args_as_tibble <- function(spec) {
  if (nrow(spec$args) == 0) {
    return("")
  }
  spec$args %>%
    mutate(
      tag_str = pmap_chr(lst(required, direction), function(required, direction) {
        out <- c()
        if (!required) {
          out <- c(out, "Optional")
        }
        if (direction == "output") {
          out <- c(out, "Output")
        }
        if (length(out) == 0) {
          ""
        } else {
          paste0("(_", paste(out, collapse = ", "), "_) ")
        }
      })
    ) %>%
    transmute(
      Name = paste0("`--", arg_name, "`"),
      Type = paste0("`", type, "`"),
      Description = paste0(
        tag_str,
        (summary %|% description) %>% gsub(" *\n *", " ", .) %>% gsub("\\. *$", "", .),
        ".",
        ifelse(!is.na(default), paste0(" Default: `", default, "`."), "")
      )
    ) %>%
    knitr::kable()
}
