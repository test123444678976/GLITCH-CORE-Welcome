#!/usr/bin/env python3
"""GLITCH//CORE Welcome — first-run GTK 3 application."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from core.system_info import get_system_info

APP_VERSION = "0.1.0"
ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="GLITCH//CORE Welcome")
    parser.add_argument("--version", action="version", version=f"GLITCH//CORE Welcome {APP_VERSION}")
    args = parser.parse_args()

    try:
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk, Gdk
    except (ImportError, ValueError) as exc:
        print("GTK 3 / PyGObject is required to launch the graphical application.", file=sys.stderr)
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

            brand = Gtk.Label()
            brand.set_markup('<span size="small" foreground="#a8b4d6">GLITCH//CORE</span>')
            brand.set_xalign(0)
            outer.pack_start(brand, False, False, 0)

            title = Gtk.Label()
            title.set_markup('<span size="xx-large" weight="bold">Welcome to your new system.</span>')
            title.set_xalign(0)
            outer.pack_start(title, False, False, 0)

            subtitle = Gtk.Label(label="A new beginning. Your system, your way.")
            subtitle.set_xalign(0)
            subtitle.get_style_context().add_class("subtitle")
            outer.pack_start(subtitle, False, False, 0)

            info = get_system_info()
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
                panel.attach(name, 0, row, 1, 1)
                panel.attach(value, 1, row, 1, 1)
            outer.pack_start(panel, True, True, 0)

            footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            footer.set_halign(Gtk.Align.END)
            done = Gtk.Button(label="Finish")
            done.get_style_context().add_class("suggested-action")
            done.connect("clicked", lambda _button: Gtk.main_quit())
            footer.pack_end(done, False, False, 0)
            outer.pack_end(footer, False, False, 0)

    window = WelcomeWindow()
    window.show_all()
    Gtk.main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
