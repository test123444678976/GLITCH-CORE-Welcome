# GLITCH//CORE Welcome

The official first-run welcome application for GLITCH//CORE.

## Current status

Early development (0.1.0). This repository contains a GTK 3 application prototype,
a small optional C system-information backend, tests and CI. It is **not yet
integrated into a GLITCH//CORE image**.

The current GLITCH//CORE rescue ISO is a BusyBox-based prototype and does not
ship GTK 3, PyGObject, Xorg or MATE. Run this application on a Linux desktop
with GTK 3 and PyGObject installed, or integrate it after the graphical
GLITCH//CORE userspace is available.

## Features

- First-run welcome screen with GLITCH//CORE visual styling
- Read-only OS, kernel, architecture and memory information
- Optional native C backend (Python fallback remains available)
- Accessible GTK navigation and a setup-complete action
- No privileged operations and no changes to system configuration

## Development

Dependencies (Debian/Ubuntu example):

```sh
sudo apt install python3 python3-gi gir1.2-gtk-3.0 build-essential
make
make run
```

The C backend is optional. Build it with `make`; without the shared library,
the app uses its Python standard-library fallback.

Run checks:

```sh
make test
make check
```

## Project layout

- `src/main.py` — GTK 3 application and CLI
- `src/core/system.c`, `system.h` — safe read-only native system information
- `src/core/system_info.py` — Python interface and fallback
- `src/ui/style.css` — application styling
- `tests/` — automated tests
- `packaging/` — desktop entry and GLITCH package metadata

## Safety and permissions

The application only reads system information. It does not run shell commands,
request administrator privileges, install software, or edit system files.
