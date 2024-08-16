requireNamespace("assertthat", quietly = TRUE)

## VIASH START
## VIASH END

task_template <- "/task_template"
output_path <- "output.md"
setwd(task_template)
cat(">> Running the script as test\n")
system(paste(
  meta["executable"],
  "--output", output_path,
  "--task_dir", "src"
))

cat(">> Checking whether output files exist\n")
assertthat::assert_that(file.exists(output_path))

cat(">> Checking file contents\n")
lines <- readLines(output_path)
assertthat::assert_that(any(grepl("# Template", lines)))
assertthat::assert_that(any(grepl("# Description", lines)))
assertthat::assert_that(any(grepl("# Motivation", lines)))
assertthat::assert_that(any(grepl("# Authors", lines)))
assertthat::assert_that(any(grepl("flowchart LR", lines)))
assertthat::assert_that(any(grepl("# File format:", lines)))

cat("All checks succeeded!\n")
