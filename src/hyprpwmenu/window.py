from ctypes import CDLL
import signal
import sys
from hyprpwmenu.constants import APP_NAME, DEFAULT_STYLE_FILE
from hyprpwmenu.util import printLog

CDLL("libgtk4-layer-shell.so")

import gi  # pyright: ignore # noqa

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")

from gi.repository import Gtk, Gtk4LayerShell  # pyright: ignore # noqa


class Window:
    def __init__(self):
        # Criar a aplicação GTK
        self.app = Gtk.Application(application_id=f"com.example.{APP_NAME}")
        self.app.connect("activate", self.on_activate)

        # Configurar manipulador de sinal para SIGINT (Ctrl+C)
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Manipulador para SIGINT (Ctrl+C)"""
        printLog("Exiting...")
        if hasattr(self, "app"):
            self.app.quit()
        sys.exit(0)

    def on_activate(self, app):
        # Criar a janela principal
        window = Gtk.ApplicationWindow(application=app)
        window.set_title(f"{APP_NAME}")

        # Inicializar o GTK4 Layer Shell para a janela
        Gtk4LayerShell.init_for_window(window)

        # Configurar a camada (overlay layer para ficar acima de outras janelas)
        Gtk4LayerShell.set_layer(window, Gtk4LayerShell.Layer.OVERLAY)

        # Ancorar a janela no centro da tela
        Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.TOP, False)
        Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.BOTTOM, False)
        Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.LEFT, False)
        Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.RIGHT, False)

        # Definir tamanho fixo para a janela
        window.set_default_size(300, 150)

        # Criar o label com a palavra "gonha"
        label = Gtk.Label()
        label.set_markup('<span font_size="xx-large" weight="bold">gonha</span>')
        label.set_halign(Gtk.Align.CENTER)
        label.set_valign(Gtk.Align.CENTER)

        # Adicionar estilo CSS para melhor aparência
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(f"{DEFAULT_STYLE_FILE}")
        display = window.get_display()
        Gtk.StyleContext.add_provider_for_display(
            display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        printLog("CSS provider loaded")  # Adicionar o label à janela
        window.set_child(label)

        # Conectar evento de fechamento
        window.connect("close-request", self.on_close)

        # Mostrar a janela
        window.present()

    def on_close(self, window):
        self.app.quit()
        return False

    def run(self):
        return self.app.run([])


if __name__ == "__main__":
    gonha_window = Window()
    gonha_window.run()
