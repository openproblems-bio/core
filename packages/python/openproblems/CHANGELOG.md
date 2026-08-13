# openproblems core Python v0.2.0

## NEW FUNCTIONALITY

* `project`:
  - `resolve_path`: Resolve a path relative to a parent path or project root.

* `project.component_tests`:
  - `check_config`: Validate a component's Viash config (namespace, type, metadata, normalization, variants, Nextflow runner).
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

* `check_config`: Skip the Nextflow resource label check for components whose script is itself a Nextflow workflow. Viash renders those as a workflow rather than a process, so the labels would have no effect.

## BUG FIXES

* `read_task_metadata`: Order the task graph topologically instead of by a breadth-first search from a single root.
  Tasks with more than one raw dataset no longer strand all but the first at the end of the README,
  and a component is never documented before the files it consumes.

* `render_component_spec`: Include non-file arguments (e.g. `--seed`) in the arguments table,
  and fall back to an argument's `description` when it has no `summary`.

* `resolve_path`: Resolve a path starting with a `/` relative to the project root, the way
  Viash does. `os.path.join()` treats such a path as absolute and silently dropped the project
  root, so a config containing e.g. `__merge__: /src/api/file_dataset.yaml` failed to read.

* `deep_merge`: Preserve the order of the keys. Since the merged keys were collected in a `set()`
  and Python randomises string hashing per process, `read_nested_yaml` returned its keys in a
  different order on every run, and a rendered task README differed from one run to the next.

* `render_file_format`: Render file formats of type `tabular`. `read_file_format` accepts them,
  but the renderer only knew about `csv`, `tsv` and `parquet`, so the Format and Data structure
  sections came out empty.
  
* `check_config`: Check the required links even when a component defines no links at all.
  `check_links` returned early on an empty `links`, so a method without any links passed,
  while a method with only a `documentation` link was told that `.links.repository` is missing.

* `check_config`: Give `check_url` a 30 second timeout, and report a request that fails outright
  as an unreachable link rather than letting the exception escape.

* `check_config`: Escape the dot in the DOI regex, which also matched a prefix like `10X1038`.

* `run_and_check_output`: Skip the format validation of an output file argument that has no
  value. An optional output without a default or example crashed with a `KeyError: 'value'`.

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
