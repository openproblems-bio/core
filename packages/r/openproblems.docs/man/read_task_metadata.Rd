% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/read_task_metadata.R
\name{read_task_metadata}
\alias{read_task_metadata}
\title{Read the api files in a task}
\usage{
read_task_metadata(path)
}
\arguments{
\item{path}{Path to the API directory of a task}
}
\value{
A list with the api info
}
\description{
This function reads the api files in a task and returns a list with the api info
}
\examples{
path <- system.file("extdata", "example_project", "api", package = "openproblems.docs")

task_metadata <- read_task_metadata(path)

task_metadata
}
