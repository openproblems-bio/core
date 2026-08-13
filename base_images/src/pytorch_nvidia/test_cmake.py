import shutil
import subprocess
import tempfile

## VIASH START
meta = {
    "temp_dir": tempfile.gettempdir(),
}
## VIASH END

# The nvcr pytorch image ships a pip-installed cmake whose shims land in
# /usr/local/bin and shadow apt's cmake. If a base image rebuild ever
# reintroduces them, components that compile from source break in confusing
# ways, so check that cmake resolves to the apt-provided binary and runs.
print("--- Checking cmake ---", flush=True)

cmake = shutil.which("cmake")
print(f"cmake resolves to: {cmake}", flush=True)

assert cmake is not None, "cmake not found on PATH"
assert cmake == "/usr/bin/cmake", (
    f"expected apt's /usr/bin/cmake on PATH, got {cmake} -- a pip-installed "
    "cmake is probably shadowing it"
)

out = subprocess.run([cmake, "--version"], capture_output=True, text=True)
print(out.stdout.strip(), flush=True)

assert out.returncode == 0, f"`cmake --version` exited {out.returncode}: {out.stderr.strip()}"

# The pip package ships cpack and ctest alongside cmake; removing only the
# cmake shim would leave those two broken.
for tool in ["cpack", "ctest"]:
    path = shutil.which(tool)
    print(f"{tool} resolves to: {path}", flush=True)
    assert path is None or path.startswith("/usr/bin/"), (
        f"{tool} resolves to {path}, expected /usr/bin/{tool} or nothing"
    )

print("\ncmake test passed!", flush=True)
