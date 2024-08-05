# BASE images v1.0.2

## MINOR CHANGES

* `base_r`: added `bit64` as a dependency.

# Base images v1.0.1

## MINOR CHANGES

* `base_python`: Added scanpy as a dependency.

* `base_r`: Added scanpy as a dependency.

# Base images v1.0.0

Initial release containing the following base images:

* `ghcr.io/openproblems-bio/base/python_3_10:1.0.0`, a Python 3.10 image with the following extra packages preinstalled:
  - Apt: `procps`
  - Python: `anndata~=0.8.0`, `mudata~=0.2.0`, `scanpy~=1.9.2`

* `ghcr.io/openproblems-bio/base/r2u_22_04:1.0.0`, an R2U 22.04 image with the following extra packages preinstalled:
  - Apt: `python3` and `procps`
  - Python: `anndata~=0.8.0`, `mudata~=0.2.0`, `scanpy~=1.9.2`
  - R: `anndata`