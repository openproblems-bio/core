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
