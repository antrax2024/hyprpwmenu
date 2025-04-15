# -*- coding: utf-8 -*-
"""
Simple Power Menu application
"""
import os
import sys
import qtawesome as qta
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QToolButton
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QKeyEvent, QIcon
from config import *


class MainWindow(QWidget):
    """
    Main application window displaying control buttons.
    """

    config = AppConfig()

    def __init__(self) -> None:
        """
        Initializes the main window, layout, buttons, and styles.
        """
        super().__init__()
        self.setWindowTitle("Power Menu")

        # List to hold the buttons for easy navigation
        self.buttons = []
        # Index of the currently focused button (still useful for arrow key logic)
        self.currentFocusIndex = 0

        # Setup UI elements
        self.setupUI()

        # Apply global styles using stylesheets
        self.applyStyles()

        # Set initial focus to the first button
        if self.buttons:
            self.buttons[self.currentFocusIndex].setFocus()

    def setupUI(self):
        """
        Sets up the user interface elements like layout and buttons.
        """
        # Horizontal layout
        layout = QHBoxLayout()
        # Remove spacing and margins for a tighter look
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Icons
        shutdownIcon = qta.icon(
            self.config.shutdownIcon,
            color=self.config.iconColor,
            color_active=self.config.iconColorActive,
        )
        rebootIcon = qta.icon(
            self.config.rebootIcon,
            color=self.config.iconColor,
            color_active=self.config.iconColorActive,
        )
        logoffIcon = qta.icon(
            self.config.logoffIcon,
            color=self.config.iconColor,
            color_active=self.config.iconColorActive,
        )

        # Icon size
        iconSize = QSize(self.config.iconSizeW, self.config.iconSizeH)

        # Create buttons and add them to layout and list

        # shutdownButton
        shutdownButton = self.createButton("Shutdown", shutdownIcon, iconSize)
        shutdownButton.clicked.connect(self.shutdownButtonClick)
        self.buttons.append(shutdownButton)
        # rebootButton
        rebootButton = self.createButton("Reboot", rebootIcon, iconSize)
        rebootButton.clicked.connect(self.rebootButtonClick)
        self.buttons.append(rebootButton)
        # logoffButton
        logoffButton = self.createButton("Logoff", logoffIcon, iconSize)
        logoffButton.clicked.connect(self.logoffButtonClick)
        self.buttons.append(logoffButton)

        for button in self.buttons:
            layout.addWidget(button)

        # Set the layout on the main window
        self.setLayout(layout)
        # Adjust window size to fit content snugly
        self.adjustSize()
        # Optional: Make window non-resizable
        # self.setFixedSize(self.size())

    def shutdownButtonClick(self) -> None:
        """
        Action performed when the shutdown button is clicked or activated.
        """
        print("Shutdown button clicked")
        os.system(command=self.config.shutdownCommand)

    def rebootButtonClick(self) -> None:
        """
        Action performed when the reboot button is clicked or activated.
        """
        print("Reboot button clicked")
        os.system(command=self.config.rebootCommand)

    def logoffButtonClick(self) -> None:
        """
        Action performed when the logoff button is clicked or activated.
        """
        print("Logoff button clicked")
        os.system(command=self.config.logoffCommand)

    def createButton(self, tooltip: str, icon: QIcon, iconSize: QSize) -> QToolButton:
        """
        Creates a QToolButton with specified properties.

        Args:
            tooltip (str): The text to show when hovering over the button.
            icon (QIcon): The icon for the button (created using qtawesome).
            iconSize (QSize): The desired size of the icon.

        Returns:
            QToolButton: The configured tool button.
        """
        button = QToolButton()
        button.setIcon(icon)
        button.setIconSize(iconSize)
        button.setToolTip(tooltip)
        # Set focus policy to allow keyboard focus
        button.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        return button

    def applyStyles(self) -> None:
        """
        Applies CSS-like stylesheets for appearance and hover/focus effects.
        """
        self.setStyleSheet(
            """
            QWidget {
                background-color: %s; /* Window background */
            }
            QToolButton {
                background-color: transparent; /* Default transparent background */
                border: 2px solid transparent; /* Add transparent border to reserve space */
                border-radius: 15px; /* Rounded corners */
                padding: 5px; /* Add some padding around the icon */
                margin: 0px; /* No margin between buttons */
            }
            /* Style for when the button has keyboard focus */
            QToolButton:focus {
                border: 2px solid %s; 
                background-color: transparent; /* Slightly lighter background when focused */
            }
            /* Optional: Style for when the mouse is hovering */
            QToolButton:hover {
                background-color: #222222; /* Dark gray background on hover */
            }
            QToolTip {
                color: black;
                background-color: lightgray;
                border: 1px solid black;
            }
        """
            % (self.config.MainWindow.backgrounColor, self.config.iconColor)
        )

    # --- MÉTODO CORRIGIDO ---
    def keyPressEvent(self, event: QKeyEvent):
        """
        Handles key press events for navigation between buttons and triggering actions.

        Args:
            event (QKeyEvent): The key event object.
        """
        key = event.key()
        numButtons = len(self.buttons)

        if not numButtons:  # Do nothing if there are no buttons
            super().keyPressEvent(event)
            return

        # Handle Escape key to exit the application
        if key == Qt.Key.Key_Escape:
            self.close()  # Close the window

        elif key == Qt.Key.Key_Right:
            # Move focus to the next button, wrap around
            self.currentFocusIndex = (self.currentFocusIndex + 1) % numButtons
            self.buttons[self.currentFocusIndex].setFocus()
        elif key == Qt.Key.Key_Left:
            # Move focus to the previous button, wrap around
            self.currentFocusIndex = (
                self.currentFocusIndex - 1 + numButtons
            ) % numButtons
            self.buttons[self.currentFocusIndex].setFocus()
        # --- CONDIÇÃO CORRIGIDA ---
        # Check for Enter key (Return on main keyboard, Enter on numpad)
        elif key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            # Get the widget that currently has focus within this window
            focusedWidget = self.focusWidget()
            # Check if the focused widget is one of our QToolButtons
            if isinstance(focusedWidget, QToolButton) and focusedWidget in self.buttons:
                # Trigger the click action of the actually focused button
                focusedWidget.click()  # Simulate a button click on the focused widget
            # --- FIM DA CONDIÇÃO CORRIGIDA ---
        else:
            # Handle other keys normally by passing the event to the parent
            super().keyPressEvent(event)


def passArgs() -> None:
    printAsciiArt()
    # Configuração do parser
    parser = argparse.ArgumentParser(
        description=f"pwrmenu - A Modern Power Menu for Hyprland. Version: {getGitVersionInfo()}.",
    )

    # Argumentos
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=AppConfig.CONFIG_SOURCES.file,
        required=False,
        help="Path to the config file (config.yaml)",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"pwrmenu - Version: {getGitVersionInfo()}",
        help="Show the version and exit",
    )

    # Processamento dos argumentos
    args: argparse.Namespace = parser.parse_args()

    AppConfig.CONFIG_SOURCES = FileSource(file=args.config)
    print("Using config file: ", args.config)

    if not os.path.exists(args.config):
        print("Config file not found. Creating a new one.")
        sys.exit(1)
    else:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    passArgs()
