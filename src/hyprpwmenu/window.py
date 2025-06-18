from ctypes import CDLL
from hyprpwmenu.constants import APP_NAME, DEFAULT_STYLE_FILE
from hyprpwmenu.util import printLog
from hyprpwmenu.config import AppConfig
from typing import List

CDLL("libgtk4-layer-shell.so")

import gi  # pyright: ignore # noqa

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")

from gi.repository import Gtk, Gdk, Gtk4LayerShell  # pyright: ignore # noqa


class Window:
    buttons: List[Gtk.Button]
    currentFocusIndex = 0

    def __init__(self) -> None:
        # Create the GTK application
        printLog("Initializing GTK application...")
        self.app = Gtk.Application(application_id=f"com.antrax.{APP_NAME}")
        self.app.connect("activate", self.on_activate)
        self.appConfig = AppConfig()

        printLog("Initializing button list...")
        self.buttons = []

    def on_key_pressed(self, controller, keyval, keycode, state) -> bool:
        """Handler for key press events"""
        printLog(f"Key pressed: keyval={keyval}, keycode={keycode}")

        # Check if 'q' key is pressed
        if keyval == Gdk.KEY_q:
            printLog("Key 'q' pressed - Exiting...")
            self.app.quit()
            return True
        # Check if ESC key is pressed
        elif keyval == Gdk.KEY_Escape:
            printLog("ESC key pressed - Exiting...")
            self.app.quit()
            return True

        elif keyval == Gdk.KEY_Right:
            printLog("Right arrow key pressed")
            self.currentFocusIndex += 1
            if self.currentFocusIndex >= len(self.buttons):
                self.currentFocusIndex = 0

            self.buttons[self.currentFocusIndex].grab_focus()
            self.buttons[self.currentFocusIndex].set_state_flags(
                Gtk.StateFlags.FOCUSED, False
            )
            self.updateHintLabel()

            return True

        elif keyval == Gdk.KEY_Left:
            printLog(f"Left arrow key pressed")
            self.currentFocusIndex -= 1

            printLog(f"New focus index: {self.currentFocusIndex}")
            if self.currentFocusIndex < 0:
                self.currentFocusIndex = len(self.buttons) - 1

            self.buttons[self.currentFocusIndex].grab_focus()
            self.buttons[self.currentFocusIndex].set_state_flags(
                Gtk.StateFlags.FOCUSED, False
            )
            self.updateHintLabel()

            return True

        return False

    def onMouseEnter(
        self,
        controller: Gtk.EventControllerMotion,
        x: float,
        y: float,
        button: Gtk.Button,
    ) -> None:
        """Handler for mouse enter event - gives focus to button"""
        printLog(f"Mouse entered button: {button.get_name()}")
        button.grab_focus()

        # Update currentFocusIndex to match the focused button
        try:
            self.currentFocusIndex = self.buttons.index(button)
            printLog(f"Updated focus index to: {self.currentFocusIndex}")
            self.updateHintLabel()
        except ValueError:
            printLog("Warning: Button not found in buttons list")

    def updateHintLabel(self) -> None:
        self.hintLabel.set_label(self.appConfig.buttons[self.currentFocusIndex].hint)

    def onMouseLeave(
        self, controller: Gtk.EventControllerMotion, button: Gtk.Button
    ) -> None:
        """Handler for mouse leave event"""
        printLog(f"Mouse left button: {button.get_name()}")
        # Optionally, you can implement logic here if needed
        # For now, we keep the focus to maintain keyboard navigation

    def onMouseClick(self, button: Gtk.Button) -> None:
        """Handler for mouse click event"""
        printLog(f"Mouse clicked button: {button.get_name()}")

    def on_activate(self, app) -> None:
        # Create the main window
        printLog("Creating main window...")
        window = Gtk.ApplicationWindow(application=app)
        window.set_title(f"{APP_NAME}")

        # Initialize GTK4 Layer Shell for the window
        printLog("Initializing GTK4 Layer Shell...")
        Gtk4LayerShell.init_for_window(window)

        printLog("Creating main box...")
        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        printLog("Creating top and bottom boxes...")
        topBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        bottomBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        mainBox.append(topBox)
        mainBox.append(bottomBox)

        printLog("Configuring main boxes alignment...")
        mainBox.set_halign(Gtk.Align.CENTER)
        mainBox.set_valign(Gtk.Align.CENTER)
        topBox.set_halign(Gtk.Align.CENTER)
        topBox.set_valign(Gtk.Align.CENTER)
        bottomBox.set_halign(Gtk.Align.CENTER)
        bottomBox.set_valign(Gtk.Align.CENTER)

        printLog("Adding main box to the window...")
        window.set_child(mainBox)

        printLog("Adding buttons to the main box...")
        for b in self.appConfig.buttons:
            topBox.append(self.makeButton(icon_path=b.icon_path, id=b.id))

        self.hintLabel = Gtk.Label(label=self.appConfig.buttons[0].hint)
        self.hintLabel.set_name("hint_label")
        bottomBox.append(self.hintLabel)

        # Configure the layer (overlay layer to stay above other windows)
        printLog("Configuring layer...")
        Gtk4LayerShell.set_layer(window, Gtk4LayerShell.Layer.OVERLAY)

        # Configure keyboard interactivity - IMPORTANT!
        printLog("Setting keyboard interactivity...")
        Gtk4LayerShell.set_keyboard_mode(window, Gtk4LayerShell.KeyboardMode.EXCLUSIVE)

        # Anchor the window in the center of the screen
        printLog("Anchoring window in the center of the screen...")
        Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.TOP, False)
        Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.BOTTOM, False)
        Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.LEFT, False)
        Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.RIGHT, False)

        # Create and configure the key event controller
        printLog("Setting up key event controller...")
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.on_key_pressed)
        window.add_controller(key_controller)

        # Add CSS style for better appearance
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(f"{DEFAULT_STYLE_FILE}")
        display = window.get_display()
        Gtk.StyleContext.add_provider_for_display(
            display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        printLog("CSS provider loaded")

        # Connect close event
        window.connect("close-request", self.on_close)

        # Connect to the "realize" signal of the window
        # This ensures the window and its children are fully drawn before we try to set focus
        window.connect("realize", self.onWindowRealize)

        # Show the window and grab focus
        window.present()

    def onWindowRealize(self, window) -> None:
        """
        Callback executed when the window is fully realized (drawn on screen).
        This is the ideal place to set initial focus.
        """
        # Request focus for the first button
        printLog("Requesting focus for the first button...")
        self.buttons[self.currentFocusIndex].grab_focus()

    def makeButton(self, icon_path: str, id: str) -> Gtk.Button:
        # Criar a imagem a partir do arquivo PNG
        image = Gtk.Image.new_from_file(icon_path)

        # Create the button
        button = Gtk.Button.new()
        button.set_child(image)  # Set the configured label as the button's child
        button.set_name(
            id
        )  # Use set_name for the widget ID, not set_id (deprecated/internal)

        # Add motion controller for hover effects
        motionController = Gtk.EventControllerMotion()
        motionController.connect(
            "enter",
            lambda controller, x, y: self.onMouseEnter(controller, x, y, button),
        )
        motionController.connect(
            "leave", lambda controller: self.onMouseLeave(controller, button)
        )
        button.add_controller(motionController)

        self.buttons.append(button)
        button.connect("clicked", self.onMouseClick)
        button.set_tooltip_text(self.appConfig.buttons[self.currentFocusIndex].hint)

        return button

    def on_close(self, window) -> bool:
        self.app.quit()
        return False

    def run(self) -> int:
        return self.app.run([])


if __name__ == "__main__":
    gonha_window = Window()
    gonha_window.run()
