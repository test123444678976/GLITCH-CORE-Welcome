"""Read-only system information with an optional native C backend."""
from __future__ import annotations

import ctypes
import os
import platform
from pathlib import Path


def _load_native():
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
                pass
    return None


def _decode(value: bytes | None, fallback: str) -> str:
    return value.decode("utf-8", errors="replace") if value else fallback


def get_system_info() -> dict[str, str]:
    """Return display-safe, read-only information about this machine."""
    native = _load_native()
    kernel = platform.release()
    architecture = platform.machine() or "Unknown"
    memory = "Unknown"

    if native is not None:
        kernel = _decode(native.glitch_kernel_release(), kernel)
        architecture = _decode(native.glitch_machine(), architecture)
        total_mb = native.glitch_total_memory_mb()
        if total_mb > 0:
            memory = f"{total_mb:,} MB".replace(",", " ")

    if memory == "Unknown":
        try:
            for line in Path("/proc/meminfo").read_text(encoding="ascii").splitlines():
                if line.startswith("MemTotal:"):
                    kb = int(line.split()[1])
                    memory = f"{kb // 1024:,} MB".replace(",", " ")
                    break
        except (OSError, ValueError, IndexError):
            pass

    pretty_name = platform.system() or "Unknown"
    try:
        for line in Path("/etc/os-release").read_text(encoding="utf-8").splitlines():
            if line.startswith("PRETTY_NAME="):
                pretty_name = line.partition("=")[2].strip().strip('"')
                break
    except OSError:
        pass

    return {
        "operating_system": pretty_name,
        "kernel": kernel or "Unknown",
        "architecture": architecture,
        "memory": memory,
    }
