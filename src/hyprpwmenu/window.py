from ctypes import CDLL

CDLL("libgtk4-layer-shell.so")

#!/usr/bin/env python3
import gi  # pyright: ignore # noqa

gi.require_version("Gtk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")

from gi.repository import Gtk, Gtk4LayerShell, GLib  # pyright: ignore # noqa
from hyprpwmenu.constants import APP_NAME, DEFAULT_STYLE_FILE  # pyright: ignore # noqa


class Window:
    def __init__(self):
        # Criar a aplicação GTK
        self.app = Gtk.Application(application_id=f"com.example.{APP_NAME}")
        self.app.connect("activate", self.on_activate)

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
        css_provider.load_from_data(b"""
            window {
                background-color: rgba(0, 0, 0, 1.0);
                border-radius: 10px;
            }
            label {
                color: white;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
        """)

        # Aplicar o CSS
        style_context = window.get_style_context()
        style_context.add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Adicionar o label à janela
        window.set_child(label)

        # Conectar evento de fechamento
        window.connect("close-request", self.on_close)

        # Mostrar a janela
        window.present()

        # Fechar automaticamente após 3 segundos (opcional)
        # GLib.timeout_add_seconds(3, lambda: window.close())

    def on_close(self, window):
        self.app.quit()
        return False

    def run(self):
        return self.app.run()


if __name__ == "__main__":
    gonha_window = Window()
    gonha_window.run()
