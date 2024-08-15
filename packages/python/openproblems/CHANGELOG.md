# openproblems core Python v0.1.0

Initial release

## NEW FUNCTIONALITY

* `io`:
  - `read_nested_yaml`: Read a nested YAML file

* `project`:
  - `find_project_root`: Find the root of a Viash project
  - `read_viash_config`: Read a viash configuration file (PR #8).

* `utils`:
  - `strip_margin`: Strip margin from a string

## MINOR CHANGES

* Add dependencies to project toml file (PR #1).

* Clean up project toml file (PR #8).

## BUG FIXES

* Fix recursion bug in `find_project_root` (PR #11).

## TESTING

* Add tests for `find_project_root` (PR #11).
