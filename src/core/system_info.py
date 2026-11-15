"""Read-only system information with an optional native C backend."""
from __future__ import annotations

import ctypes
import platform
import shlex
from pathlib import Path


def _load_native():
    """Load the optional C library from a build tree or installed location."""
    root = Path(__file__).resolve().parents[2]
    candidates = (
        root / "libglitch_system.so",
        root / "build" / "libglitch_system.so",
    )
    for candidate in candidates:
        if candidate.is_file():
            try:
                lib = ctypes.CDLL(str(candidate))
                lib.glitch_kernel_release.restype = ctypes.c_char_p
                lib.glitch_machine.restype = ctypes.c_char_p
                lib.glitch_total_memory_mb.restype = ctypes.c_long
                return lib
            except (OSError, AttributeError):
                continue
    return None


def _decode(value: bytes | None, fallback: str) -> str:
    return value.decode("utf-8", errors="replace") if value else fallback


def _read_pretty_name() -> str:
    """Read PRETTY_NAME from os-release without assuming a fixed quote style."""
    try:
        lines = Path("/etc/os-release").read_text(encoding="utf-8").splitlines()
    except OSError:
        return platform.system() or "Unknown"

    for line in lines:
        if line.startswith("PRETTY_NAME="):
            raw_value = line.partition("=")[2]
            try:
                parsed = shlex.split(raw_value, comments=False, posix=True)
                return parsed[0] if parsed else "Unknown"
            except ValueError:
                return raw_value.strip().strip('"').strip("'") or "Unknown"
    return platform.system() or "Unknown"


def _read_memory_mb() -> int | None:
    """Read total memory from procfs when the native backend is unavailable."""
    try:
        for line in Path("/proc/meminfo").read_text(
            encoding="ascii"
        ).splitlines():
            if line.startswith("MemTotal:"):
                return int(line.split()[1]) // 1024
    except (OSError, ValueError, IndexError):
        return None
    return None


def _format_memory(total_mb: int) -> str:
    return f"{total_mb:,} MB".replace(",", " ")


def get_system_info() -> dict[str, str]:
    """Return display-safe, read-only information about this machine."""
    native = _load_native()
    kernel = platform.release() or "Unknown"
    architecture = platform.machine() or "Unknown"
    total_mb = 0

    if native is not None:
        kernel = _decode(native.glitch_kernel_release(), kernel)
        architecture = _decode(native.glitch_machine(), architecture)
        total_mb = native.glitch_total_memory_mb()

    if total_mb <= 0:
        total_mb = _read_memory_mb() or 0

    return {
        "operating_system": _read_pretty_name(),
        "kernel": kernel,
        "architecture": architecture,
        "memory": _format_memory(total_mb) if total_mb > 0 else "Unknown",
    }
