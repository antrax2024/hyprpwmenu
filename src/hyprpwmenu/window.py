"""
Main Window Module for HyprPwMenu

This module implements the main GTK4 window interface for the HyprPwMenu application.
It uses GTK4 Layer Shell to create an overlay window with power menu buttons and
handles user interactions through keyboard and mouse events.

Classes:
    Window: Main application window class managing the GUI interface

Dependencies:
    - ctypes: For loading the GTK4 Layer Shell library
    - gi.repository: GTK4, GDK4, and GTK4LayerShell for GUI components
    - hyprpwmenu.config: Configuration management
    - hyprpwmenu.util: Utility functions for logging and command execution

Features:
    - Overlay window using GTK4 Layer Shell
    - Keyboard navigation with arrow keys and ESC/Q for exit
    - Mouse hover effects and click handling
    - Dynamic button creation from configuration
    - CSS styling support
    - System command execution for power operations
"""

from ctypes import CDLL
import os
from hyprpwmenu.constants import APP_NAME, DEFAULT_STYLE_FILE
from hyprpwmenu.util import printLog, executeCommand
from hyprpwmenu.config import AppConfig
from typing import List

CDLL("libgtk4-layer-shell.so")

import gi  # pyright: ignore # noqa

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")

from gi.repository import Gtk, Gdk, Gtk4LayerShell  # pyright: ignore # noqa


class Window:
    """
    Main window class for the HyprPwMenu application.

    This class manages the GTK4 window interface, handles user interactions,
    and coordinates between the GUI and system commands. It uses GTK4 Layer Shell
    to create an overlay window that stays above other applications.

    Attributes:
        buttons (List[Gtk.Button]): List of power menu buttons
        currentFocusIndex (int): Index of currently focused button
        app (Gtk.Application): GTK4 application instance
        appConfig (AppConfig): Application configuration loaded from YAML
        hintLabel (Gtk.Label): Label displaying button hints/tooltips

    Methods:
        __init__: Initialize the window and GTK application
        on_activate: Callback for GTK application activation
        on_key_pressed: Handle keyboard input events
        onMouseEnter: Handle mouse enter events on buttons
        onMouseLeave: Handle mouse leave events on buttons
        onMouseClick: Handle button click events
        makeButton: Create a button from configuration
        updateHintLabel: Update the hint label text
        onWindowRealize: Handle window realization event
        on_close: Handle window close event
        run: Start the GTK application main loop
    """

    buttons: List[Gtk.Button]
    currentFocusIndex = 0

    def __init__(self) -> None:
        """
        Initialize the Window instance and GTK application.

        Creates the GTK application, loads configuration, and initializes
        the button list. Sets up the application ID and connects activation callback.

        Side Effects:
            - Creates GTK application instance
            - Loads AppConfig from YAML file
            - Initializes empty button list
            - Logs initialization steps
        """
        # Create the GTK application
        printLog("Initializing GTK application...")
        self.app = Gtk.Application(application_id=f"com.antrax.{APP_NAME}")
        self.app.connect("activate", self.on_activate)
        self.appConfig = AppConfig()

        printLog("Initializing button list...")
        self.buttons = []

    def on_key_pressed(self, controller, keyval, keycode, state) -> bool:
        """
        Handle keyboard input events for window navigation and control.

        Processes key presses for navigation (arrow keys) and application control
        (ESC, Q for quit). Updates focus and hint labels accordingly.

        Args:
            controller: GTK event controller instance
            keyval: Key value identifier from GDK
            keycode: Hardware key code
            state: Modifier state flags

        Returns:
            bool: True if event was handled, False otherwise

        Key Mappings:
            - Right Arrow: Move focus to next button (wraps around)
            - Left Arrow: Move focus to previous button (wraps around)
            - Q/Escape: Quit the application
        """
        printLog(f"Key pressed: keyval={keyval}, keycode={keycode}")

        if keyval == Gdk.KEY_q:
            printLog("Key 'q' pressed - Exiting...")
            self.app.quit()
            return True
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
        """
        Handle mouse enter events on buttons.

        Updates focus when mouse cursor enters a button area and updates
        the current focus index to match the hovered button.

        Args:
            controller: GTK motion event controller
            x: Mouse cursor X coordinate
            y: Mouse cursor Y coordinate
            button: The button that received mouse enter event

        Side Effects:
            - Sets focus to the hovered button
            - Updates currentFocusIndex
            - Updates hint label text
            - Logs mouse enter event
        """
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
        """
        Update the hint label text based on current button focus.

        Retrieves the hint text from the currently focused button's configuration
        and updates the hint label display.

        Side Effects:
            - Updates hintLabel text content
        """
        self.hintLabel.set_label(self.appConfig.buttons[self.currentFocusIndex].hint)

    def onMouseLeave(
        self, controller: Gtk.EventControllerMotion, button: Gtk.Button
    ) -> None:
        """
        Handle mouse leave events on buttons.

        Currently logs the mouse leave event for debugging purposes.
        Can be extended for additional mouse leave behaviors.

        Args:
            controller: GTK motion event controller
            button: The button that received mouse leave event
        """
        printLog(f"Mouse leave button: {button.get_name()}")

    def onMouseClick(self, button: Gtk.Button) -> None:
        """
        Handle button click events and execute associated commands.

        Executes the system command associated with the currently focused button
        as defined in the application configuration.

        Args:
            button: The button that was clicked

        Side Effects:
            - Executes system command via executeCommand utility
            - Logs button click event
        """
        printLog(f"Mouse clicked button: {button.get_name()}")
        executeCommand(self.appConfig.buttons[self.currentFocusIndex].command)

    def on_activate(self, app) -> None:
        """
        Callback function executed when the GTK application is activated.

        This function is the main initialization point for the GUI interface.
        It creates and configures the main window, sets up GTK4 Layer Shell,
        creates buttons from configuration, and handles window styling.

        Args:
            app: The GTK4 application instance

        Side Effects:
            - Creates main application window
            - Initializes GTK4 Layer Shell with overlay layer
            - Creates button interface from configuration
            - Loads CSS styling
            - Sets up keyboard and mouse event handlers
            - Displays the window on screen
        """
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

        This is the ideal place to set initial focus as it ensures the window
        and its children are fully drawn before attempting to set focus.

        Args:
            window: The GTK window that was realized

        Side Effects:
            - Sets focus to the first button in the list
            - Logs the focus request action
        """
        # Request focus for the first button
        printLog("Requesting focus for the first button...")
        self.buttons[self.currentFocusIndex].grab_focus()

    def makeButton(self, icon_path: str, id: str) -> Gtk.Button:
        """
        Create a GTK button from configuration parameters.

        This method creates a button with an icon image, sets up event controllers
        for mouse interactions, and configures the button properties according
        to the application configuration.

        Args:
            icon_path: Absolute path to the PNG icon file
            id: CSS identifier for styling the button

        Returns:
            Gtk.Button: Configured button ready for display

        Side Effects:
            - Creates GTK Image from file
            - Adds button to internal buttons list
            - Sets up motion event controllers
            - Connects click event handler
            - Sets tooltip text
        """
        # Create image from PNG file
        image = Gtk.Image.new_from_file(os.path.expanduser(icon_path))

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
        """
        Handle window close event.

        Properly terminates the GTK application when the window is closed.

        Args:
            window: The GTK window being closed

        Returns:
            bool: False to allow the window to close

        Side Effects:
            - Calls self.app.quit() to terminate the application
        """
        self.app.quit()
        return False

    def run(self) -> int:
        """
        Start the GTK application main loop.

        This method starts the application and returns when it exits.
        It serves as the main entry point for running the GUI.

        Returns:
            int: Exit code from the GTK application (typically 0 for success)

        Example:
            >>> window = Window()
            >>> exit_code = window.run()
            >>> print(f"Application exited with code: {exit_code}")
        """
        return self.app.run([])


if __name__ == "__main__":
    gonha_window = Window()
    gonha_window.run()
