# oead

**oead** is a C++ library for common file formats used in modern first-party Nintendo EAD (now EPD) titles.

Python bindings for Python 3.9+ are also available.

## Features

oead handles common formats used in recent games such as *Breath of the Wild* and *Super Mario Odyssey*.

- [AAMP](https://zeldamods.org/wiki/AAMP) (binary parameter archive): only version 2 is supported.
- [BYML](https://zeldamods.org/wiki/BYML) (binary YAML): versions 1-10 are supported, including 32-bit and 64-bit hash nodes and monotyped arrays. Remapped container nodes and non-container root nodes are not supported.
- [SARC](https://zeldamods.org/wiki/SARC) (archive).
- [Yaz0](https://zeldamods.org/wiki/Yaz0) (compression algorithm).

oead also supports a recent Grezzo format used in *Link's Awakening (Switch)*:

- [gsheet](https://zeldamods.org/las/Datasheet) (Grezzo datasheet).

## Getting Started

To install the Python module, run:

```bash
py -3.14 -m pip install --upgrade -r https://cobra838.github.io/oead/latest.txt

or

py -3.14 -m pip install --upgrade --index-url https://cobra838.github.io/oead/simple/ oead
```

This downloads a precompiled wheel for:

- Windows (x86-64 / 64-bit).
- Recent Linux distributions (x86-64, glibc and musl).
- macOS 10.14+ (x86-64 / arm64).

Supported Python versions:

- CPython 3.9 to 3.14.

If your platform is not listed, build oead from source.

> **Warning**
> Windows users must install the [latest Visual C++ Redistributable](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads).

For more information, see the [documentation](https://oead.readthedocs.io/).

## Building From Source

Building oead from source requires:

- Python 3.9-3.14
- CMake 3.12+.
- Ninja 1.13
- A compiler with C++17 support.

Tested versions:

```bash
uv run python --version
# Python 3.14.6

cmake --version
# cmake version 4.0.3

ninja --version
# 1.13.2

Visual Studio version
# Microsoft Visual Studio\2022\Community
```

Clone the repository, cd to `oead` directory, and initialize submodules:

```bash
git submodule update --init --recursive
```

### Building The Python Module

Use [uv](https://github.com/astral-sh/uv) to create a CPython 3.14 environment and install the application and build dependencies:

```bash
uv venv --python 3.14 .venv
call .venv\Scripts\activate
uv pip install setuptools wheel
```

#### Ninja Build

Install Ninja if necessary:

```bash
winget install --id Ninja-build.Ninja --exact
```

Open an `x64 Native Tools Command Prompt for Visual Studio`, then activate the venv as above. In that prompt `cl.exe` is available, so the build automatically uses Ninja:

```bash
python setup.py bdist_wheel

# -- Building for: Ninja
```

#### Visual Studio Build

Run the commands above in a regular `cmd.exe` session, then build the wheel:

```bash
python setup.py bdist_wheel

# -- Building for: Visual Studio 17 2022
```

#### Install The Built Wheel

With the venv still activated, install the compatible wheel from `dist`:

```bash
uv pip install --force-reinstall --no-index --find-links dist oead
```

## C++ Usage

Linking to the `oead` target is sufficient to use the library.

## Contributing

- [Issue tracker](https://github.com/zeldamods/oead/issues).
- [Source code](https://github.com/zeldamods/oead).

This project is licensed under the GPLv2+ license.
