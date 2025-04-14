# -*- coding: utf-8 -*-

"""
Simple Power Menu application
"""
import sys
import qtawesome as qta
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QToolButton
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QKeyEvent  # Import QKeyEvent for type hinting


class MainWindow(QWidget):
    """
    Main application window displaying control buttons.
    """

    def __init__(self):
        """
        Initializes the main window, layout, buttons, and styles.
        """
        super().__init__()
        self.setWindowTitle("Control Panel")

        # List to hold the buttons for easy navigation
        self.buttons = []
        # Index of the currently focused button
        self.currentFocusIndex = 0

        # Setup UI elements
        self.setupUI()

        # Apply global styles using stylesheets
        self.applyStyles()

        # Set initial focus to the first button
        # This line was already here, but the focus state wasn't visually distinct
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
        shutdownIcon = qta.icon("fa6s.power-off", color="white", color_active="black")
        rebootIcon = qta.icon("fa6s.repeat", color="white", color_active="black")
        logoffIcon = qta.icon(
            "ri.logout-box-r-fill", color="white", color_active="black"
        )

        # Icon size
        iconSize = QSize(120, 120)

        # Create buttons and add them to layout and list
        self.buttons.append(self.createButton("Shutdown", shutdownIcon, iconSize))
        self.buttons.append(self.createButton("Reboot", rebootIcon, iconSize))
        self.buttons.append(self.createButton("Logoff", logoffIcon, iconSize))

        for button in self.buttons:
            layout.addWidget(button)

        # Set the layout on the main window
        self.setLayout(layout)
        # Adjust window size to fit content snugly
        self.adjustSize()
        # Optional: Make window non-resizable
        # self.setFixedSize(self.size())

    def createButton(self, tooltip: str, icon, iconSize: QSize) -> QToolButton:
        """
        Creates a QToolButton with specified properties.

        Args:
            tooltip (str): The text to show when hovering over the button.
            icon: The icon for the button (created using qtawesome).
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

    def applyStyles(self):
        """
        Applies CSS-like stylesheets for appearance and hover/focus effects.
        """
        self.setStyleSheet(
            """
            QWidget {
                background-color: black; /* Window background */
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
                border: 2px solid white; /* White border when focused */
                background-color: #333333; /* Slightly lighter background when focused */
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
        )

    def keyPressEvent(self, event: QKeyEvent):
        """
        Handles key press events for navigation between buttons.

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
            self.close()
            # Consider using QApplication.quit() for a cleaner exit sometimes
            # sys.exit(0) # This can be abrupt

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
        # Allow Enter/Return key to activate the focused button if needed
        # elif key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
        #     if self.focusWidget() in self.buttons:
        #         # Add action here, e.g., self.buttons[self.currentFocusIndex].click()
        #         print(f"{self.buttons[self.currentFocusIndex].toolTip()} activated")
        #     super().keyPressEvent(event)
        else:
            # Handle other keys normally
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
