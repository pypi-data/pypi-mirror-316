# All OSes build for CPython 3.8, CPython 3.9, CPython 3.10, CPython 3.11, CPython 3.12, CPython 3.13, CPython 3.13t, PyPy 3.9, PyPy 3.10

### Source distribution
maturin sdist

### Linux
# - aarch64-unknown-linux-gnu
# - i686-unknown-linux-gnu
# - x86_64-unknown-linux-gnu
# Add Rust targets
rustup target add aarch64-unknown-linux-gnu i686-unknown-linux-gnu x86_64-unknown-linux-gnu
# Build wheels
maturin build --release --target aarch64-unknown-linux-gnu --compatibility manylinux2014 --auditwheel repair --find-interpreter --zig --quiet
maturin build --release --target i686-unknown-linux-gnu    --compatibility manylinux2014 --auditwheel repair --find-interpreter --zig --quiet
maturin build --release --target x86_64-unknown-linux-gnu  --compatibility manylinux2014 --auditwheel repair --find-interpreter --zig --quiet

### macOS
# - aarch64-apple-darwin
# - x86_64-apple-darwin
# Add Rust targets
rustup target add aarch64-apple-darwin x86_64-apple-darwin
# Build wheels
maturin build --release --target aarch64-apple-darwin --compatibility manylinux2014 --auditwheel repair --find-interpreter --zig --quiet
maturin build --release --target x86_64-apple-darwin  --compatibility manylinux2014 --auditwheel repair --find-interpreter --zig --quiet

### Windows
# - x86_64-pc-windows-msvc
# Add Rust target
rustup target add x86_64-pc-windows-msvc
# Install LLVM for llvm-dlltool
sudo apt install llvm -y
# Force use of cargo-xwin for building
export MATURIN_USE_XWIN=1
# Build wheels
maturin build --release --target x86_64-pc-windows-msvc --compatibility manylinux2014 --auditwheel repair --find-interpreter --quiet
