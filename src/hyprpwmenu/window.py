from ctypes import CDLL

CDLL("libgtk4-layer-shell.so")
import gi  # pyright: ignore # noqa

gi.require_version("Gtk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
