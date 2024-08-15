# openproblems core R v0.1.0

Initial release

## NEW FUNCTIONALITY

* Input/output:
  - `read_nested_yaml`: Read a nested YAML file

* Project:
  - `find_project_root`: Find the root of a Viash project
  - `read_viash_config`: Read a viash configuration file (PR #8).

* Utilities:
  - `strip_margin`: Strip margin from a string

## MINOR CHANGES

* Add dependencies to DESCRIPTION file (PR #8).

* `find_project_root`: simplify implementation (PR #9).

## TESTING

* Add tests for `find_project_root` (PR #9).
