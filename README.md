# pygel: Python GNU Econometrics Library

Lightweight C-accelerated library for econometric modelling which no longer has anything to do with GNU.

## Prerequisites
* **C Compiler** (gcc/clang)
* **Meson**
* **Ninja**

## Build the C Library
Core logic written in C and must be compiled into a shared library before the Python wrapper can be used:

```bash
# Setup the build
meson setup build

# Compile project
meson compile -C build
```



