# openproblems

[![PyPI](https://img.shields.io/pypi/v/openproblems)](https://pypi.org/project/openproblems/)
[![Python Versions](https://img.shields.io/pypi/pyversions/openproblems)](https://pypi.org/project/openproblems/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Core Python helper functions for [OpenProblems](https://openproblems.bio) benchmarking tasks.

## Installation

```bash
pip install openproblems
```

## Modules

### `openproblems.project`

Utilities for working with Viash projects.

- `find_project_root`: Find the root of a Viash project.
- `read_nested_yaml`: Read a nested YAML file.
- `read_viash_config`: Read a Viash configuration file.
- `resolve_path`: Resolve a path relative to a parent or project path.

#### `openproblems.project.component_tests`

Helpers for writing component tests.

- `run_check_config` / `check_config`: Validate a component's Viash configuration.
- `run_and_check_output`: Run a component and validate its output files against format specs.

#### `openproblems.project.docs`

Utilities for generating task documentation.

- `read_task_config`: Read a task-level configuration file.
- `read_task_metadata`: Read and assemble full task metadata.
- `read_component_spec`: Read a component API specification.
- `read_file_format`: Read a file format specification.
- `render_task_readme_qmd`: Render a Quarto README for a task.
- `render_component_spec`: Render a component specification as Markdown.
- `render_file_format`: Render a file format specification as Markdown.

### `openproblems.utils`

General-purpose utilities.

- `strip_margin`: Strip leading margin characters from a multiline string.
- `deep_merge`: Recursively merge two dictionaries.

## Links

- **Documentation**: <https://openproblems.bio/documentation>
- **Repository**: <https://github.com/openproblems-bio/core>
- **Issue tracker**: <https://github.com/openproblems-bio/core/issues>
