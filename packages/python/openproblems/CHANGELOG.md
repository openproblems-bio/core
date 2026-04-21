# openproblems core Python v0.2.0

## NEW FUNCTIONALITY

* `project`:
  - `resolve_path`: Resolve a path relative to a parent path or project root.

* `project.component_tests`:
  - `run_check_config` / `check_config`: Validate a component's Viash config (namespace, type, metadata, normalization, variants, Nextflow runner).
  - `run_and_check_output`: Run a component executable and validate its output files against format specifications.

* `project.docs`:
  - `read_task_config`: Read a task-level configuration file.
  - `read_task_metadata`: Read and assemble full task metadata by traversing the task's component graph.
  - `read_component_spec`: Read a component API specification.
  - `read_file_format`: Read a file format specification.
  - `render_task_readme_qmd`: Render a Quarto README document for a task.
  - `render_component_spec`: Render a component specification as a Markdown section.
  - `render_file_format`: Render a file format specification as a Markdown section.

## MINOR CHANGES

* Improve diagnostic print messages in `check_config` and `run_and_check_output` to be more descriptive.

# openproblems core Python v0.1.1

## NEW FUNCTIONALITY

* Add support for python 3.9 (PR #17).

* Add support for python 3.13 (PR #18).

# openproblems core Python v0.1.0

Initial release

## NEW FUNCTIONALITY

* `project`:
  - `find_project_root`: Find the root of a Viash project.
  - `read_nested_yaml`: Read a nested YAML file.
  - `read_viash_config`: Read a viash configuration file (PR #8).

* `utils`:
  - `strip_margin`: Strip margin from a string
  - `deep_merge`: Merge two dictionaries recursively

## MAJOR CHANGES

* Bump minimum Python version to 3.10 (PR #11).

## MINOR CHANGES

* Add dependencies to project toml file (PR #1).

* Clean up project toml file (PR #8).

## BUG FIXES

* Fix recursion bug in `find_project_root` (PR #11).

## TESTING

* Add tests for `find_project_root` (PR #11).
