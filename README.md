# GLITCH//CORE Welcome

The first-run welcome application for the GLITCH//CORE operating system.

## Status

**Version:** 0.2.0 — early development.

This repository contains a GTK 3 desktop application, a small optional native
C backend, automated tests and a GitHub Actions CI workflow. It is not yet
integrated into a GLITCH//CORE image.

The current GLITCH//CORE rescue ISO is still a BusyBox-based prototype. It
does not include GTK 3, PyGObject, Xorg or MATE. Welcome can be tested on a
Linux desktop now and integrated into the distribution when its graphical
userspace is ready.

## Features

- GLITCH//CORE-themed first-run window built with GTK 3
- Read-only operating-system, kernel, architecture and memory information
- Optional native C backend with a Python standard-library fallback
- Copy system information to the clipboard
- About dialog and application version
- Headless `--version` and `--system-info` commands
- Desktop entry and staged installation support
- No administrator operations and no automatic system changes

## Requirements

- Linux
- Python 3.10 or newer
- GTK 3 and PyGObject
- A C compiler and Make (only needed to build/install the optional native backend)

On Ubuntu 24.04 or 26.04, install the dependencies with:

```sh
sudo apt update
sudo apt install -y python3 python3-gi gir1.2-gtk-3.0 build-essential make desktop-file-utils
```

## Build and run

From the repository root:

```sh
make
make test
make check
make run
```

The graphical window requires a Linux graphical session. WSL2 users need WSLg
(or another working X11/Wayland display connection) for `make run`.

Headless information commands do not need GTK to open a window:

```sh
python3 src/main.py --version
python3 src/main.py --system-info
```

## Install

To install into the system (default prefix: `/usr`):

```sh
sudo make install
```

To create a package staging tree without changing the host system:

```sh
make DESTDIR=/tmp/glitch-welcome-stage install
```

The installed launcher is `glitch-welcome`. The desktop entry is installed
under `share/applications`.

## Project layout

- `src/main.py` — GTK 3 interface and command-line entry point
- `src/core/system.c`, `system.h` — read-only native system information
- `src/core/system_info.py` — Python API and fallback implementation
- `src/ui/style.css` — application styling
- `tests/` — automated tests
- `packaging/` — desktop entry and provisional GLITCH package metadata
- `.github/workflows/ci.yml` — build, test and packaging checks

## Package metadata

`packaging/glitch-app.json` is a provisional project manifest. Its
`gcpkg-app-v1` format must be checked against the eventual GLITCH//CORE
package-manager specification before it is treated as an installable package.

## Safety and permissions

Welcome only reads system information. It does not run shell commands, request
administrator privileges, install software, edit system files or change system
settings. The Finish button closes the window; it does not claim to complete
system configuration.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE).
