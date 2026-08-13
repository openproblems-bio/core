# OpenProblems Base Images v1.2.0

## MAJOR CHANGES

* Rebuild `base_tensorflow_nvidia` on `python:3.12` with `tensorflow[and-cuda]` (PR #49).
  nvcr.io stopped publishing TensorFlow images after 25.02, which left the image stuck on
  TensorFlow 2.17, NumPy 1.26 and Scanpy 1.10. Taking CUDA from the `and-cuda` extra pins it
  to whatever the TensorFlow wheel was built against, so the two can no longer drift apart
  and silently fall back to the CPU.

* Bump TensorFlow from 2.17 to 2.21, NumPy from 1.26 to 2.x and Scanpy from 1.10 to 1.12 in
  `base_tensorflow_nvidia` (PR #49).

## BUG FIXES

* `base_tensorflow_nvidia`: put the CUDA libraries that the `and-cuda` extra installs under
  `site-packages/nvidia/*/lib` on the linker path with `ldconfig` (PR #49). TensorFlow does
  not look there by itself, so without this it reports `Cannot dlopen some GPU libraries`,
  finds no GPU and quietly trains on the CPU.

* `base_pytorch_nvidia`: drop the pip-installed `cmake` in favour of apt's (PR #48). The pip
  shims in `/usr/local/bin` shadow `/usr/bin/cmake`, and they fail with `ModuleNotFoundError:
  No module named 'cmake'` when a build calls them from inside a pip build isolation
  environment -- which broke, among others, building `louvain` for `cellplm`.

## TESTING

* Check that `cmake`, `cpack` and `ctest` resolve to the apt-provided binaries in
  `base_pytorch_nvidia` (PR #48).

* Check that the CUDA libraries are on the linker path in `base_tensorflow_nvidia` (PR #49).
  There is no GPU in CI, but the linker can be asked whether it would find them, which is
  enough to catch the failure above.

# OpenProblems Base Images v1.1.0

## MAJOR CHANGES

* Bump R base image from `rocker/r2u:22.04` to `rocker/r2u:24.04` (PR #25).
* Bump Python base image from `openproblems/base_python:3.11` to `openproblems/base_python:3.12` (PR #25).
* Bump AnnData dependency from 0.10 to 0.11 (PR #25).
* Bump Scanpy dependency from 1.10 to 1.11 (PR #25).
* Also create Major and Major.Minor versions for Docker images (PR #26).

## MINOR

* Log in to NVIDIA container registry to avoid rate limits (PR #28).

## TESTING

* Add tests for checking whether the installed packages are available in the base images (PR #25).

# OpenProblems Base Images v1.0.0

Relocated the base images from base_images repo to core repo.

## NEW FUNCTIONALITY

* Install the `openproblems` R and Python packages in the base images (PR #8).

## MAJOR CHANGES

* Change container registry from `ghcr.io/openproblems-bio/base_images` to docker hub `openproblems/base_*` (PR #5).

## BUG FIXES

* Bump to Viash 0.9.0 RC7 (PR #11).

* Update to Viash 0.9.4 (PR #24).
