# Contributing

Thanks for helping improve GLITCH//CORE Welcome.

## Before opening a change

1. Keep the application read-only. Do not add privileged operations or silent
   changes to the host system.
2. Keep GTK imports inside the graphical startup path so CLI checks work
   without opening a display.
3. Preserve the Python fallback when changing the optional C backend.
4. Add or update tests for behavior changes.
5. Run `make clean all test check` before submitting.
6. Validate the desktop entry with `desktop-file-validate` when available.

## Scope

Welcome is the first-run desktop application, not the GLITCH//CORE installer
or package manager. Package metadata remains provisional until the native
GLITCH package format is specified.
