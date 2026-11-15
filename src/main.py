#!/usr/bin/env python3
"""GLITCH//CORE Welcome — first-run GTK 3 application."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from core.system_info import get_system_info

APP_VERSION = "0.2.0"
ROOT = Path(__file__).resolve().parents[1]


def format_system_info(info: dict[str, str]) -> str:
    """Format system information for the CLI and clipboard."""
    labels = (
        ("Operating system", "operating_system"),
        ("Kernel", "kernel"),
        ("Architecture", "architecture"),
        ("Installed memory", "memory"),
    )
    return "\n".join(f"{label}: {info[key]}" for label, key in labels)


def main() -> int:
    parser = argparse.ArgumentParser(description="GLITCH//CORE Welcome")
    parser.add_argument(
        "--version",
        action="version",
        version=f"GLITCH//CORE Welcome {APP_VERSION}",
    )
    parser.add_argument(
        "--system-info",
        action="store_true",
        help="print read-only system information and exit",
    )
    args = parser.parse_args()

    info = get_system_info()
    if args.system_info:
        print(format_system_info(info))
        return 0

    try:
        import gi
        gi.require_version("Gdk", "3.0")
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gdk, Gtk
    except (ImportError, ValueError) as exc:
        print(
            "GTK 3 / PyGObject is required to launch the graphical application.",
            file=sys.stderr,
        )
        print(f"Details: {exc}", file=sys.stderr)
        return 2

    class WelcomeWindow(Gtk.Window):
        def __init__(self):
            super().__init__(title="Welcome to GLITCH//CORE")
            self.set_default_size(760, 520)
            self.set_position(Gtk.WindowPosition.CENTER)
            self.connect("destroy", Gtk.main_quit)

            screen = Gdk.Screen.get_default()
            css_file = ROOT / "src" / "ui" / "style.css"
            if screen and css_file.is_file():
                provider = Gtk.CssProvider()
                provider.load_from_path(str(css_file))
                Gtk.StyleContext.add_provider_for_screen(
                    screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                )

            outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
            outer.set_border_width(28)
            outer.get_style_context().add_class("welcome-root")
            self.add(outer)

            brand = Gtk.Label(label="GLITCH//CORE")
            brand.set_xalign(0)
            brand.get_style_context().add_class("brand")
            outer.pack_start(brand, False, False, 0)

            title = Gtk.Label(label="Welcome to your new system.")
            title.set_xalign(0)
            title.set_line_wrap(True)
            title.get_style_context().add_class("welcome-title")
            outer.pack_start(title, False, False, 0)

            subtitle = Gtk.Label(
                label="A new beginning. Your system, your way."
            )
            subtitle.set_xalign(0)
            subtitle.get_style_context().add_class("subtitle")
            outer.pack_start(subtitle, False, False, 0)

            panel = Gtk.Grid(column_spacing=24, row_spacing=14)
            panel.set_margin_top(14)
            panel.get_style_context().add_class("info-panel")
            for row, (label, key) in enumerate((
                ("Operating system", "operating_system"),
                ("Kernel", "kernel"),
                ("Architecture", "architecture"),
                ("Installed memory", "memory"),
            )):
                name = Gtk.Label(label=label)
                name.set_xalign(0)
                name.get_style_context().add_class("info-label")

                value = Gtk.Label(label=info[key])
                value.set_xalign(0)
                value.set_selectable(True)
                value.set_line_wrap(True)
                value.set_max_width_chars(48)

                panel.attach(name, 0, row, 1, 1)
                panel.attach(value, 1, row, 1, 1)
            outer.pack_start(panel, True, True, 0)

            footer = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL, spacing=10
            )
            footer.set_halign(Gtk.Align.END)

            about = Gtk.Button(label="About")
            about.get_style_context().add_class("secondary-action")
            about.connect("clicked", self.show_about)
            footer.pack_start(about, False, False, 0)

            copy_button = Gtk.Button(label="Copy system info")
            copy_button.get_style_context().add_class("secondary-action")
            copy_button.connect("clicked", self.copy_system_info)
            footer.pack_start(copy_button, False, False, 0)

            done = Gtk.Button(label="Finish")
            done.get_style_context().add_class("suggested-action")
            done.connect("clicked", lambda _button: Gtk.main_quit())
            footer.pack_start(done, False, False, 0)
            outer.pack_end(footer, False, False, 0)

            version = Gtk.Label(label=f"GLITCH//CORE Welcome {APP_VERSION}")
            version.set_xalign(0)
            version.get_style_context().add_class("version")
            outer.pack_end(version, False, False, 0)

        def copy_system_info(self, _button):
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            clipboard.set_text(format_system_info(info), -1)

        def show_about(self, _button):
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=Gtk.DialogFlags.MODAL,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.CLOSE,
                text="GLITCH//CORE Welcome",
            )
            dialog.format_secondary_text(
                f"Version {APP_VERSION}\n"
                "A first-run application for GLITCH//CORE.\n"
                "Distributed under the MIT License."
            )
            dialog.run()
            dialog.destroy()

    window = WelcomeWindow()
    window.show_all()
    Gtk.main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
